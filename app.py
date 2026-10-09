import streamlit as st
import streamlit.components.v1 as components
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

# --- 5. 3D GALACTIC NEIGHBORHOOD MAP ---
st.divider()
st.subheader("🌌 3D Interactive Galactic Neighborhood (Local Bubble)")
st.write("Explore WISE 0855−0714 positioned in 3D interstellar space relative to the Sun and the nearest stellar systems within ~12 light-years. Rotate, zoom, and pan the interactive volume:")

local_stars = [
    {"name": "Sol (Sun / Earth Base)", "ra": 0.0, "dec": 0.0, "dist": 0.0, "type": "G2V Star", "color": "#FFD700", "size": 12},
    {"name": "WISE 0855−0714", "ra": 133.795, "dec": -7.245, "dist": 7.43, "type": "Y2 Sub-Brown Dwarf", "color": "#00FFCC", "size": 14},
    {"name": "Alpha Centauri A/B", "ra": 219.90, "dec": -60.83, "dist": 4.37, "type": "G2V / K1V Binary", "color": "#FFA726", "size": 9},
    {"name": "Proxima Centauri", "ra": 217.43, "dec": -62.68, "dist": 4.24, "type": "M5.5V Red Dwarf", "color": "#FF5252", "size": 7},
    {"name": "Barnard's Star", "ra": 269.45, "dec": 4.69, "dist": 5.96, "type": "M4.0V Red Dwarf", "color": "#FF5252", "size": 7},
    {"name": "Luhman 16 A/B", "ra": 162.33, "dec": -53.32, "dist": 6.51, "type": "L7.5 / T0.5 Brown Dwarf Pair", "color": "#CE93D8", "size": 9},
    {"name": "Wolf 359", "ra": 164.12, "dec": 7.01, "dist": 7.86, "type": "M6.0V Red Dwarf", "color": "#FF5252", "size": 7},
    {"name": "Lalande 21185", "ra": 165.83, "dec": 35.97, "dist": 8.31, "type": "M2.0V Red Dwarf", "color": "#FF5252", "size": 7},
    {"name": "Sirius A/B", "ra": 101.28, "dec": -16.72, "dist": 8.66, "type": "A1V / DA2 Binary", "color": "#E0F7FA", "size": 11},
    {"name": "Luyten 726-8", "ra": 24.75, "dec": -17.95, "dist": 8.73, "type": "M5.5V Flare Star Pair", "color": "#FF7043", "size": 7},
    {"name": "Ross 154", "ra": 282.46, "dec": -23.83, "dist": 9.70, "type": "M3.5V Red Dwarf", "color": "#FF5252", "size": 7},
    {"name": "Epsilon Eridani", "ra": 53.23, "dec": -9.46, "dist": 10.47, "type": "K2V Orange Dwarf", "color": "#FFCA28", "size": 9}
]

star_x, star_y, star_z, star_color, star_size, star_hover, star_labels = [], [], [], [], [], [], []
wise_pos = (0.0, 0.0, 0.0)

for s in local_stars:
    ra_r = np.radians(s["ra"])
    dec_r = np.radians(s["dec"])
    x = float(s["dist"] * np.cos(dec_r) * np.cos(ra_r))
    y = float(s["dist"] * np.cos(dec_r) * np.sin(ra_r))
    z = float(s["dist"] * np.sin(dec_r))
    if "WISE" in s["name"]:
        wise_pos = (x, y, z)
    star_x.append(x)
    star_y.append(y)
    star_z.append(z)
    star_color.append(s["color"])
    star_size.append(s["size"])
    star_labels.append(s["name"])

for i, s in enumerate(local_stars):
    d_to_wise = np.sqrt((star_x[i] - wise_pos[0])**2 + (star_y[i] - wise_pos[1])**2 + (star_z[i] - wise_pos[2])**2)
    star_hover.append(
        f"<b>{s['name']}</b><br>"
        f"Type: {s['type']}<br>"
        f"Dist from Sol: {s['dist']} ly<br>"
        f"Dist to WISE 0855: {d_to_wise:.2f} ly<br>"
        f"Coordinates: ({star_x[i]:.2f}, {star_y[i]:.2f}, {star_z[i]:.2f}) ly"
    )

fig_3d = go.Figure()

