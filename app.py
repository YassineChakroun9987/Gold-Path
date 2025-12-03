import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from graphviz import Digraph
import tempfile
import os
import streamlit.components.v1 as components

# -----------------------------------------------------------
# PAGE CONFIG + GLOBAL UI THEME
# -----------------------------------------------------------
st.set_page_config(
    page_title="Shortest Path Multi-Criteria",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS (Design + Animations)
st.markdown("""
<style>
/* ---------- ROOT VARIABLES ---------- */
:root {
    --light-bg: #f8f9fa;
    --card-bg: #ffffff;
    --text-primary: #2c3e50;
    --text-secondary: #5d6d7e;
    --accent-gold: #b8860b;
    --accent-gold-dark: #8b6914;
    --accent-gold-light: #f5e8c6;
    --accent-gold-lighter: #f9f3e3;
    --primary-blue: #3498db;
    --success: #27ae60;
    --border: #e9ecef;
    --shadow: rgba(0, 0, 0, 0.05);
}

/* ---------- GLOBAL STYLES ---------- */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    background-color: var(--light-bg);
    color: var(--text-primary);
    scroll-behavior: smooth;
}

.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    animation: gradientBG 20s ease infinite;
    background-size: 400% 400%;
}

/* ---------- ANIMATIONS ---------- */
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    0% { opacity: 0; transform: translateX(-20px); }
    100% { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    0% { opacity: 0; transform: translateX(20px); }
    100% { opacity: 1; transform: translateX(0); }
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ---------- HEADERS WITH GOLD ACCENT ---------- */
h1 {
    font-weight: 800 !important;
    color: var(--accent-gold-dark) !important;
    letter-spacing: -0.5px;
    padding-bottom: 15px;
    margin-bottom: 30px;
    border-bottom: 3px solid var(--accent-gold);
    animation: slideInLeft 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    background: linear-gradient(90deg, var(--accent-gold), transparent);
    background-size: 100% 3px;
    background-position: bottom left;
    background-repeat: no-repeat;
}

h2, h3, h4, h5, h6 {
    color: var(--accent-gold-dark) !important;
    font-weight: 700 !important;
    animation: fadeIn 0.6s ease-out;
}

/* ---------- TEXT ELEMENTS ---------- */
p, li, span, div {
    color: var(--text-primary) !important;
}

/* ---------- SECTION TITLES ---------- */
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin: 35px 0 20px 0;
    color: var(--accent-gold-dark) !important;
    padding-left: 16px;
    border-left: 4px solid var(--accent-gold);
    animation: slideInLeft 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    background: linear-gradient(90deg, rgba(184, 134, 11, 0.05) 0%, transparent 100%);
    padding: 12px 20px;
    border-radius: 0 10px 10px 0;
    letter-spacing: -0.3px;
}

/* ---------- ENHANCED CARD DESIGN ---------- */
.card {
    padding: 25px;
    background: var(--card-bg);
    border-radius: 16px;
    box-shadow: 
        0 3px 12px var(--shadow),
        inset 0 1px 0 rgba(255, 255, 255, 0.7);
    animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(184, 134, 11, 0.08);
    margin-bottom: 20px;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 6px 20px rgba(184, 134, 11, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

/* ---------- BUTTON DESIGN ---------- */
.stButton button {
    background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-dark) 100%);
    color: white !important;
    border: none;
    padding: 12px 28px;
    font-weight: 600;
    font-size: 0.95rem;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(184, 134, 11, 0.2);
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(184, 134, 11, 0.3);
}





/* ---------- UPLOADER STYLING WITH WHITE TEXT ---------- */
.stFileUploader {
    animation: slideInRight 0.6s ease;
}

.stFileUploader > div {
    border: 2px dashed rgba(184, 134, 11, 0.3) !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, rgba(184, 134, 11, 0.1) 0%, rgba(139, 105, 20, 0.1) 100%) !important;
    transition: all 0.3s ease !important;
}

/* Target the "Drag and drop file here" text specifically */
.stFileUploader > div > div > div > div > div > div > div {
    color: white !important;
    font-weight: 500 !important;
}

.stFileUploader > div:hover {
    border-color: var(--accent-gold) !important;
    background: linear-gradient(135deg, rgba(184, 134, 11, 0.15) 0%, rgba(139, 105, 20, 0.15) 100%) !important;
}

/* Also target the browse files button text */
.stFileUploader button {
    color: white !important;
    background: var(--accent-gold) !important;
    border-radius: 8px !important;
}

.stFileUploader button:hover {
    background: var(--accent-gold-dark) !important;
}

/* ---------- DATA FRAME STYLING ---------- */
/* Light background for tables */
.dataframe {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid rgba(184, 134, 11, 0.2) !important;
    animation: fadeIn 0.6s ease !important;
    background-color: var(--accent-gold-lighter) !important;
}

/* Gold bold headers */
.dataframe th {
    background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-dark) 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 12px 15px !important;
    text-align: center !important;
}

/* Table cells */
.dataframe td {
    border: 1px solid rgba(184, 134, 11, 0.1) !important;
    padding: 10px 15px !important;
    color: var(--text-primary) !important;
    background-color: var(--accent-gold-lighter) !important;
}

/* Remove default borders */
.dataframe tbody tr {
    border-bottom: 1px solid rgba(184, 134, 11, 0.1) !important;
}

/* Hover effect */
.dataframe tbody tr:hover {
    background-color: rgba(184, 134, 11, 0.1) !important;
}

/* ---------- GRADIENT TABLE CELLS ---------- */
.gradient-low {
    background: linear-gradient(135deg, #f9f3e3 0%, #f5e8c6 100%) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.gradient-medium {
    background: linear-gradient(135deg, #f0dcaf 0%, #e8cf9a 100%) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.gradient-high {
    background: linear-gradient(135deg, #e8c87a 0%, #dbb85c 100%) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.gradient-very-high {
    background: linear-gradient(135deg, #dbb85c 0%, #b8860b 100%) !important;
    color: white !important;
    font-weight: 600 !important;
}

/* ---------- GRAPH CONTAINER - CENTERED ---------- */
.graph-container {
    border-radius: 16px;
    background: var(--card-bg);
    padding: 20px;
    box-shadow: 
        0 3px 12px var(--shadow),
        inset 0 1px 0 rgba(255, 255, 255, 0.7);
    animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid var(--border);
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
    max-width: 90%;
}

/* Center the graph SVG */
.graph-container svg {
    display: block;
    margin: 0 auto;
}

/* TIME WEIGHT slider */
div[data-testid="stSlider"] label:has(span:contains("Time Weight")) ~ div input[type="range"]::-webkit-slider-runnable-track {
    background: #0A3D62 !important;
}
div[data-testid="stSlider"] label:has(span:contains("Time Weight")) ~ div input[type="range"]::-webkit-slider-thumb {
    background: #074273 !important;
    border: 2px solid #0A3D62 !important;
}

/* COST WEIGHT slider */
div[data-testid="stSlider"] label:has(span:contains("Cost Weight")) ~ div input[type="range"]::-webkit-slider-runnable-track {
    background: #0A3D62 !important;
}
div[data-testid="stSlider"] label:has(span:contains("Cost Weight")) ~ div input[type="range"]::-webkit-slider-thumb {
    background: #074273 !important;
    border: 2px solid #0A3D62 !important;
}

/* RISK WEIGHT slider */
div[data-testid="stSlider"] label:has(span:contains("Risk Weight")) ~ div input[type="range"]::-webkit-slider-runnable-track {
    background: #0A3D62 !important;
}
div[data-testid="stSlider"] label:has(span:contains("Risk Weight")) ~ div input[type="range"]::-webkit-slider-thumb {
    background: #074273 !important;
    border: 2px solid #0A3D62 !important;
}
  

/* ---------- ALERT MESSAGES ---------- */
.stAlert {
    border-radius: 10px !important;
    border-left: 4px solid !important;
    animation: slideInRight 0.4s ease !important;
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
}

.stSuccess {
    border-left-color: var(--success) !important;
    color: #155724 !important;
}

.stError {
    border-left-color: #e74c3c !important;
    color: #721c24 !important;
}

/* ---------- WEIGHT DISPLAY ---------- */
.weight-display {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
    padding: 15px;
    background: linear-gradient(135deg, rgba(184, 134, 11, 0.05) 0%, rgba(139, 105, 20, 0.05) 100%);
    border-radius: 10px;
    animation: fadeIn 0.6s ease;
    border: 1px solid rgba(184, 134, 11, 0.1);
}

.weight-item {
    text-align: center;
    padding: 10px;
    flex: 1;
}

.weight-value {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent-gold-dark);
    margin-bottom: 5px;
}

.weight-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ---------- METRIC CARDS ---------- */
.metric-card {
    padding: 15px;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 10px;
    border-left: 4px solid var(--accent-gold);
    animation: fadeIn 0.5s ease;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-gold-dark);
    margin-bottom: 5px;
}

.metric-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
}

/* ---------- SCROLLBAR STYLING ---------- */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(184, 134, 11, 0.05);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: var(--accent-gold);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-gold-dark);
}

/* ---------- REMOVE WHITE DIVS ---------- */
div[data-testid="stVerticalBlock"] > div > div {
    background: transparent !important;
}

/* ---------- CENTERED CONTAINER FOR GRAPH ---------- */
.centered-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

/* ---------- FORCE WHITE TEXT IN UPLOADER ---------- */
div[data-testid="stFileUploader"] span {
    color: white !important;
}

/* Make sure ALL text in uploader is white */
div[data-testid="stFileUploader"] * {
    color: white !important;
}

/* ---------- BUTTON TEXT WHITE ---------- */
.stButton button, .stButton button span, .stButton button p {
    color: white !important;
}
            


</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# UTIL: shorten edges (unchanged)
# -----------------------------------------------------------
def shorten_edge(pos_u, pos_v, node_radius=0.08):
    x1, y1 = pos_u
    x2, y2 = pos_v
    dx = x2 - x1
    dy = y2 - y1
    dist = np.sqrt(dx*dx + dy*dy)

    if dist == 0:
        return x2, y2

    ratio = (dist - node_radius) / dist
    return x1 + dx * ratio, y1 + dy * ratio


# -----------------------------------------------------------
# FLOYD–WARSHALL WITH PATH RECONSTRUCTION
# -----------------------------------------------------------
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


# -----------------------------------------------------------
# PATH TOTALS (Weighted + Time + Cost + Risk)
# -----------------------------------------------------------
def compute_path_totals(path, orig_time, orig_cost, orig_risk,
                        w_time, w_cost, w_risk):

    total_time = total_cost = total_risk = total_weighted = 0

    for k in range(len(path) - 1):
        i = path[k]
        j = path[k+1]

        t = orig_time[i][j] if orig_time[i][j] != 9999 else 0
        c = orig_cost[i][j] if orig_cost[i][j] != 9999 else 0
        r = orig_risk[i][j] if orig_risk[i][j] != 9999 else 0

        total_time += t
        total_cost += c
        total_risk += r
        total_weighted += w_time*t + w_cost*c + w_risk*r

    return total_weighted, total_time, total_cost, total_risk


# -----------------------------------------------------------
# GRAPHVIZ VISUALIZATION
# -----------------------------------------------------------
def visualize_graph(graph, node_labels, title="Graph"):
    import re
    import tempfile
    import os
    from graphviz import Digraph
    import streamlit.components.v1 as components

    dark_pastels = [
        "#7BB5C8", "#E58A87", "#E5B08A", "#AFCF95", "#C7DAA3",
        "#8ECBCB", "#E39A9A", "#D3A9A7", "#A6AFD1", "#CB97BC",
        "#D2C088", "#9FBEB7"
    ]
    V = len(graph)
    node_colors = {str(i): dark_pastels[i % len(dark_pastels)] for i in range(V)}

    dot = Digraph(engine="neato")

    # Better spacing but WITHOUT forcing huge size
    dot.attr(
        format="png",
        overlap="false",
        splines="true",
        dpi="96",
        ratio="compress",
        nodesep="1.0",
        ranksep="1.0",
        K="0.8",
        bgcolor="transparent"
    )

    for i in range(V):
        dot.node(
            str(i),
            node_labels[i],
            shape="circle",
            style="filled",
            fillcolor=node_colors[str(i)],
            color="black",
            fontsize="16",
            width="1.0"
        )

    for i in range(V):
        for j in range(V):
            if i != j and graph[i][j] != 9999:
                dot.edge(
                    str(i), str(j),
                    label=str(round(graph[i][j], 2)),
                    color=node_colors[str(i)],
                    fontcolor=node_colors[str(i)],
                    arrowsize="0.9",
                    fontsize="12"
                )

    # Render SVG
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "graph")
        dot.render(filepath, format="svg", cleanup=True)
        with open(filepath + ".svg", "r", encoding="utf-8") as f:
            svg = f.read()

    # --------------------------------------------------
    # 1. Extract original viewBox or width/height
    # --------------------------------------------------
    viewbox_match = re.search(r'viewBox="([\d\.\s\-]+)"', svg)
    if viewbox_match:
        original_viewbox = viewbox_match.group(1)
    else:
        # fallback to width/height parsing
        w = re.search(r'width="([\d\.]+)', svg)
        h = re.search(r'height="([\d\.]+)', svg)
        if w and h:
            original_viewbox = f"0 0 {w.group(1)} {h.group(1)}"
        else:
            original_viewbox = "0 0 2000 1200"   # safe fallback

    # --------------------------------------------------
    # 2. Apply a NORMALIZED viewBox for scaling
    # --------------------------------------------------
    svg = re.sub(
        r'viewBox="[^"]+"',
        f'viewBox="{original_viewbox}"',
        svg
    )

    # Remove fixed width/height
    svg = re.sub(r'width="[^"]+"', 'width="100%"', svg)
    svg = re.sub(r'height="[^"]+"', 'height="100%"', svg)

    # Force responsive mode
    if "preserveAspectRatio" in svg:
        svg = re.sub(r'preserveAspectRatio="[^"]+"',
                     'preserveAspectRatio="xMidYMid meet"', svg)
    else:
        svg = svg.replace("<svg", '<svg preserveAspectRatio="xMidYMid meet"')

    # --------------------------------------------------
    # 3. Streamlit container (NO CROPPING)
    # --------------------------------------------------
    initial_zoom = 0.20      # <<< TRY VALUES: 0.45, 0.35, 0.25, 0.20, 0.15, 0.10
    initial_pan_x = 0        # <<< shift left/right (positive → right)
    initial_pan_y = 0        # <<< shift up/down (positive → down)

    components.html(
        f"""
        <div style="
            width: 100%;
            max-width: 1800px;
            height: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg,#f8f9fa,#e9ecef);
            border-radius: 18px;
            border: 1px solid #e9ecef;
            box-shadow: 0 3px 12px rgba(0,0,0,0.05);
            overflow: hidden;
        ">

            <div id="svg_container" style="width:100%; height:100%; overflow:hidden;">
                {svg}
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/svg-pan-zoom/3.6.1/svg-pan-zoom.min.js"></script>

            <script>
                const svgEl = document.querySelector('#svg_container svg');

                // Make responsive
                svgEl.removeAttribute('width');
                svgEl.removeAttribute('height');
                svgEl.style.width = "100%";
                svgEl.style.height = "100%";

                // Init pan/zoom
                const instance = svgPanZoom(svgEl, {{
                    zoomEnabled: true,
                    controlIconsEnabled: true,
                    fit: false,         // <<< IMPORTANT: disable auto fit so manual zoom works
                    center: false,
                    minZoom: 0.01,
                    maxZoom: 10,
                    contain: false
                }});

                // Apply manual zoom and pan
                setTimeout(() => {{
                    instance.zoom({initial_zoom});
                    instance.pan({{ x: {initial_pan_x}, y: {initial_pan_y} }});
                }}, 50);
            </script>

        </div>
        """,
        height=850,
        scrolling=False
    )

# -----------------------------------------------------------
# UI LAYOUT
# -----------------------------------------------------------
st.markdown("<h1>Gold Trade Path Multi-Criteria Optimizer</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='card'>
<h3 style='margin-top:0; color: var(--accent-gold-dark);'>Upload Your Dataset</h3>
<p style='color: var(--text-primary); line-height: 1.6; margin-bottom: 0;'>
Upload an Excel file with 3 sheets: <strong>Time</strong>, <strong>Cost</strong>, <strong>Risk</strong>.
Each sheet must contain a square adjacency matrix with identical node names.
</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# FILE UPLOAD
# -----------------------------------------------------------
file = st.file_uploader("Upload Excel File", type=["xlsx"], help="Upload your Excel file with Time, Cost, and Risk sheets")

if file:
    st.markdown("<div class='section-title'>Matrix Validation</div>", unsafe_allow_html=True)
    
    try:
        time_df = pd.read_excel(file, sheet_name="Time", index_col=0)
        cost_df = pd.read_excel(file, sheet_name="Cost", index_col=0)
        risk_df = pd.read_excel(file, sheet_name="Risk", index_col=0)
    except:
        st.error("File must contain sheets: Time, Cost, Risk.")
        st.stop()

    # Validate
    if time_df.shape[0] != time_df.shape[1]:
        st.error("Time matrix is not square."); st.stop()
    if cost_df.shape[0] != cost_df.shape[1]:
        st.error("Cost matrix is not square."); st.stop()
    if risk_df.shape[0] != risk_df.shape[1]:
        st.error("Risk matrix is not square."); st.stop()

    if not (list(time_df.index) == list(cost_df.index) == list(risk_df.index)):
        st.error("Sheet node labels do not match."); st.stop()

    node_labels = list(time_df.index)
    V = len(node_labels)

    st.success(f"**{V} nodes loaded successfully:** {', '.join(node_labels)}")

    # Matrix prep
    time_graph = np.nan_to_num(time_df.to_numpy(), nan=9999)
    cost_graph = np.nan_to_num(cost_df.to_numpy(), nan=9999)
    risk_graph = np.nan_to_num(risk_df.to_numpy(), nan=9999)

    orig_time = time_graph.copy()
    orig_cost = cost_graph.copy()
    orig_risk = risk_graph.copy()

    # -------------------------------------------------------
    # Weights
    # -------------------------------------------------------
    st.markdown("<div class='section-title'>Weight Configuration</div>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            w_time = st.slider("Time Weight", 0.0, 1.0, 0.33, 0.01, help="Importance of time in path optimization")
        with col2:
            w_cost = st.slider("Cost Weight", 0.0, 1.0, 0.33, 0.01, help="Importance of cost in path optimization")
        with col3:
            w_risk = st.slider("Risk Weight", 0.0, 1.0, 0.34, 0.01, help="Importance of risk in path optimization")

        total = w_time + w_cost + w_risk
        w_time /= total
        w_cost /= total
        w_risk /= total

        # Display weight summary
        st.markdown("---")
        st.markdown("#### Normalized Weights")
        
        cols = st.columns(3)
        with cols[0]:
            st.markdown(f"""
            <div class='weight-item'>
                <div class='weight-value'>{w_time:.2%}</div>
                <div class='weight-label'>Time</div>
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"""
            <div class='weight-item'>
                <div class='weight-value'>{w_cost:.2%}</div>
                <div class='weight-label'>Cost</div>
            </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"""
            <div class='weight-item'>
                <div class='weight-value'>{w_risk:.2%}</div>
                <div class='weight-label'>Risk</div>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # RUN COMPUTATION
    # -------------------------------------------------------
    st.markdown("<div class='section-title'>Compute Shortest Paths</div>", unsafe_allow_html=True)

    if st.button("Run Floyd-Warshall Algorithm", key="run_algo"):
        
        with st.spinner("Computing optimal paths..."):
            
            # Weighted combined graph
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("#### Weighted Combined Matrix")

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

            # Display weighted matrix with gold headers
            weighted_df = pd.DataFrame(final_graph, index=node_labels, columns=node_labels)
            st.dataframe(
                weighted_df.style.format(
                    lambda x: "∞" if x == 9999 else f"{x:.2f}"
                ),
                use_container_width=True,
                height=470   # Increase this value until the matrix fits
            )

            st.markdown("</div>", unsafe_allow_html=True)

            # Graph visualization - centered
            st.markdown("<div class='section-title'>Graph Visualization</div>", unsafe_allow_html=True)
            visualize_graph(final_graph, node_labels, "Weighted Graph")

            # Floyd–Warshall
            dist_matrix = final_graph.copy()
            dist_matrix, next_node = floydWarshall_with_path(dist_matrix)

            # PATH OUTPUT
            st.markdown("<div class='section-title'>All Shortest Paths</div>", unsafe_allow_html=True)
            
            with st.container():
                rows = []
                for i in range(V):
                    for j in range(V):
                        if i != j:
                            path = reconstruct_path(i, j, next_node)
                            if path:
                                total_w, total_t, total_c, total_r = compute_path_totals(
                                    path, orig_time, orig_cost, orig_risk,
                                    w_time, w_cost, w_risk
                                )
                                rows.append({
                                    "From": node_labels[i],
                                    "To": node_labels[j],
                                    "Path": " → ".join(node_labels[p] for p in path),
                                    "Total Score": round(total_w, 2),
                                    "Total Time": round(total_t, 2),
                                    "Total Cost": round(total_c, 2),
                                    "Total Risk": round(total_r, 2),
                                })
                            else:
                                rows.append({
                                    "From": node_labels[i],
                                    "To": node_labels[j],
                                    "Path": "NO PATH",
                                    "Total Score": None,
                                    "Total Time": None,
                                    "Total Cost": None,
                                    "Total Risk": None,
                                })

                df_results = pd.DataFrame(rows)
                
                # Apply gradient styling based on values
                def apply_gradient_styling(df):
                    # Define gradient classes for numeric columns
                    numeric_cols = ['Total Score', 'Total Time', 'Total Cost', 'Total Risk']
                    
                    # Initialize style dictionary
                    styles = {}
                    
                    for col in numeric_cols:
                        if col in df.columns:
                            # Get valid values (non-null)
                            valid_values = df[col].dropna()
                            if len(valid_values) > 0:
                                # Calculate quartiles
                                q1 = valid_values.quantile(0.25)
                                q2 = valid_values.quantile(0.50)
                                q3 = valid_values.quantile(0.75)
                                
                                # Apply gradient classes
                                def get_gradient_class(val):
                                    if pd.isna(val):
                                        return ''
                                    elif val <= q1:
                                        return 'gradient-low'
                                    elif val <= q2:
                                        return 'gradient-medium'
                                    elif val <= q3:
                                        return 'gradient-high'
                                    else:
                                        return 'gradient-very-high'
                                
                                styles[col] = df[col].apply(get_gradient_class)
                            else:
                                styles[col] = [''] * len(df)
                    
                    return styles
                
                # Apply styling
                gradient_styles = apply_gradient_styling(df_results)
                
                # Create styled dataframe
                styled_df = df_results.style.set_table_styles([
                    {'selector': 'th', 'props': [
                        ('background', 'linear-gradient(135deg, #b8860b 0%, #8b6914 100%)'),
                        ('color', 'white'),
                        ('font-weight', 'bold'),
                        ('text-align', 'center')
                    ]},
                    {'selector': 'td', 'props': [
                        ('color', 'var(--text-primary)'),
                        ('background-color', 'var(--accent-gold-lighter)')
                    ]}
                ])
                
                # Apply gradient classes
                for col, styles in gradient_styles.items():
                    styled_df = styled_df.set_td_classes(pd.DataFrame({
                        col: styles
                    }))
                
                # Display the dataframe
                st.dataframe(
                    styled_df.format({
                        'Total Score': '{:.2f}',
                        'Total Time': '{:.2f}',
                        'Total Cost': '{:.2f}',
                        'Total Risk': '{:.2f}'
                    }),
                    use_container_width=True,
                    height=400
                )
                
                # Summary statistics
                st.markdown("---")
                valid_paths = df_results[df_results['Path'] != 'NO PATH']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>{len(df_results)}</div>
                        <div class='metric-label'>Total Paths</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>{len(valid_paths)}</div>
                        <div class='metric-label'>Valid Paths</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>{valid_paths['Total Score'].min():.2f}</div>
                        <div class='metric-label'>Best Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>{valid_paths['Total Score'].mean():.2f}</div>
                        <div class='metric-label'>Average Score</div>
                    </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
<p style='color: var(--text-secondary);'>
<br>
<strong>Gold Trade Path Multi-Criteria Optimizer</strong><br>
Floyd-Warshall Algorithm • Graph Visualization • Multi-Objective Optimization
</p>
</div>
""", unsafe_allow_html=True)
