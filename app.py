import os
from pathlib import Path
import base64

import streamlit as st
import pandas as pd
from PIL import Image

from main import run_pipeline

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="SH-WFS Analysis System",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Styling -----------------------------
st.markdown("""
<style>
:root {
    --navy: #061426;
    --panel: #0a1d33;
    --panel2: #0d2742;
    --line: #14527b;
    --cyan: #16baf4;
    --text: #edf6ff;
    --muted: #9db5ca;
}
.stApp {
    background: radial-gradient(circle at 78% 0%, #102e4a 0%, #07182b 42%, #040d19 100%);
    color: var(--text);
}
[data-testid="stHeader"] { background: rgba(4, 13, 25, 0.88); }
.block-container { padding-top: 1.3rem; padding-bottom: 2.5rem; max-width: 1600px; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061426 0%, #081b30 100%);
    border-right: 1px solid #123a5a;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }
h1, h2, h3 { color: #f4f9ff !important; letter-spacing: -0.02em; }
p, label, span { color: inherit; }
div[data-testid="stFileUploader"] {
    background: rgba(10, 31, 53, .8);
    border: 1px solid #164c73;
    border-radius: 14px;
    padding: 10px;
}
div[data-testid="stFileUploader"] section { border: 1px dashed #2375a5; }
.stButton > button {
    background: linear-gradient(90deg, #087fd4, #13b5ed);
    color: white; border: 0; border-radius: 10px;
    font-weight: 700; min-height: 2.8rem;
    box-shadow: 0 5px 18px rgba(0, 153, 255, .18);
}
.stButton > button:hover { background: linear-gradient(90deg, #1098ed, #27c5f5); color: white; border: 0; }
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #102b47, #0a1d32);
    border: 1px solid #164e76; padding: 14px 16px; border-radius: 12px;
}
div[data-testid="stMetricLabel"] { color: #b7cde0 !important; }
div[data-testid="stMetricValue"] { color: #62e6ff !important; }
div[data-testid="stExpander"] {
    border: 1px solid #174d72; border-radius: 10px; background: rgba(9, 28, 48, .65);
}
hr { border-color: #174361; }
.panel-title {
    background: linear-gradient(90deg, rgba(12, 64, 102, .95), rgba(8, 31, 53, .92));
    border: 1px solid #17618d; border-radius: 12px;
    padding: 12px 16px; margin: 10px 0 14px 0;
    font-size: 1.18rem; font-weight: 750; color: #f2f8ff;
}
.subcard {
    background: linear-gradient(150deg, rgba(12, 34, 57, .98), rgba(6, 22, 39, .98));
    border: 1px solid #174f76; border-radius: 13px;
    padding: 12px 14px; min-height: 62px; margin-bottom: 8px;
}
.subcard h4 { margin: 0 0 7px 0; color: #f4f9ff; font-size: 1rem; }
.small-note { color: #9db5ca; font-size: .86rem; }
.pill {
    display: inline-block; border-radius: 999px; padding: 5px 11px;
    background: #075c35; color: #baffd5; font-size: .82rem; font-weight: 700;
}
.brand { display:flex; align-items:center; gap:12px; padding:8px 4px 20px 4px; }
.brand-name { font-size:1.12rem; font-weight:800; letter-spacing:.04em; color:#eaf8ff; }
.brand-caption { font-size:.75rem; color:#8db4d1; }
</style>
""", unsafe_allow_html=True)

logo_path = BASE_DIR / "assets" / "shwfs_logo.svg"
if logo_path.exists():
    logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    logo_html = f'<img src="data:image/svg+xml;base64,{logo_b64}" width="76" height="76">'
else:
    logo_html = '<div style="font-size:48px">🔭</div>'