# Concentric range rings in the XY plane
angles = np.linspace(0, 2 * np.pi, 100)
for radius, dash_col in [(5, "rgba(0, 255, 204, 0.22)"), (10, "rgba(0, 255, 204, 0.12)")]:
    fig_3d.add_trace(go.Scatter3d(
        x=radius * np.cos(angles),
        y=radius * np.sin(angles),
        z=np.zeros_like(angles),
        mode="lines",
        line=dict(color=dash_col, width=2, dash="dash"),
        hoverinfo="text",
        hovertext=f"{radius} Light-Year Equatorial Range Ring",
        showlegend=False
    ))

# Sol to WISE 0855 baseline vector line
fig_3d.add_trace(go.Scatter3d(
    x=[0, wise_pos[0]],
    y=[0, wise_pos[1]],
    z=[0, wise_pos[2]],
    mode="lines+text",
    line=dict(color="#00FFCC", width=4),
    text=["", "  Baseline Vector (7.43 ly)"],
    textposition="middle right",
    textfont=dict(color="#00FFCC", size=11, family="Courier New"),
    hoverinfo="none",
    name="Baseline Vector"
))

# Outer neon glow sphere for WISE 0855
fig_3d.add_trace(go.Scatter3d(
    x=[wise_pos[0]],
    y=[wise_pos[1]],
    z=[wise_pos[2]],
    mode="markers",
    marker=dict(size=26, color="rgba(0, 255, 204, 0.3)", symbol="circle"),
    hoverinfo="none",
    showlegend=False
))

# Main stellar systems trace
fig_3d.add_trace(go.Scatter3d(
    x=star_x,
    y=star_y,
    z=star_z,
    mode="markers+text",
    marker=dict(size=star_size, color=star_color, line=dict(color="white", width=1)),
    text=star_labels,
    textposition="top center",
    textfont=dict(color="#E0E6ED", size=10, family="Courier New"),
    hoverinfo="text",
    hovertext=star_hover,
    name="Local Stellar Systems"
))

fig_3d.update_layout(
    scene=dict(
        bgcolor="#0B0E14",
        xaxis=dict(
            title="X (Light-Years)",
            backgroundcolor="#0B0E14",
            gridcolor="rgba(0, 255, 204, 0.12)",
            showbackground=True,
            zerolinecolor="rgba(0, 255, 204, 0.25)",
            tickfont=dict(color="#8F9CAE", family="Courier New")
        ),
        yaxis=dict(
            title="Y (Light-Years)",
            backgroundcolor="#0B0E14",
            gridcolor="rgba(0, 255, 204, 0.12)",
            showbackground=True,
            zerolinecolor="rgba(0, 255, 204, 0.25)",
            tickfont=dict(color="#8F9CAE", family="Courier New")
        ),
        zaxis=dict(
            title="Z (Light-Years)",
            backgroundcolor="#0B0E14",
            gridcolor="rgba(0, 255, 204, 0.12)",
            showbackground=True,
            zerolinecolor="rgba(0, 255, 204, 0.25)",
            tickfont=dict(color="#8F9CAE", family="Courier New")
        ),
        camera=dict(
            eye=dict(x=1.35, y=1.35, z=0.85)
        )
    ),
    paper_bgcolor="#0B0E14",
    plot_bgcolor="#0B0E14",
    font=dict(color="#E0E6ED"),
    height=600,
    margin=dict(l=20, r=20, t=30, b=20),
    showlegend=False
)

st.plotly_chart(fig_3d, use_container_width=True)

# --- 6. PROPER MOTION TIME-MACHINE (NATIVE PLOTLY ANIMATION) ---
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
# --- 7. REAL-TIME ASTRONOMICAL IMAGE CUTOUT ---
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

# --- 8. ATMOSPHERIC CHEMICAL FINGERPRINT ---
st.divider()
st.subheader("🧪 Atmospheric Chemical Fingerprint")
st.write("Relative spectroscopic molecular absorption profile across key atmospheric constituents:")

chem_species = ['Water Ice (H₂O)', 'Methane (CH₄)', 'Ammonia (NH₃)', 'CO', 'N₂']
absorption_levels = [92, 78, 54, 35, 18]

# Close the radar loop
theta_radar = chem_species + [chem_species[0]]
r_radar = absorption_levels + [absorption_levels[0]]

fig_chem = go.Figure()

fig_chem.add_trace(go.Scatterpolar(
    r=r_radar,
    theta=theta_radar,
    fill='toself',
    fillcolor='rgba(0, 255, 204, 0.25)',
    line=dict(color='#00FFCC', width=3),
    marker=dict(color='#00FFCC', size=9, symbol='circle', line=dict(color='#FFFFFF', width=1)),
    hovertemplate='<b>%{theta}</b><br>Absorption: %{r}%<extra></extra>',
    name='Chemical Fingerprint'
))

