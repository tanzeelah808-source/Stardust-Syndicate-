import streamlit as st
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import time
from astro_api import fetch_infrared_cutout

# --- 1. PAGE SETUP & AUTOBLINKER CSS ---
st.set_page_config(page_title="Stardust Syndicate | Universe Monitor", layout="wide", page_icon="🔭")

# Custom CSS for the Autoblinker!
st.markdown("""
    <style>
    .blinker {
        animation: blinker 1.5s linear infinite;
        color: #FF3333;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    @keyframes blinker {
        50% { opacity: 0; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔭 Stardust Syndicate: WISE 0855−0714 Command Center")

# --- 2. TARGET COORDINATES ---
target_ra = 133.795   # 08h 55m 10.8s
target_dec = -7.245   # -07° 14′ 42.5″

# --- 3. TELEMETRY SIDEBAR (WITH AUTOBLINKER) ---
with st.sidebar:
    st.markdown('<div class="blinker">🔴 LIVE UPLINK ACTIVE</div>', unsafe_allow_html=True)
    st.header("🛰️ Live Telemetry")
    st.markdown("Target Locked: **WISE 0855−0714**")
    
    st.metric(label="Distance", value="7.43 Light-Years", delta="-0.04 ly uncertainty")
    st.metric(label="Surface Temperature", value="~276 K (3 °C)", delta="Water ice clouds detected")
    st.metric(label="Estimated Mass", value="3–10 M_Jup", delta="Sub-brown dwarf regime")
    st.metric(label="Right Ascension", value="08h 55m 10.8s")
    st.metric(label="Declination", value="−07° 14′ 42.5″")

# --- 4. INTERACTIVE SKY MAP (WIDE ANGLE TRACKING) ---
st.subheader("🗺️ Live Celestial Tracking Map (RA / Dec Field)")

np.random.seed(42)
num_stars = 150
star_ra = np.random.uniform(target_ra - 10, target_ra + 10, num_stars)
star_dec = np.random.uniform(target_dec - 10, target_dec + 10, num_stars)
star_sizes = np.random.uniform(2, 6, num_stars)

fig_main = go.Figure()

# Background Star Field
fig_main.add_trace(go.Scatter(
    x=star_ra, y=star_dec, mode='markers',
    marker=dict(size=star_sizes, color='white', opacity=0.7), name="Catalog Stars"
))

# Target Lock Reticle (Glow Ring)
fig_main.add_trace(go.Scatter(
    x=[target_ra], y=[target_dec], mode='markers',
    marker=dict(size=24, color='rgba(255, 50, 50, 0.3)', symbol='circle'),
    showlegend=False, hoverinfo="none"
))

# Target Center Crosshair
fig_main.add_trace(go.Scatter(
    x=[target_ra], y=[target_dec], mode='markers+text',
    marker=dict(size=12, color='#FF3333', symbol='cross', line=dict(width=2, color='white')),
    text=["  WISE 0855−0714"], textposition="middle right",
    textfont=dict(color="#FFD700", size=13, family="Courier New"), name="Locked Target"
))

fig_main.update_layout(
    xaxis=dict(title="Right Ascension (°)", range=[target_ra - 12, target_ra + 12], autorange="reversed", showgrid=True, gridcolor='rgba(255, 255, 255, 0.15)', zeroline=False),
    yaxis=dict(title="Declination (°)", range=[target_dec - 12, target_dec + 12], showgrid=True, gridcolor='rgba(255, 255, 255, 0.15)', zeroline=False),
    paper_bgcolor='#0B0E14', plot_bgcolor='#0B0E14', font=dict(color='#E0E6ED'),
    height=550, margin=dict(l=40, r=40, t=40, b=40)
)
st.plotly_chart(fig_main, use_container_width=True)
# --- 5. PROPER MOTION TIME-MACHINE (NATIVE PLOTLY ANIMATION) ---
st.divider()
st.subheader("⏱️ Proper Motion Time-Machine (Jump Loop)")
st.write("Set the fast-forward timeline, then click the button on the map to watch WISE 0855−0714 physically jump between current and future coordinates!")

# Controls
years_lapsed = st.slider("🕰️ Fast-Forward Target (Years)", min_value=1, max_value=100, value=15, step=1)

pm_ra_deg_yr = -0.00225 
pm_dec_deg_yr = 0.00019 

current_ra = target_ra + (pm_ra_deg_yr * years_lapsed)
current_dec = target_dec + (pm_dec_deg_yr * years_lapsed)

# Generate static background stars
np.random.seed(99)
pm_star_ra = np.random.uniform(target_ra - 0.1, target_ra + 0.1, 50)
pm_star_dec = np.random.uniform(target_dec - 0.1, target_dec + 0.1, 50)
pm_star_sizes = np.random.uniform(2, 5, 50)

# 1. Define individual traces
trace_stars = go.Scatter(
    x=pm_star_ra, 
    y=pm_star_dec, 
    mode='markers', 
    marker=dict(size=pm_star_sizes, color='white', opacity=0.4), 
    hoverinfo="none"
)

trace_ghost = go.Scatter(
    x=[target_ra], 
    y=[target_dec], 
    mode='markers', 
    marker=dict(size=12, color='rgba(255, 255, 255, 0.15)', symbol='cross'), 
    hoverinfo="none"
)

trace_current = go.Scatter(
    x=[target_ra], 
    y=[target_dec], 
    mode='markers+text',
    marker=dict(size=14, color='#00FFCC', symbol='cross-thin', line=dict(width=3, color='#00FFCC')),
    text=["  CURRENT (2026)"], 
    textposition="middle right",
    textfont=dict(color="#00FFCC", size=14, family="Courier New")
)

trace_future = go.Scatter(
    x=[current_ra], 
    y=[current_dec], 
    mode='markers+text',
    marker=dict(size=14, color='#00FFCC', symbol='cross-thin', line=dict(width=3, color='#00FFCC')),
    text=[f"  FUTURE (+{years_lapsed} YRS)"], 
    textposition="middle right",
    textfont=dict(color="#00FFCC", size=14, family="Courier New")
)

# 2. Define animation frames cleanly
frame_1 = go.Frame(data=[trace_stars, trace_ghost, trace_current], name="pos1")
frame_2 = go.Frame(data=[trace_stars, trace_ghost, trace_future], name="pos2")

# 3. Assemble figure
fig_pm = go.Figure(
    data=[trace_stars, trace_ghost, trace_current],
    frames=[frame_1, frame_2]
)

fig_pm.update_layout(
    xaxis=dict(
        title="Right Ascension (°)", 
        range=[target_ra - 0.25, target_ra + 0.05], 
        autorange="reversed", 
        showgrid=True, 
        gridcolor='rgba(255, 255, 255, 0.05)', 
        zeroline=False
    ),
    yaxis=dict(
        title="Declination (°)", 
        range=[target_dec - 0.05, target_dec + 0.05], 
        showgrid=True, 
        gridcolor='rgba(255, 255, 255, 0.05)', 
        zeroline=False
    ),
    paper_bgcolor='#0B0E14', 
    plot_bgcolor='#0B0E14', 
    font=dict(color='#E0E6ED'),
    height=450, 
    margin=dict(l=40, r=40, t=40, b=40), 
    showlegend=False,
    updatemenus=[
        dict(
            type="buttons", 
            showactive=False,
            y=1.05, 
            x=0.5, 
            xanchor="center", 
            yanchor="bottom",
            buttons=[
                dict(
                    label="🔴 ACTIVATE JUMP LOOP",
                    method="animate",
                    args=[
                        None, 
                        dict(
                            frame=dict(duration=800, redraw=True), 
                            transition=dict(duration=0), 
                            fromcurrent=True, 
                            mode="immediate", 
                            loop=True
                        )
                    ]
                )
            ]
        )
    ]
)

st.plotly_chart(fig_pm, use_container_width=True)
# --- 6. REAL-TIME ASTRONOMICAL IMAGE CUTOUT ---
st.subheader("📸 Deep Space Infrared Cutout")

@st.cache_data(show_spinner=False)
def get_cached_image(ra, dec):
    return fetch_infrared_cutout(ra, dec)

try:
    with st.spinner("Establishing uplink to SkyView archives..."):
        img_data = get_cached_image(target_ra, target_dec)
        
    fig_img, ax = plt.subplots()
    fig_img.patch.set_facecolor('#0B0E14') 
    ax.imshow(img_data, cmap='magma', origin='lower')
    ax.axis('off') 
    st.pyplot(fig_img, use_container_width=False)
except Exception as e:
    st.error(f"⚠️ Telemetry Uplink Failed: {e}")

# --- 7. SIMULATED INFRARED FLUX STREAM ---
st.subheader("📡 Infrared Flux Data Stream")
st.write("Simulating real-time atmospheric anomaly detection...")

chart_placeholder = st.empty()
flux_data = []

for i in range(30):
    new_flux = 6.03e-8 + np.random.normal(0, 0.2e-8)
    flux_data.append(new_flux)
    chart_placeholder.line_chart(flux_data, height=200)
    time.sleep(0.08) # Slightly faster sweep!