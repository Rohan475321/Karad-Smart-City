import streamlit as st
st.set_page_config(page_title="Karad Smart City Analytics", layout="wide")

import pandas as pd
import plotly.express as px
import os, time, io

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ===================== LOAD DATA =====================
DATA_PATH = "data"
traffic = pd.read_csv(os.path.join(DATA_PATH, "traffic_accidents.csv"))
services = pd.read_csv(os.path.join(DATA_PATH, "public_services.csv"))
business = pd.read_csv(os.path.join(DATA_PATH, "businesses.csv"))
social = pd.read_csv(os.path.join(DATA_PATH, "social_indicators.csv"))

# ===================== HERO =====================
st.markdown("""
<div style="
background: linear-gradient(135deg,#2563EB,#1E3A8A);
padding:35px;
border-radius:20px;
color:white;
">
<h1>🏙️ Karad Smart City Analytics Dashboard</h1>
<p style="font-size:18px;">
Public Data • Business Intelligence • Social Impact
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===================== KPI ANIMATION =====================
def animated_kpi(title, value, icon):
    placeholder = st.empty()
    step = max(1, int(value / 25)) if value > 0 else 1
    for i in range(0, int(value) + 1, step):
        placeholder.markdown(f"""
        <div style="
            background:white;
            padding:20px;
            border-radius:18px;
            box-shadow:0 6px 14px rgba(0,0,0,0.08);
            text-align:center;
        ">
            <h2>{icon} {i}</h2>
            <p style="color:#475569;">{title}</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.015)

# ===================== PDF REPORT =====================
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

    content.append(Paragraph("<br/><b>Key Insights</b>", styles["Heading2"]))
    content.append(Paragraph(
        "• Accident risk peaks during evening hours (6–10 PM)<br/>"
        "• Central wards show higher business density<br/>"
        "• Infrastructure improvement required in high-complaint wards",
        styles["Normal"]
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ===================== TABS =====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏙️ Overview",
    "🚦 Traffic",
    "🚰 Public Services",
    "🏪 Business Intelligence",
    "📈 Predictive Insights",
    "🧪 What-If Analysis"
])

# =====================================================
# 🏙️ OVERVIEW
# =====================================================
with tab1:
    st.markdown("## 📌 City Health Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    with c1: animated_kpi("Total Accidents", len(traffic), "🚦")
    with c2: animated_kpi("Total Businesses", business["count"].sum(), "🏪")
    with c3: animated_kpi("Water Issues", services["water_issues"].sum(), "🚰")
    with c4: animated_kpi("Avg Safety Index", round(social["safety_index"].mean(),1), "🛡️")

    acc = traffic.groupby("ward").size().reset_index(name="Accidents")
    fig = px.bar(acc, x="ward", y="Accidents", title="Accidents by Ward")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📄 Download Executive Report")
    pdf = generate_pdf()
    st.download_button(
        "⬇️ Download PDF Report",
        data=pdf,
        file_name="Karad_Smart_City_Report.pdf",
        mime="application/pdf"
    )

# =====================================================
# 🚦 TRAFFIC
# =====================================================
with tab2:
    st.markdown("## 🚦 Traffic & Accident Analysis")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(traffic, x="hour", title="Accidents by Hour")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(traffic, names="vehicle_type", title="Vehicle Type Involvement")
        st.plotly_chart(fig, use_container_width=True)

    st.info("📌 Peak accident risk observed between 6 PM – 10 PM.")

# =====================================================
# 🚰 PUBLIC SERVICES
# =====================================================
with tab3:
    st.markdown("## 🚰 Public Services Performance")

    fig = px.bar(
        services,
        x="ward",
        y="water_issues",
        title="Water Supply Issues by Ward"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 🏪 BUSINESS
# =====================================================
with tab4:
    st.markdown("## 🏪 Local Business Intelligence")

    fig = px.bar(
        business,
        x="ward",
        y="count",
        color="business_type",
        title="Business Distribution by Ward"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 📈 PREDICTIVE INSIGHTS
# =====================================================
with tab5:
    st.markdown("## 📈 Predictive & Prescriptive Insights")

    st.markdown("""
    <div style="
    background:#ECFEFF;
    padding:20px;
    border-left:6px solid #0891B2;
    border-radius:14px;
    ">
    <b>🔮 Accident Risk Prediction</b><br><br>
    High traffic density + evening hours + bad weather = higher risk.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:#F0FDF4;
    padding:20px;
    border-left:6px solid #16A34A;
    border-radius:14px;
    ">
    <b>✅ Recommendations</b>
    <ul>
        <li>Deploy traffic police during peak hours</li>
        <li>Install speed cameras at junctions</li>
        <li>Improve road lighting</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 🧪 WHAT-IF ANALYSIS
# =====================================================
with tab6:
    st.markdown("## 🧪 What-If Accident Risk Simulation")

    traffic_level = st.slider("Traffic Density", 1, 10, 5)
    weather = st.selectbox("Weather Condition", ["Clear", "Rainy", "Foggy"])
    police = st.slider("Traffic Police Presence", 1, 10, 5)

    risk_score = traffic_level * 2
    if weather == "Rainy":
        risk_score += 5
    elif weather == "Foggy":
        risk_score += 7
    risk_score -= police

    if risk_score > 15:
        risk = "🔴 High Risk"
    elif risk_score > 8:
        risk = "🟠 Medium Risk"
    else:
        risk = "🟢 Low Risk"

    st.markdown(f"""
    <div style="
    background:#FFF7ED;
    padding:20px;
    border-left:6px solid #F97316;
    border-radius:14px;
    font-size:18px;
    ">
    <b>Predicted Accident Risk:</b> {risk}
    </div>
    """, unsafe_allow_html=True)

# ===================== FOOTER =====================
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🚀 Karad Smart City Analytics • End-to-End Data Analytics Project")