fig_chem.update_layout(
    polar=dict(
        bgcolor='#0B0E14',
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            ticksuffix='%',
            tickfont=dict(color='#8F9CAE', size=11, family='Courier New'),
            gridcolor='rgba(0, 255, 204, 0.15)',
            linecolor='rgba(0, 255, 204, 0.25)',
            showticklabels=True
        ),
        angularaxis=dict(
            tickfont=dict(color='#E0E6ED', size=13, family='Courier New'),
            gridcolor='rgba(0, 255, 204, 0.15)',
            linecolor='rgba(0, 255, 204, 0.25)'
        )
    ),
    paper_bgcolor='#0B0E14',
    plot_bgcolor='#0B0E14',
    font=dict(color='#E0E6ED'),
    height=480,
    margin=dict(l=70, r=70, t=50, b=50),
    showlegend=False
)

st.plotly_chart(fig_chem, use_container_width=True)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Water Ice (H₂O)", "92%", "Deep cloud deck")
col2.metric("Methane (CH₄)", "78%", "Strong band")
col3.metric("Ammonia (NH₃)", "54%", "Moderate signature")
col4.metric("CO", "35%", "Disequilibrium")
col5.metric("N₂", "18%", "Background trace")

# --- 9. DEEP SPACE RADIO BEACON & AUDIO SYNTHESIZER ---
st.divider()
st.subheader("📻 Deep Space Radio Beacon & Audio Synthesizer")
st.write("Trigger an acoustic telemetry transmission via Web Audio API. Synthesizes a high-frequency chirp signal and listens for simulated interstellar echo:")

synth_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {
        margin: 0;
        padding: 10px;
        background-color: #0B0E14;
        font-family: 'Courier New', Courier, monospace;
        color: #E0E6ED;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .panel {
        width: 100%;
        max-width: 720px;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(0, 255, 204, 0.35);
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.12), inset 0 0 15px rgba(0, 255, 204, 0.05);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        box-sizing: border-box;
    }
    .btn-chirp {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.2) 0%, rgba(11, 14, 20, 0.95) 100%);
        color: #00FFCC;
        border: 2px solid #00FFCC;
        border-radius: 6px;
        padding: 13px 26px;
        font-size: 14px;
        font-weight: 700;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 0 14px rgba(0, 255, 204, 0.35), inset 0 0 10px rgba(0, 255, 204, 0.15);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .btn-chirp:hover {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.35) 0%, rgba(11, 14, 20, 0.9) 100%);
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.7), inset 0 0 18px rgba(0, 255, 204, 0.3);
        transform: translateY(-1px);
        color: #FFFFFF;
    }
    .btn-chirp:active {
        transform: translateY(1px) scale(0.98);
        box-shadow: 0 0 35px #00FFCC, inset 0 0 25px #00FFCC;
    }
    .hud-status {
        font-size: 12px;
        color: #8F9CAE;
        letter-spacing: 1px;
        text-align: center;
    }
    .hud-status span {
        color: #00FFCC;
        font-weight: bold;
    }
    .visualizer {
        display: flex;
        gap: 4px;
        align-items: flex-end;
        height: 18px;
    }
    .bar {
        width: 4px;
        height: 4px;
        background: #00FFCC;
        border-radius: 2px;
        transition: height 0.1s ease;
        opacity: 0.3;
        box-shadow: 0 0 6px rgba(0, 255, 204, 0.5);
    }
    .bar.active {
        opacity: 1;
        animation: pulseBar 0.35s infinite alternate ease-in-out;
    }
    @keyframes pulseBar {
        0% { height: 4px; }
        100% { height: 18px; }
    }
</style>
</head>
<body>
<div class="panel">
    <button class="btn-chirp" id="chirpBtn" onclick="triggerSpaceChirp()">
        <span>📡</span> TRANSMIT DEEP SPACE CHIRP SIGNAL
    </button>
    
    <div class="visualizer" id="visualizer">
        <div class="bar" style="animation-delay: 0.05s"></div>
        <div class="bar" style="animation-delay: 0.15s"></div>
        <div class="bar" style="animation-delay: 0.25s"></div>
        <div class="bar" style="animation-delay: 0.10s"></div>
        <div class="bar" style="animation-delay: 0.30s"></div>
        <div class="bar" style="animation-delay: 0.20s"></div>
        <div class="bar" style="animation-delay: 0.05s"></div>
        <div class="bar" style="animation-delay: 0.18s"></div>
    </div>
    
    <div class="hud-status" id="hudStatus">
        BEACON: <span>ARMED & READY</span> // CARRIER: <span>4.80 GHz SYNTH</span> // TARGET: <span>WISE 0855−0714</span>
    </div>
