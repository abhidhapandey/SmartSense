
import csv
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ---------------- CONFIGURATION ----------------
CSV_FILE = Path(__file__).parent / "sensor_readings.csv"
TEMP_LIMIT = 70
VIBRATION_LIMIT = 5

st.set_page_config(
    page_title="SmartSense | Industrial Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- VISUAL DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { color-scheme: dark; }
.stApp {
    background:
      radial-gradient(ellipse at 8% 0%, rgba(14,165,233,.12), transparent 34%),
      radial-gradient(ellipse at 95% 10%, rgba(99,102,241,.09), transparent 28%),
      #07111f;
    color: #e6edf7;
    font-family: 'Manrope', sans-serif;
}
[data-testid="stHeader"] { background: rgba(7,17,31,.72); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c192a 0%, #081321 100%);
    border-right: 1px solid #203149;
}
.block-container { padding-top: 1.7rem; padding-bottom: 2.5rem; max-width: 1500px; }
h1,h2,h3 { letter-spacing: -.035em; }
.hero {
    border: 1px solid #203750; border-radius: 22px; padding: 24px 28px;
    background: linear-gradient(115deg, rgba(15,35,56,.96), rgba(10,22,38,.88));
    box-shadow: 0 18px 55px rgba(0,0,0,.18); margin-bottom: 22px;
}
.eyebrow { color:#51d7ef; text-transform:uppercase; letter-spacing:.18em; font-size:.72rem; font-weight:800; }
.hero-title { font-size:2.25rem; line-height:1.15; font-weight:800; margin:.35rem 0; color:#f2f7ff; }
.hero-sub { color:#91a8c3; font-size:.95rem; }
.pill {
    display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px;
    background:#0c2b2c; color:#5ee7b7; border:1px solid #1b5b53; font-size:.75rem; font-weight:800;
}
.dot { width:7px; height:7px; border-radius:50%; background:#34d399; display:inline-block; box-shadow:0 0 12px #34d399; }
.kpi {
    background:linear-gradient(145deg, rgba(18,35,55,.98), rgba(12,25,42,.98));
    border:1px solid #243b54; border-radius:18px; padding:18px 20px; min-height:150px;
    box-shadow:0 12px 28px rgba(0,0,0,.13); transition:transform .18s ease,border-color .18s ease;
}
.kpi:hover { transform:translateY(-3px); border-color:#3e91aa; }
.kpi-top { display:flex; justify-content:space-between; align-items:center; color:#9db1c9; font-size:.82rem; font-weight:700; }
.kpi-icon { width:34px; height:34px; display:grid; place-items:center; border-radius:11px; background:#12334a; color:#67e8f9; font-size:1.1rem; }
.kpi-value { color:#f3f7ff; font-size:2rem; font-weight:800; letter-spacing:-.06em; margin-top:13px; line-height:1.15; }
.kpi-foot { color:#829ab5; font-size:.76rem; margin-top:9px; }
.section-head { display:flex; align-items:center; gap:10px; margin: 1.2rem 0 .7rem; color:#eaf2fc; font-weight:800; font-size:1.15rem; }
.section-mark { width:4px; height:21px; border-radius:6px; background:#43d5ed; display:inline-block; }
.panel {
    background:linear-gradient(145deg, rgba(15,29,47,.97), rgba(10,22,37,.97));
    border:1px solid #20344b; border-radius:18px; padding:18px 20px; margin-bottom:10px;
}
.small-label { color:#8ea5bf; text-transform:uppercase; font-size:.7rem; letter-spacing:.13em; font-weight:800; }
.status-ok { color:#6ee7b7; background:#0b302b; border:1px solid #1b6655; padding:10px 13px; border-radius:12px; font-weight:800; }
.status-warn { color:#fbbf24; background:#382a10; border:1px solid #805a18; padding:10px 13px; border-radius:12px; font-weight:800; }
.status-bad { color:#fda4af; background:#3c1723; border:1px solid #813047; padding:10px 13px; border-radius:12px; font-weight:800; }
.alert-row { border:1px solid #263b52; border-left:4px solid #f59e0b; border-radius:12px; padding:12px 14px; background:#101f31; margin-bottom:9px; }
.alert-critical { border-left-color:#fb7185; }
.alert-ok { border-left-color:#34d399; }
div[data-testid="stMetric"] { background:#102036; border:1px solid #243b54; padding:14px 16px; border-radius:15px; }
div[data-testid="stMetricLabel"] { color:#9db1c9; }
div[data-testid="stMetricValue"] { color:#f3f7ff; }
.stButton > button, .stDownloadButton > button {
    border-radius:11px; border:1px solid #2a536c; background:#103149; color:#dffaff; font-weight:800;
}
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#55d8ef; color:white; background:#16415b; }
div[data-testid="stDataFrame"] { border:1px solid #203750; border-radius:12px; overflow:hidden; }
hr { border-color:#21344a; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA LOADING & CLEANING ----------------
@st.cache_data
def load_data(file_path: str, modified_time: int):
    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))
    return rows

def determine_status(row):
    if pd.isna(row["Temperature_C"]) or pd.isna(row["Vibration_mm_s"]):
        return "INSUFFICIENT DATA"
    warnings = []
    if row["Temperature_C"] > TEMP_LIMIT:
        warnings.append("HIGH TEMPERATURE")
    if row["Vibration_mm_s"] > VIBRATION_LIMIT:
        warnings.append("HIGH VIBRATION")
    return " | ".join(warnings) if warnings else "WITHIN DEMO LIMITS"

if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:
    st.markdown('<div class="hero"><div class="eyebrow">Industrial intelligence platform</div><div class="hero-title">SmartSense</div><div class="hero-sub">Your monitoring workspace is ready. Generate readings to begin.</div></div>', unsafe_allow_html=True)
    st.warning("No sensor data found. Run `python main.py` first, then refresh this page.")
    st.stop()

try:
    records = load_data(str(CSV_FILE), CSV_FILE.stat().st_mtime_ns)
    df = pd.DataFrame(records)
except (OSError, csv.Error, pd.errors.ParserError) as error:
    st.error(f"Could not read sensor history: {error}")
    st.stop()

if df.empty:
    st.warning("The CSV contains no sensor readings.")
    st.stop()

# Keep only the canonical schema. Extra/duplicate/blank CSV columns are ignored.
canonical = ["Timestamp", "Temperature_C", "Vibration_mm_s", "Current_A", "Status"]
for column in canonical:
    if column not in df.columns:
        df[column] = None
df = df[canonical].copy()

numeric_columns = ["Temperature_C", "Vibration_mm_s", "Current_A"]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

missing_status = df["Status"].isna() | df["Status"].astype(str).str.strip().eq("")
df.loc[missing_status, "Status"] = df.loc[missing_status].apply(determine_status, axis=1)
df["Status"] = df["Status"].fillna("INSUFFICIENT DATA").astype(str).str.strip()
df = df.dropna(subset=numeric_columns, how="all").copy()
if df.empty:
    st.warning("No valid numeric sensor readings were found.")
    st.stop()

df["Reading"] = range(1, len(df) + 1)
df["Alert"] = df["Status"].str.contains("HIGH", case=False, na=False)
df["Machine State"] = df["Status"].apply(
    lambda s: "ALERT" if "HIGH" in s else ("CHECK DATA" if "INSUFFICIENT" in s else "NORMAL")
)

# ---------------- SIDEBAR CONTROLS ----------------
with st.sidebar:
    st.markdown("## 🏭 SmartSense")
    st.caption("INDUSTRIAL MONITORING SIMULATOR")
    st.divider()
    st.markdown("### Workspace")
    view = st.radio("Navigate", ["Overview", "Sensor analytics", "Alert center", "Data explorer"], label_visibility="collapsed")
    st.divider()
    st.markdown("### Filters")
    sensor_choice = st.selectbox("Primary sensor", ["All sensors", "Temperature", "Vibration", "Current"])
    status_choice = st.selectbox("Machine status", ["All readings", "Alerts only", "Normal only"])
    time_choice = st.selectbox("Time window", ["All available", "Last 5 readings", "Last 10 readings", "Last 25 readings"])
    st.divider()
    st.markdown("### Demo thresholds")
    st.markdown(f"🌡️ **Temperature:** {TEMP_LIMIT} °C")
    st.markdown(f"〰️ **Vibration:** {VIBRATION_LIMIT} mm/s")
    st.caption("Thresholds are illustrative, not certified safety limits.")
    if st.button("↻ Refresh sensor data", width="stretch"):
        st.cache_data.clear()
        st.rerun()

filtered = df.copy()
if time_choice != "All available":
    n = int(time_choice.split()[1])
    filtered = filtered.tail(n)
if status_choice == "Alerts only":
    filtered = filtered[filtered["Alert"]]
elif status_choice == "Normal only":
    filtered = filtered[~filtered["Alert"]]

latest = df.iloc[-1]
latest_status = str(latest["Status"])
has_alert = "HIGH" in latest_status
alert_count = int(df["Alert"].sum())
normal_count = int((~df["Alert"]).sum())
latest_temp = latest["Temperature_C"]
latest_vib = latest["Vibration_mm_s"]
latest_current = latest["Current_A"]

def fmt(value, suffix):
    return f"{value:.1f}{suffix}" if pd.notna(value) else "N/A"

# ---------------- HERO HEADER ----------------
status_class = "status-warn" if has_alert else "status-ok"
status_label = "ATTENTION REQUIRED" if has_alert else "SYSTEM NOMINAL"
st.markdown(f"""
<div class="hero">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:18px;flex-wrap:wrap;">
    <div>
      <div class="eyebrow">Industrial intelligence platform · Demo environment</div>
      <div class="hero-title">SmartSense <span style="color:#49d7ef">/</span> Command Center</div>
      <div class="hero-sub">A clear view of simulated machine health, sensor trends, and operational alerts.</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:10px;">
      <div class="pill"><span class="dot"></span> SIMULATION ACTIVE</div>
      <div class="{status_class}">{'⚠' if has_alert else '✓'} {status_label}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------- KPI CARDS ----------------
st.markdown('<div class="section-head"><span class="section-mark"></span> Live snapshot <span style="color:#7189a5;font-size:.78rem;font-weight:500">· latest recorded sample</span></div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

def kpi_card(container, icon, label, value, foot, accent="#67e8f9"):
    container.markdown(f"""
    <div class="kpi">
      <div class="kpi-top"><span>{label}</span><span class="kpi-icon" style="color:{accent}">{icon}</span></div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-foot">{foot}</div>
    </div>""", unsafe_allow_html=True)

kpi_card(k1, "🌡", "TEMPERATURE", fmt(latest_temp, " °C"), f"Demo threshold · {TEMP_LIMIT} °C", "#fbbf24")
kpi_card(k2, "〰", "VIBRATION", fmt(latest_vib, " mm/s"), f"Demo threshold · {VIBRATION_LIMIT} mm/s", "#67e8f9")
kpi_card(k3, "ϟ", "ELECTRICAL CURRENT", fmt(latest_current, " A"), "Latest simulated reading", "#c4b5fd")
kpi_card(k4, "◈", "ALERT EVENTS", str(alert_count), f"{normal_count} non-alert readings recorded", "#fb7185")

st.markdown("")

# ---------------- PLOTLY HELPERS ----------------
plot_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Manrope, sans-serif", color="#c5d4e7", size=11),
    margin=dict(l=12, r=12, t=42, b=12),
    xaxis=dict(showgrid=False, zeroline=False, color="#829ab5", linecolor="#25394f"),
    yaxis=dict(showgrid=True, gridcolor="rgba(125,155,190,.13)", zeroline=False, color="#829ab5"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    hoverlabel=dict(bgcolor="#10243a", bordercolor="#3d718e", font_color="#f2f7ff"),
)
def sensor_figure(data, column, title, color, threshold=None, unit=""):
    fig = go.Figure()
    x = data["Timestamp"] if data["Timestamp"].notna().any() else data["Reading"]
    fig.add_trace(go.Scatter(
        x=x, y=data[column], mode="lines+markers", name=title,
        line=dict(color=color, width=3, shape="spline"),
        marker=dict(size=6, color=color, line=dict(width=1, color="#07111f")),
        connectgaps=False,
        hovertemplate=f"<b>{title}</b><br>%{{x}}<br>%{{y:.2f}} {unit}<extra></extra>",
    ))
    if threshold is not None:
        fig.add_hline(y=threshold, line_dash="dash", line_color="#f59e0b", line_width=1.5,
                      annotation_text=f"Demo limit · {threshold}", annotation_position="top left",
                      annotation_font_color="#fbbf24")
    fig.update_layout(**plot_layout, title=dict(text=title, font=dict(size=15, color="#eaf2fc")), height=310)
    fig.update_yaxes(title_text=unit)
    fig.update_xaxes(title_text="Timestamp" if data["Timestamp"].notna().any() else "Reading")
    return fig

def show_chart(fig, key):
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False, "scrollZoom": True}, key=key)

# ---------------- OVERVIEW ----------------
if view == "Overview":
    left, right = st.columns([1.6, 1])
    with left:
        st.markdown('<div class="section-head"><span class="section-mark"></span> Sensor telemetry</div>', unsafe_allow_html=True)
        chart_data = filtered.copy()
        if chart_data.empty:
            st.info("No readings match the selected filters.")
        else:
            selected = ["Temperature_C", "Vibration_mm_s", "Current_A"] if sensor_choice == "All sensors" else [{
                "Temperature": "Temperature_C", "Vibration": "Vibration_mm_s", "Current": "Current_A"
            }[sensor_choice]]
            if len(selected) == 1:
                col = selected[0]
                config = {
                    "Temperature_C": ("Temperature", "#fbbf24", TEMP_LIMIT, "°C"),
                    "Vibration_mm_s": ("Vibration", "#4dd8ef", VIBRATION_LIMIT, "mm/s"),
                    "Current_A": ("Electrical current", "#b8a3ff", None, "A"),
                }[col]
                show_chart(sensor_figure(chart_data, col, config[0], config[1], config[2], config[3]), "overview_single")
            else:
                fig = go.Figure()
                for col, name, color in [
                    ("Temperature_C", "Temperature (°C)", "#fbbf24"),
                    ("Vibration_mm_s", "Vibration (mm/s)", "#4dd8ef"),
                    ("Current_A", "Current (A)", "#b8a3ff"),
                ]:
                    fig.add_trace(go.Scatter(x=chart_data["Timestamp"] if chart_data["Timestamp"].notna().any() else chart_data["Reading"],
                        y=chart_data[col], mode="lines+markers", name=name, line=dict(color=color, width=2.5),
                        marker=dict(size=5), connectgaps=False))
                fig.update_layout(**plot_layout, title="Multi-sensor overview · native units", height=310)
                show_chart(fig, "overview_multi")
                st.caption("Each sensor retains its native unit. Select one sensor for a focused view with its threshold line.")
    with right:
        st.markdown('<div class="section-head"><span class="section-mark"></span> Machine health</div>', unsafe_allow_html=True)
        gauge_value = 100 if not has_alert else max(15, 100 - 25 * latest_status.count("HIGH"))
        gauge_color = "#34d399" if not has_alert else "#fb7185"
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=gauge_value, number={"suffix":"%", "font":{"size":35, "color":"#f3f7ff"}},
            title={"text":"DEMO HEALTH INDEX", "font":{"size":12, "color":"#91a8c3"}},
            gauge={"axis":{"range":[0,100], "tickwidth":1, "tickcolor":"#50647d"},
                   "bar":{"color":gauge_color, "thickness":.28}, "bgcolor":"#102036",
                   "borderwidth":0, "steps":[{"range":[0,40],"color":"#351d2b"},{"range":[40,70],"color":"#392e19"},{"range":[70,100],"color":"#12342f"}],
                   "threshold":{"line":{"color":"#f3f7ff","width":3},"thickness":.8,"value":gauge_value}}
        ))
        gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#c5d4e7", height=250, margin=dict(l=20,r=20,t=45,b=8))
        show_chart(gauge, "health_gauge")
        if has_alert:
            st.markdown(f'<div class="status-warn">⚠ {latest_status}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-ok">✓ All latest readings within demo limits</div>', unsafe_allow_html=True)
        st.caption("Health index is a simple demonstration indicator, not a validated industrial health score.")

    st.markdown('<div class="section-head"><span class="section-mark"></span> Recent events</div>', unsafe_allow_html=True)
    recent = df.tail(5).iloc[::-1]
    if recent.empty:
        st.caption("No recent events.")
    for _, row in recent.iterrows():
        ts = row["Timestamp"].strftime("%Y-%m-%d %H:%M:%S") if pd.notna(row["Timestamp"]) else f"Reading #{row['Reading']}"
        is_alert = "HIGH" in str(row["Status"])
        row_class = "alert-critical" if is_alert else "alert-ok"
        symbol = "⚠" if is_alert else "✓"
        st.markdown(f'<div class="alert-row {row_class}"><div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;"><strong>{symbol} {row["Status"]}</strong><span style="color:#829ab5;font-size:.8rem">{ts}</span></div><div style="color:#9db1c9;font-size:.82rem;margin-top:6px">Temp: {fmt(row["Temperature_C"], " °C")} &nbsp;·&nbsp; Vibration: {fmt(row["Vibration_mm_s"], " mm/s")} &nbsp;·&nbsp; Current: {fmt(row["Current_A"], " A")}</div></div>', unsafe_allow_html=True)

# ---------------- SENSOR ANALYTICS ----------------
elif view == "Sensor analytics":
    st.markdown('<div class="section-head"><span class="section-mark"></span> Deep-dive analytics</div>', unsafe_allow_html=True)
    if filtered.empty:
        st.info("No readings match the selected filters.")
    else:
        a, b = st.columns(2)
        with a:
            show_chart(sensor_figure(filtered, "Temperature_C", "Temperature over time", "#fbbf24", TEMP_LIMIT, "°C"), "analytics_temp")
            show_chart(sensor_figure(filtered, "Current_A", "Electrical current over time", "#b8a3ff", None, "A"), "analytics_current")
        with b:
            show_chart(sensor_figure(filtered, "Vibration_mm_s", "Vibration over time", "#4dd8ef", VIBRATION_LIMIT, "mm/s"), "analytics_vibration")
            counts = filtered["Machine State"].value_counts().rename_axis("State").reset_index(name="Count")
            pie = px.pie(counts, names="State", values="Count", hole=.68, title="Reading status distribution",
                         color="State", color_discrete_map={"NORMAL":"#34d399","ALERT":"#fb7185","CHECK DATA":"#fbbf24"})
            pie.update_layout(**{**plot_layout, "height": 310, "legend": dict(orientation="h", y=-.1)})
            pie.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="#0b1726",width=3)))
            show_chart(pie, "status_distribution")
        st.markdown('<div class="section-head"><span class="section-mark"></span> Summary statistics</div>', unsafe_allow_html=True)
        stats = filtered[numeric_columns].agg(["mean", "min", "max"]).T.reset_index().rename(columns={"index":"Sensor", "mean":"Average", "min":"Minimum", "max":"Maximum"})
        stats["Sensor"] = stats["Sensor"].map({"Temperature_C":"Temperature (°C)","Vibration_mm_s":"Vibration (mm/s)","Current_A":"Current (A)"})
        st.dataframe(stats.round(2), width="stretch", hide_index=True)

# ---------------- ALERT CENTER ----------------
elif view == "Alert center":
    st.markdown('<div class="section-head"><span class="section-mark"></span> Alert center</div>', unsafe_allow_html=True)
    alerts = filtered[filtered["Alert"]].copy().iloc[::-1]
    m1, m2, m3 = st.columns(3)
    m1.metric("Total alerts in history", alert_count)
    m2.metric("Alerts in current filter", len(alerts))
    m3.metric("Latest machine state", "ALERT" if has_alert else "NORMAL")
    if alerts.empty:
        st.markdown('<div class="status-ok">✓ No alerts in the selected readings.</div>', unsafe_allow_html=True)
    else:
        for _, row in alerts.iterrows():
            ts = row["Timestamp"].strftime("%Y-%m-%d %H:%M:%S") if pd.notna(row["Timestamp"]) else f"Reading #{row['Reading']}"
            severity = "CRITICAL" if row["Status"].count("HIGH") > 1 else "WARNING"
            st.markdown(f'<div class="alert-row alert-critical"><div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;"><strong>🔴 {severity} · {row["Status"]}</strong><span style="color:#829ab5;font-size:.8rem">{ts}</span></div><div style="color:#b3c3d8;font-size:.86rem;margin-top:7px">Temperature: {fmt(row["Temperature_C"], " °C")} &nbsp;·&nbsp; Vibration: {fmt(row["Vibration_mm_s"], " mm/s")} &nbsp;·&nbsp; Current: {fmt(row["Current_A"], " A")}</div></div>', unsafe_allow_html=True)

# ---------------- DATA EXPLORER ----------------
elif view == "Data explorer":
    st.markdown('<div class="section-head"><span class="section-mark"></span> Sensor data explorer</div>', unsafe_allow_html=True)
    search = st.text_input("⌕ Search status or timestamp", placeholder="Try: HIGH VIBRATION, NORMAL, or a date…")
    table_df = filtered.copy()
    if search.strip():
        mask = table_df["Status"].str.contains(search.strip(), case=False, na=False)
        if table_df["Timestamp"].notna().any():
            mask = mask | table_df["Timestamp"].astype(str).str.contains(search.strip(), case=False, na=False)
        table_df = table_df[mask]
    table_df = table_df.iloc[::-1].copy()
    table_df["Timestamp"] = table_df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S").fillna("Unavailable")
    table_df = table_df.rename(columns={
        "Temperature_C":"Temperature (°C)", "Vibration_mm_s":"Vibration (mm/s)",
        "Current_A":"Current (A)", "Machine State":"Machine state"
    })
    visible_cols = ["Reading", "Timestamp", "Temperature (°C)", "Vibration (mm/s)", "Current (A)", "Status", "Machine state"]
    table_df = table_df[visible_cols]
    st.caption(f"{len(table_df)} readings shown · sorted newest first")
    st.dataframe(
        table_df, width="stretch", hide_index=True, height=420,
        column_config={
            "Reading": st.column_config.NumberColumn("Reading #", format="%d"),
            "Temperature (°C)": st.column_config.NumberColumn(format="%.2f"),
            "Vibration (mm/s)": st.column_config.NumberColumn(format="%.2f"),
            "Current (A)": st.column_config.NumberColumn(format="%.2f"),
            "Status": st.column_config.TextColumn("Status"),
        },
    )
    csv_data = table_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download filtered data (CSV)", data=csv_data, file_name="smartsense_filtered_readings.csv", mime="text/csv")
    st.caption("Legacy rows are normalized for display. The original CSV is not rewritten.")

# ---------------- FOOTER ----------------
st.divider()
foot1, foot2 = st.columns([2, 1])
with foot1:
    st.caption("SMARTSENSE · Industrial IoT Monitoring Simulator · Built with Python, Streamlit, Pandas & Plotly")
with foot2:
    st.caption(f"{len(df)} readings loaded · {datetime.now().strftime('%d %b %Y, %H:%M')} local app time")
st.caption("Simulation only. Thresholds are illustrative, not certified industrial safety limits. The health index is a demo visualization, not a validated safety assessment.")