# ----------------------------- Sidebar -----------------------------
with st.sidebar:
    st.markdown(
        f'<div class="brand">{logo_html}<div><div class="brand-name">SH-WFS</div>'
        '<div class="brand-caption">OPTICAL WAVEFRONT ANALYSIS</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Navigation")
    st.markdown("🔹 **Analysis**")
    st.markdown("⚙️ Workflow")
    st.markdown("ⓘ About")
    st.markdown("❔ Help")
    st.divider()
    st.markdown("### Processing Pipeline")
    steps = [
        "Spot Centroid Detection",
        "Spot Shift Calculation",
        "Wavefront Slopes",
        "Wavefront Reconstruction",
        "Zernike Coefficients",
        "Turbulence Characterization",
        "Actuator Map Generation",
        "Deformable Mirror Correction",
    ]
    for number, label in enumerate(steps, start=4):
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin:9px 0;">'
            f'<span style="background:#079ce5;color:white;border-radius:50%;'
            f'width:27px;height:27px;display:inline-flex;align-items:center;'
            f'justify-content:center;font-weight:800;">{number}</span>'
            f'<span style="font-size:.88rem;color:#d9e9f7;">{label}</span></div>',
            unsafe_allow_html=True,
        )
    st.divider()
    st.caption("SH-WFS Analysis • Academic software prototype")

# ----------------------------- Header -----------------------------
head_l, head_r = st.columns([5, 1])
with head_l:
    st.title("SH-WFS Analysis System")
    st.markdown(
        '<div style="color:#9fc7df;font-size:1.02rem;margin-top:-10px;">'
        'Shack–Hartmann Wavefront Reconstruction &amp; Turbulence Characterization'
        '</div>',
        unsafe_allow_html=True,
    )
with head_r:
    st.markdown(
        '<div style="text-align:right;font-size:2.8rem;padding-top:8px;">🔭</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="panel-title">⬆️ &nbsp; Input: Upload SH-WFS Images (Before Processing)</div>', unsafe_allow_html=True)

upload_left, upload_right = st.columns(2, gap="large")
allowed_types = ["png", "bmp", "jpg", "jpeg", "tif", "tiff"]

with upload_left:
    st.markdown("**Reference Image (Ideal Spots)**")
    reference_file = st.file_uploader(
        "Choose reference SH-WFS image",
        type=allowed_types,
        key="reference_upload",
    )
    if reference_file:
        st.image(Image.open(reference_file), caption=reference_file.name, use_container_width=True)

with upload_right:
    st.markdown("**Current Image (Aberrated Spots)**")
    current_file = st.file_uploader(
        "Choose current SH-WFS image",
        type=allowed_types,
        key="current_upload",
    )
    if current_file:
        st.image(Image.open(current_file), caption=current_file.name, use_container_width=True)

ready = reference_file is not None and current_file is not None
button_col, hint_col = st.columns([1, 3])
with button_col:
    process_clicked = st.button("⚙️  Process Images  ➜", disabled=not ready, use_container_width=True)
with hint_col:
    if not ready:
        st.markdown('<div class="small-note" style="padding-top:12px;">Upload both reference and current images to start the analysis.</div>', unsafe_allow_html=True)

if process_clicked:
    ref_ext = Path(reference_file.name).suffix.lower() or ".png"
    cur_ext = Path(current_file.name).suffix.lower() or ".png"
    ref_path = UPLOAD_DIR / f"reference_input{ref_ext}"
    cur_path = UPLOAD_DIR / f"current_input{cur_ext}"
    ref_path.write_bytes(reference_file.getvalue())
    cur_path.write_bytes(current_file.getvalue())

    try:
        with st.spinner("Processing images through the SH-WFS pipeline..."):
            st.session_state["shwfs_results"] = run_pipeline(str(ref_path), str(cur_path))
            st.session_state["shwfs_error"] = None
    except Exception as exc:
        st.session_state["shwfs_error"] = str(exc)
        st.session_state["shwfs_results"] = None

if st.session_state.get("shwfs_error"):
    st.error(f"Processing failed: {st.session_state['shwfs_error']}")

