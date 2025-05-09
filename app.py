
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Triphorium Energy Dashboard", layout="wide")

st.title("🏢 Triphorium Energy Dashboard")

# ========== 用户输入建筑信息 ==========
st.sidebar.header("🏗️ Building Input")
building_type = st.sidebar.selectbox("Building Type", ["Office", "School", "Hospital", "Retail"])
floor_area = st.sidebar.number_input("Area (sqft)", value=100000)
address = st.sidebar.text_input("Address", "New York, NY")
electricity_benchmark = st.sidebar.number_input("Electricity Benchmark (kWh/sqft/year)", value=12.0)
co2_benchmark = st.sidebar.number_input("CO₂ Benchmark (tons/year)", value=400.0)

climate_zone = "4A - Mixed-Humid" if "NY" in address else "Unknown"
st.markdown(f"**Climate Zone**: {climate_zone}")

# ========== 上传数据 ==========
uploaded_file = st.file_uploader("Upload your building energy CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.success("✅ File uploaded successfully!")

    # ========== 图表分列显示 ==========
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.subheader("⚡ Electricity Consumption (kWh)")
        fig1 = px.line(df, x="timestamp", y="electricity_kwh", title="Electricity Over Time")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("💧 Water Usage (tons)")
        fig2 = px.line(df, x="timestamp", y="water_tons", title="Water Usage Over Time")
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.subheader("🔥 Gas Consumption (m³)")
        fig3 = px.line(df, x="timestamp", y="gas_m3", title="Gas Consumption Over Time")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("🌫️ CO₂ Emissions (tons)")
        fig4 = px.line(df, x="timestamp", y="co2_tons", title="CO2 Emissions Over Time")
        st.plotly_chart(fig4, use_container_width=True)

    # ========== 评级 & 建议逻辑 ==========
    st.header("🏅 Building Energy Rating & Optimization")
    latest_year = df["timestamp"].dt.year.max()
    df_latest = df[df["timestamp"].dt.year == latest_year]
    annual_kwh = df_latest["electricity_kwh"].sum()
    annual_co2 = df_latest["co2_tons"].sum()
    kwh_per_sqft = annual_kwh / floor_area

    if annual_co2 <= co2_benchmark * 0.7:
        rating = "A"
    elif annual_co2 <= co2_benchmark:
        rating = "B"
    elif annual_co2 <= co2_benchmark * 1.3:
        rating = "C"
    else:
        rating = "D"

    st.markdown(f"**Latest Year**: {latest_year}")
    st.markdown(f"**Electricity Intensity**: {kwh_per_sqft:.2f} kWh/sqft")
    st.markdown(f"**Annual CO₂ Emission**: {annual_co2:.2f} tons")
    st.markdown(f"**🏆 NYC Energy Rating**: **:blue[{rating}]**")

    # ========== 节能建议 ==========
    if rating in ["C", "D"]:
        st.warning("⚠️ This building is underperforming. Consider energy retrofits.")
        saving_percent = 0.25
        potential_saving = annual_kwh * saving_percent
        elec_price = st.number_input("Electricity Price ($/kWh)", value=0.18)
        saving_value = potential_saving * elec_price
        investment = st.number_input("Estimated Investment ($)", value=30000)
        roi = (saving_value / investment) * 100
        payback = investment / saving_value if saving_value > 0 else "N/A"

        st.markdown(f"💡 **Suggested Saving**: {potential_saving:.0f} kWh/year")
        st.markdown(f"💰 **Annual Saving**: ${saving_value:,.0f}")
        st.markdown(f"📈 **Estimated ROI**: {roi:.1f}%")
        st.markdown(f"⏱️ **Payback Period**: {payback:.1f} years")
    else:
        st.success("✅ This building is operating efficiently. No urgent improvements needed.")
