import streamlit as st
st.set_page_config(page_title="Karad Smart City Analytics", layout="wide")

import pandas as pd
import plotly.express as px
import os, time, io

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ================= CSS (REACT-LIKE FEEL) =================
st.markdown("""
<style>
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
    text-align: center;
}
.card:hover {
    transform: scale(1.03);
}
.nav {
    display: flex;
    gap: 25px;
    font-size: 18px;
    font-weight: 600;
}
.insight {
    background:#EFF6FF;
    padding:18px;
    border-left:6px solid #2563EB;
    border-radius:14px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
DATA_PATH = "data"
traffic = pd.read_csv(os.path.join(DATA_PATH, "traffic_accidents.csv"))
services = pd.read_csv(os.path.join(DATA_PATH, "public_services.csv"))
business = pd.read_csv(os.path.join(DATA_PATH, "businesses.csv"))
social = pd.read_csv(os.path.join(DATA_PATH, "social_indicators.csv"))

# ================= GLOBAL STATE =================
if "page" not in st.session_state:
    st.session_state.page = "Overview"

# ================= HERO =================
st.markdown("""
<div style="
background: linear-gradient(135deg,#2563EB,#1E3A8A);
padding:35px;
border-radius:22px;
color:white;
">
<h1>🏙️ Karad Smart City Analytics</h1>
<p style="font-size:18px;">
Interactive • Predictive • Decision-Driven Dashboard
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================= NAVBAR (REACT STYLE) =================
cols = st.columns(6)
pages = ["Overview", "Traffic", "Services", "Business", "Predictive", "What-If"]

for i, p in enumerate(pages):
    if cols[i].button(p, use_container_width=True):
        st.session_state.page = p
        st.toast(f"Switched to {p} 🚀")

page = st.session_state.page
st.markdown("<hr>", unsafe_allow_html=True)

# ================= COMPONENTS =================
def animated_kpi(title, value, icon):
    placeholder = st.empty()
    step = max(1, int(value/20)) if value > 0 else 1
    for i in range(0, int(value)+1, step):
        placeholder.markdown(f"""
        <div class="card">
            <h2>{icon} {i}</h2>
            <p style="color:#475569;">{title}</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.015)

def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>Karad Smart City Analytics Report</b>", styles["Title"]))
    content.append(Paragraph("<br/>", styles["Normal"]))
    content.append(Paragraph(f"Total Accidents: {len(traffic)}", styles["Normal"]))
    content.append(Paragraph(f"Total Businesses: {business['count'].sum()}", styles["Normal"]))
    content.append(Paragraph(
        f"Average Safety Index: {round(social['safety_index'].mean(),1)}",
        styles["Normal"]
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ======================================================
# 🏙️ OVERVIEW
# ======================================================
if page == "Overview":
    st.subheader("📌 City Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    with c1: animated_kpi("Total Accidents", len(traffic), "🚦")
    with c2: animated_kpi("Businesses", business["count"].sum(), "🏪")
    with c3: animated_kpi("Water Issues", services["water_issues"].sum(), "🚰")
    with c4: animated_kpi("Safety Index", round(social["safety_index"].mean(),1), "🛡️")

    acc = traffic.groupby("ward").size().reset_index(name="Accidents")
    fig = px.bar(acc, x="ward", y="Accidents")
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "⬇️ Download PDF Report",
        data=generate_pdf(),
        file_name="Karad_Smart_City_Report.pdf",
        mime="application/pdf"
    )

# ======================================================
# 🚦 TRAFFIC
# ======================================================
elif page == "Traffic":
    st.subheader("🚦 Traffic & Accident Patterns")

    chart_type = st.radio("View as", ["Bar", "Line"], horizontal=True)

    if chart_type == "Bar":
        fig = px.histogram(traffic, x="hour")
    else:
        fig = px.line(traffic.groupby("hour").size().reset_index(name="count"),
                      x="hour", y="count")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> Accident frequency spikes between 6–10 PM.
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# 🚰 SERVICES
# ======================================================
elif page == "Services":
    st.subheader("🚰 Public Services Performance")

    show = st.toggle("Show Detailed Chart")

    if show:
        fig = px.bar(services, x="ward", y="water_issues")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Toggle ON to load chart")

# ======================================================
# 🏪 BUSINESS
# ======================================================
elif page == "Business":
    st.subheader("🏪 Local Business Intelligence")

    category = st.selectbox(
        "Filter by Business Type",
        ["All"] + sorted(business["business_type"].unique())
    )

    df = business if category == "All" else business[business["business_type"] == category]

    fig = px.bar(df, x="ward", y="count", color="business_type")
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 📈 PREDICTIVE
# ======================================================
elif page == "Predictive":
    st.subheader("📈 Predictive & Prescriptive Insights")

    st.success("🔮 Accident risk increases with traffic density and poor weather.")
    st.warning("⚠️ High-risk wards require enforcement & infrastructure upgrades.")

# ======================================================
# 🧪 WHAT-IF
# ======================================================
elif page == "What-If":
    st.subheader("🧪 What-If Accident Risk Simulation")

    traffic_level = st.slider("Traffic Density", 1, 10, 5)
    weather = st.selectbox("Weather", ["Clear", "Rainy", "Foggy"])
    police = st.slider("Police Presence", 1, 10, 5)

    risk = traffic_level * 2
    if weather == "Rainy": risk += 5
    if weather == "Foggy": risk += 7
    risk -= police

    label = "🟢 Low"
    if risk > 15: label = "🔴 High"
    elif risk > 8: label = "🟠 Medium"

    st.markdown(f"""
    <div class="card">
        <h2>Predicted Risk: {label}</h2>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🚀 Karad Smart City Analytics • React-like Interactive Streamlit App")