results = st.session_state.get("shwfs_results")

if results:
    st.markdown('<div class="panel-title">📊 &nbsp; Analysis Results (After Processing) <span class="pill" style="float:right;">✓ Processing completed</span></div>', unsafe_allow_html=True)

    def image_if_exists(path, caption=None):
        if path and Path(path).exists():
            st.image(str(path), caption=caption, use_container_width=True)
        else:
            st.info("Output image not found.")

    # Row 1: four visual analysis cards
    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        st.markdown('<div class="subcard"><h4>1 · Spot Centroid Detection</h4></div>', unsafe_allow_html=True)
        centroid_path = OUTPUT_DIR / "centroid_detection.png"
        image_if_exists(centroid_path, "Detected spot centroids")
        st.caption(f"Reference: {len(results['reference_centroids'])}  |  Current: {len(results['current_centroids'])}")
    with c2:
        st.markdown('<div class="subcard"><h4>2 · Spot Shift (Δx, Δy)</h4></div>', unsafe_allow_html=True)
        st.metric("Total spot shifts", len(results["spot_shifts"]))
        with st.expander("View spot shifts"):
            st.dataframe(pd.DataFrame(results["spot_shifts"]), use_container_width=True, hide_index=True)
    with c3:
        st.markdown('<div class="subcard"><h4>3 · Wavefront Slopes (Sx, Sy)</h4></div>', unsafe_allow_html=True)
        st.metric("Total slopes", len(results["slopes"]))
        with st.expander("View slopes"):
            st.dataframe(pd.DataFrame(results["slopes"]), use_container_width=True, hide_index=True)
    with c4:
        st.markdown('<div class="subcard"><h4>4 · Wavefront Reconstruction W(x,y)</h4></div>', unsafe_allow_html=True)
        image_if_exists(results.get("phase_map"), "Reconstructed wavefront")

    # Row 2: scientific outputs and simulation panels
    c5, c6, c7, c8 = st.columns(4, gap="small")
    with c5:
        st.markdown('<div class="subcard"><h4>5 · Zernike Coefficients</h4></div>', unsafe_allow_html=True)
        zernike_df = pd.DataFrame(
            [{"Mode": key, "Coefficient": float(value)} for key, value in results["zernike"].items()]
        )
        st.dataframe(zernike_df, use_container_width=True, hide_index=True)
    with c6:
        st.markdown('<div class="subcard"><h4>6 · Turbulence Parameters</h4></div>', unsafe_allow_html=True)
        st.metric("Fried parameter (r₀)", f"{results['r0']}")
        st.metric("Coherence time (τ₀)", f"{results['tau0']}")
        st.metric("Turbulence strength", f"{results['turbulence_strength']}")
        st.caption("Simplified estimates; physical validation requires calibrated sensor data.")
    with c7:
        st.markdown('<div class="subcard"><h4>7 · Actuator Map (DM Commands)</h4></div>', unsafe_allow_html=True)
        image_if_exists(results.get("actuator_map"), "Actuator command map")
    with c8:
        st.markdown('<div class="subcard"><h4>8 · Corrected Wavefront</h4></div>', unsafe_allow_html=True)
        image_if_exists(results.get("corrected_wavefront"), "Corrected wavefront simulation")

    st.markdown('<div class="panel-title">✅ &nbsp; Processing Summary</div>', unsafe_allow_html=True)
    st.success("SH-WFS processing pipeline executed successfully.")
    summary_cols = st.columns(4)
    for idx, label in enumerate(steps):
        with summary_cols[idx % 4]:
            st.markdown(f"✓ {label}")

elif not st.session_state.get("shwfs_error"):
    st.info("Upload both images above, then select **Process Images**. Results will appear here.")

st.markdown("---")
st.caption("SH-WFS Analysis System · Academic software prototype · Outputs are computational estimates and simulations, not validated instrument measurements.")
