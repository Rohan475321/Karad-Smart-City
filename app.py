import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Karad Smart City Analytics", layout="wide")
st.set_option("client.showErrorDetails", True)

st.title("🏙️ Karad Smart City Analytics Dashboard")
st.markdown("**Public Data | Business | Social Impact**")
st.markdown("---")

# ---------------- SAFE DATA LOADING ----------------
DATA_PATH = "data"

try:
    traffic = pd.read_csv(os.path.join(DATA_PATH, "traffic_accidents.csv"))
    services = pd.read_csv(os.path.join(DATA_PATH, "public_services.csv"))
    business = pd.read_csv(os.path.join(DATA_PATH, "businesses.csv"))
    social = pd.read_csv(os.path.join(DATA_PATH, "social_indicators.csv"))
except Exception as e:
    st.error("❌ Error loading CSV files")
    st.exception(e)
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.header("📊 Controls")

ward_list = sorted(traffic["ward"].unique())
selected_ward = st.sidebar.selectbox("Select Ward", ["All"] + ward_list)

module = st.sidebar.radio(
    "Select Module",
    [
        "City Overview",
        "Traffic & Accident Analysis",
        "Public Services",
        "Business Intelligence",
        "Social Impact"
    ]
)

# ---------------- FILTER ----------------
def filter_df(df):
    if selected_ward == "All":
        return df
    return df[df["ward"] == selected_ward]

traffic_f = filter_df(traffic)
services_f = filter_df(services)
business_f = filter_df(business)
social_f = filter_df(social)

# ---------------- CITY OVERVIEW ----------------
if module == "City Overview":

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Accidents", len(traffic_f))
    c2.metric("Total Businesses", business_f["count"].sum())
    c3.metric("Water Issues", services_f["water_issues"].sum())
    c4.metric("Avg Safety Index", round(social_f["safety_index"].mean(), 1))

    st.markdown("---")

    acc = traffic.groupby("ward").size().reset_index(name="accidents")
    fig = px.bar(acc, x="ward", y="accidents", title="Accidents by Ward")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TRAFFIC ----------------
elif module == "Traffic & Accident Analysis":

    st.subheader("🚦 Traffic & Accident Analysis")

    if traffic_f.empty:
        st.warning("No data available for this ward.")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(
            traffic_f,
            x="hour",
            title="Accidents by Hour"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(
            traffic_f,
            names="vehicle_type",
            title="Accidents by Vehicle Type"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📍 Accident Locations")

    fig3 = px.scatter_mapbox(
        traffic_f,
        lat="latitude",
        lon="longitude",
        size="severity",
        color="severity",
        zoom=11,
        center={"lat": 17.274, "lon": 74.182},
        mapbox_style="open-street-map",
        hover_name="ward"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------- PUBLIC SERVICES ----------------
elif module == "Public Services":

    fig = px.bar(
        services_f,
        x="ward",
        y="water_issues",
        title="Water Issues by Ward"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- BUSINESS ----------------
elif module == "Business Intelligence":

    fig = px.bar(
        business_f,
        x="ward",
        y="count",
        color="business_type",
        title="Business Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- SOCIAL ----------------
elif module == "Social Impact":

    fig = px.line(
        social_f,
        x="ward",
        y="safety_index",
        title="Safety Index by Ward",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Karad Smart City Analytics | Streamlit")
