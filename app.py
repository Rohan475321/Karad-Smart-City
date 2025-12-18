import streamlit as st
st.set_page_config(page_title="Karad Smart City Analytics", layout="wide")

import pandas as pd
import plotly.express as px
import os

# -------------------- LOAD DATA --------------------
DATA_PATH = "data"
traffic = pd.read_csv(os.path.join(DATA_PATH, "traffic_accidents.csv"))
services = pd.read_csv(os.path.join(DATA_PATH, "public_services.csv"))
business = pd.read_csv(os.path.join(DATA_PATH, "businesses.csv"))
social = pd.read_csv(os.path.join(DATA_PATH, "social_indicators.csv"))

# -------------------- MAP DATA --------------------
map_df = traffic[["latitude", "longitude"]].copy()
map_df.columns = ["17.2850", "74.1840"]

# -------------------- HERO SECTION --------------------
st.markdown("""
<div style="
background: linear-gradient(135deg,#2563EB,#1E3A8A);
padding:35px;
border-radius:20px;
color:white;
">
<h1>🏙️ Karad Smart City Analytics</h1>
<p style="font-size:18px;">
Public Data • Business Intelligence • Social Impact
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.markdown("""
<h2 style="color:#2563EB;">📊 Dashboard Controls</h2>
<hr>
""", unsafe_allow_html=True)

ward = st.sidebar.selectbox(
    "📍 Select Ward",
    ["All"] + sorted(traffic["ward"].unique())
)

module = st.sidebar.radio(
    "🧭 Select Module",
    [
        "🏙️ City Overview",
        "🚦 Traffic Analysis",
        "🚰 Public Services",
        "🏪 Business Intelligence",
        "❤️ Social Impact"
    ]
)

# -------------------- FILTER --------------------
def filter_df(df):
    if ward == "All":
        return df
    return df[df["ward"] == ward]

traffic_f = filter_df(traffic)
services_f = filter_df(services)
business_f = filter_df(business)
social_f = filter_df(social)

# -------------------- KPI CARD FUNCTION --------------------
def kpi_card(title, value, icon):
    st.markdown(f"""
    <div style="
        background:white;
        padding:22px;
        border-radius:18px;
        box-shadow:0 6px 14px rgba(0,0,0,0.08);
        text-align:center;
    ">
        <h2>{icon} {value}</h2>
        <p style="color:#475569;">{title}</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# 🏙️ CITY OVERVIEW
# ======================================================
if module == "🏙️ City Overview":

    st.markdown("## 📌 City Health Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Total Accidents", len(traffic_f), "🚦")
    with c2: kpi_card("Total Businesses", business_f["count"].sum(), "🏪")
    with c3: kpi_card("Water Issues", services_f["water_issues"].sum(), "🚰")
    with c4: kpi_card("Avg Safety Index", round(social_f["safety_index"].mean(),1), "🛡️")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- MAP --------
    st.markdown("### 🗺️ Project Location – Karad City")
    st.map(map_df, zoom=11)

    st.markdown("""
    <div style="
    background:#EFF6FF;
    padding:16px;
    border-left:6px solid #2563EB;
    border-radius:12px;
    ">
    <b>📌 Insight:</b><br>
    This map visualizes accident locations across Karad,
    helping identify high-risk zones spatially.
    </div>
    """, unsafe_allow_html=True)

    acc = traffic.groupby("ward").size().reset_index(name="Accidents")
    fig = px.bar(acc, x="ward", y="Accidents", title="Accidents by Ward")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 🚦 TRAFFIC ANALYSIS
# ======================================================
elif module == "🚦 Traffic Analysis":

    st.markdown("## 🚦 Traffic & Accident Patterns")

    # -------- MAP --------
    st.markdown("### 🚦 Accident Locations Map")
    st.map(map_df, zoom=12)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(traffic_f, x="hour", title="Accidents by Hour")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(traffic_f, names="vehicle_type", title="Vehicle Type Involvement")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="
    background:#EFF6FF;
    padding:18px;
    border-left:6px solid #2563EB;
    border-radius:12px;
    ">
    <b>📌 Insight:</b>  
    Majority of accidents occur during evening peak hours indicating traffic congestion risk.
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# 🚰 PUBLIC SERVICES
# ======================================================
elif module == "🚰 Public Services":

    st.markdown("## 🚰 Public Service Performance")

    fig = px.bar(
        services_f,
        x="ward",
        y="water_issues",
        title="Water Supply Issues by Ward"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 🏪 BUSINESS INTELLIGENCE
# ======================================================
elif module == "🏪 Business Intelligence":

    st.markdown("## 🏪 Local Business Intelligence")

    fig = px.bar(
        business_f,
        x="ward",
        y="count",
        color="business_type",
        title="Business Density by Ward"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# ❤️ SOCIAL IMPACT
# ======================================================
elif module == "❤️ Social Impact":

    st.markdown("## ❤️ Social & Safety Indicators")

    fig = px.line(
        social_f,
        x="ward",
        y="safety_index",
        markers=True,
        title="Safety Index by Ward"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# -------------------- FOOTER --------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🚀 Karad Smart City Analytics • Built with Streamlit & Python")