</div>

<script>
let audioCtx = null;

function triggerSpaceChirp() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!audioCtx) {
            audioCtx = new AudioContext();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }

        const now = audioCtx.currentTime;
        const masterGain = audioCtx.createGain();
        masterGain.gain.setValueAtTime(0.5, now);
        masterGain.connect(audioCtx.destination);

        // 1. Primary Outbound Chirp: High-speed exponential upward sweep (380 Hz -> 3200 Hz)
        const osc1 = audioCtx.createOscillator();
        const gain1 = audioCtx.createGain();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(380, now);
        osc1.frequency.exponentialRampToValueAtTime(3200, now + 0.30);

        gain1.gain.setValueAtTime(0.001, now);
        gain1.gain.linearRampToValueAtTime(0.4, now + 0.03);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.34);

        osc1.connect(gain1);
        gain1.connect(masterGain);
        osc1.start(now);
        osc1.stop(now + 0.35);

        // 2. Harmonic Telemetry Overtone with Resonant Bandpass Filter
        const osc2 = audioCtx.createOscillator();
        const gain2 = audioCtx.createGain();
        const filter = audioCtx.createBiquadFilter();
        
        osc2.type = 'sawtooth';
        osc2.frequency.setValueAtTime(760, now);
        osc2.frequency.exponentialRampToValueAtTime(5400, now + 0.28);

        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(800, now);
        filter.frequency.exponentialRampToValueAtTime(3600, now + 0.30);
        filter.Q.setValueAtTime(6.0, now);

        gain2.gain.setValueAtTime(0.001, now);
        gain2.gain.linearRampToValueAtTime(0.12, now + 0.02);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.30);

        osc2.connect(filter);
        filter.connect(gain2);
        gain2.connect(masterGain);
        osc2.start(now);
        osc2.stop(now + 0.32);

        // 3. Simulated Echo Return from WISE 0855 at t + 0.42s
        const echoOsc = audioCtx.createOscillator();
        const echoGain = audioCtx.createGain();
        echoOsc.type = 'sine';
        echoOsc.frequency.setValueAtTime(1750, now + 0.42);
        echoOsc.frequency.exponentialRampToValueAtTime(520, now + 0.85);

        echoGain.gain.setValueAtTime(0.001, now + 0.42);
        echoGain.gain.linearRampToValueAtTime(0.28, now + 0.46);
        echoGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.95);

        echoOsc.connect(echoGain);
        echoGain.connect(masterGain);
        echoOsc.start(now + 0.42);
        echoOsc.stop(now + 1.0);

        // Visual HUD updates
        const hud = document.getElementById('hudStatus');
        const bars = document.querySelectorAll('.bar');
        bars.forEach(b => b.classList.add('active'));

        hud.innerHTML = 'STATUS: <span style="color:#FF3333">TRANSMITTING PULSE...</span> [4.8 GHz CHIRP SENT]';

        setTimeout(() => {
            hud.innerHTML = 'STATUS: <span style="color:#00FFCC">📡 INTERSTELLAR ECHO RECEIVED!</span> [SNR: +24.6 dB]';
        }, 440);

        setTimeout(() => {
            bars.forEach(b => b.classList.remove('active'));
            hud.innerHTML = 'BEACON: <span>ARMED & READY</span> // CARRIER: <span>4.80 GHz SYNTH</span> // TARGET: <span>WISE 0855−0714</span>';
        }, 1400);

    } catch (e) {
        console.error(e);
    }
}
</script>
</body>
</html>
"""

components.html(synth_html, height=175)

# --- 10. SIMULATED INFRARED FLUX STREAM ---
st.divider()
st.subheader("📡 Infrared Flux Data Stream")
st.write("Simulating real-time atmospheric anomaly detection...")

chart_placeholder = st.empty()
flux_data = []

for i in range(30):
    new_flux = 6.03e-8 + np.random.normal(0, 0.2e-8)
    flux_data.append(new_flux)
    chart_placeholder.line_chart(flux_data, height=200)
    time.sleep(0.08) # Slightly faster sweep!
