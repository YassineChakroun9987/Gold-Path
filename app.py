import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ============================================
# Floyd–Warshall with PATH Reconstruction
# ============================================
def floydWarshall_with_path(graph):
    V = len(graph)
    next_node = [[None] * V for _ in range(V)]

    for i in range(V):
        for j in range(V):
            if graph[i][j] != 9999 and i != j:
                next_node[i][j] = j

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if graph[i][k] + graph[k][j] < graph[i][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]
                    next_node[i][j] = next_node[i][k]

    return graph, next_node


def reconstruct_path(i, j, next_node):
    if next_node[i][j] is None:
        return None
    path = [i]
    while i != j:
        i = next_node[i][j]
        path.append(i)
    return path


# ============================================
# Visualization
# ============================================
def visualize_graph(graph, title="Graph"):
    G = nx.DiGraph()
    V = len(graph)

    for i in range(V):
        G.add_node(i)

    for i in range(V):
        for j in range(V):
            if graph[i][j] != 9999 and i != j:
                G.add_edge(i, j, weight=graph[i][j])

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(9, 7))

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="gray")
    labels = {node: node + 1 for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12)

    for (u, v, data) in G.edges(data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        lx = x1 + 0.7 * (x2 - x1)
        ly = y1 + 0.7 * (y2 - y1)
        plt.text(lx, ly, str(data["weight"]), fontsize=10,
                 bbox=dict(facecolor="white", edgecolor="none", alpha=0.7))

    plt.title(title)
    plt.axis("off")
    st.pyplot(plt)


# ============================================
# APP
# ============================================
st.title("Shortest Path Multi-Criteria App (Floyd–Warshall + Paths)")
st.write("Fill matrices for time, cost, risk and choose weights.")

# --------------------------------------------
# Step 1 — Number of nodes
# --------------------------------------------
V = st.number_input("Number of nodes", min_value=2, max_value=15, value=4)

st.write("Nodes will be labeled 1 ..", V)

# --------------------------------------------
# Create empty matrices
# --------------------------------------------
def create_matrix(label):
    st.subheader(label)
    matrix = np.zeros((V, V), dtype=float)

    for i in range(V):
        for j in range(V):
            key = f"{label}_{i}_{j}"
            if i == j:
                st.number_input(f"{i+1} → {j+1}", value=0.0, key=key, disabled=True)
                matrix[i][j] = 0
            else:
                matrix[i][j] = st.number_input(f"{i+1} → {j+1}", value=9999.0, key=key)
    return matrix


time_graph = create_matrix("Time Matrix")
cost_graph = create_matrix("Cost Matrix")
risk_graph = create_matrix("Risk Matrix")

# --------------------------------------------
# Weights
# --------------------------------------------
st.subheader("Weights")
w_time = st.slider("Weight for Time", 0.0, 1.0, 0.33)
w_cost = st.slider("Weight for Cost", 0.0, 1.0, 0.33)
w_risk = st.slider("Weight for Risk", 0.0, 1.0, 0.34)

# Normalize (optional)
total = w_time + w_cost + w_risk
w_time /= total
w_cost /= total
w_risk /= total

st.write("Normalized Weights:", w_time, w_cost, w_risk)

# --------------------------------------------
# RUN BUTTON
# --------------------------------------------
if st.button("Compute Shortest Paths"):
    # Combine graph
    final_graph = np.zeros((V, V))
    for i in range(V):
        for j in range(V):
            if (
                (time_graph[i][j] == 9999 and w_time > 0) or
                (cost_graph[i][j] == 9999 and w_cost > 0) or
                (risk_graph[i][j] == 9999 and w_risk > 0)
            ):
                final_graph[i][j] = 9999  
            else:
                final_graph[i][j] = (
                    w_time * time_graph[i][j] +
                    w_cost * cost_graph[i][j] +
                    w_risk * risk_graph[i][j]
                )

    st.subheader("Weighted Combined Matrix")
    st.table(final_graph)

    # Visualize
    st.subheader("Graph Before Floyd–Warshall")
    visualize_graph(final_graph, title="Weighted Graph")

    # Run Floyd-Warshall
    dist_matrix = final_graph.copy()
    dist_matrix, next_node = floydWarshall_with_path(dist_matrix)

    st.subheader("Shortest Distance Matrix (After FW)")
    st.table(dist_matrix)

    # Print all paths
    st.subheader("All Shortest Paths")
    for i in range(V):
        for j in range(V):
            if i != j:
                path = reconstruct_path(i, j, next_node)
                if path:
                    st.write(f"{i+1} → {j+1}: " + " → ".join(str(p+1) for p in path))
                else:
                    st.write(f"{i+1} → {j+1}: NO PATH")

    st.subheader("Graph After Floyd–Warshall")
    visualize_graph(dist_matrix, title="Shortest Path Graph")
