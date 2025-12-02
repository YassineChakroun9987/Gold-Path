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

            svgEl.removeAttribute('width');
            svgEl.removeAttribute('height');
            svgEl.style.width = "100%";
            svgEl.style.height = "100%";

            svgPanZoom(svgEl, {{
                zoomEnabled: true,
                controlIconsEnabled: true,
                fit: true,
                center: true,
                minZoom: 0.3,
                contain: false
            }});
        </script>

    </div>
    """,
    height=850,
    scrolling=False
)
