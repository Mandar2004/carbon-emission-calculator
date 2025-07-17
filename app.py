import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import math

# Constants
CO2_ABSORPTION_PER_TREE = 21  # kg CO2/year per tree

# Emission Factors
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kg CO2/km
        "Electricity": 0.82,     # kg CO2/kWh
        "Waste": 0.1,            # kg CO2/kg
        "Shopping": 6.5,         # kg CO2 per ₹1000
        "Flights": {
            "Short": 300,
            "Medium": 1100,
            "Long": 2500
        },
        "Heating": {
            "Electricity": 0.82,
            "LPG": 2.98,
            "Wood": 1.75
        }
    }
}

# Streamlit Setup
st.set_page_config(layout="wide", page_title="Carbon Calculator Pro")
st.title("🌱 Personal Carbon Emission Calculator")

# Country Selection
country = st.selectbox("🌍 Your Country", ["India"])

# UI Inputs
col1, col2 = st.columns(2)

with col1:
    distance = st.slider("🚗 Daily commute distance (km)", 0.0, 100.0)
    electricity = st.slider("💡 Monthly electricity use (kWh)", 0.0, 1000.0)
    waste = st.slider("🗑️ Waste generated per week (kg)", 0.0, 100.0)

with col2:
    shopping = st.slider("🛒 Monthly spending on goods (₹)", 0, 50000, step=1000)
    num_short = st.number_input("🛫 Short-haul Flights (0–1500km)", 0, step=1)
    num_medium = st.number_input("🛫 Medium-haul Flights (1500–4000km)", 0, step=1)
    num_long = st.number_input("🛫 Long-haul Flights (4000km+)", 0, step=1)
    heating_type = st.selectbox("🏡 Primary Heating Fuel", ["Electricity", "LPG", "Wood"])
    heating_usage = st.slider("🔥 Estimated monthly heating usage", 0.0, 500.0)

# Normalize Inputs to Annual
distance *= 365
electricity *= 12
waste *= 52
shopping *= 12
heating_usage *= 12

# Calculate Emissions in kg CO2
ef = EMISSION_FACTORS[country]

transport_emission = ef["Transportation"] * distance
electricity_emission = ef["Electricity"] * electricity
waste_emission = ef["Waste"] * waste
shopping_emission = (shopping / 1000) * ef["Shopping"]
flights_emission = (
    ef["Flights"]["Short"] * num_short +
    ef["Flights"]["Medium"] * num_medium +
    ef["Flights"]["Long"] * num_long
)
heating_emission = ef["Heating"][heating_type] * heating_usage

# Total emission in kg and tonnes
total_emission_kg = sum([
    transport_emission, electricity_emission, waste_emission,
    shopping_emission, flights_emission, heating_emission
])
total_emission = round(total_emission_kg / 1000, 2)

# Required number of trees
required_tree_count = math.ceil(total_emission_kg / CO2_ABSORPTION_PER_TREE)

# Breakdown in tonnes for pie chart
emissions = {
    "Transportation": round(transport_emission / 1000, 2),
    "Electricity": round(electricity_emission / 1000, 2),
    "Waste": round(waste_emission / 1000, 2),
    "Shopping": round(shopping_emission / 1000, 2),
    "Flights": round(flights_emission / 1000, 2),
    "Heating": round(heating_emission / 1000, 2)
}

# Session history
if "history" not in st.session_state:
    st.session_state.history = []

# Calculate Button
if st.button("📊 Calculate CO2 Emissions"):
    st.header("Results Summary")

    col3, col4 = st.columns(2)
    with col3:
        for category, value in emissions.items():
            st.info(f"🔹 {category}: {value} tonnes CO2/year")

        # 🌳 Big message for tree count
        st.markdown(
            f"<h3 style='color:green;'>🌳 You need to plant <b>{required_tree_count} trees</b> to offset your carbon footprint.</h3>",
            unsafe_allow_html=True
        )

    with col4:
        st.success(f"🌍 Total Emissions: **{total_emission} tonnes CO2/year**")
        st.warning("🇮🇳 India Avg: 1.9 t/year | 🌐 Global Avg: 4.7 t/year")

    # 🌳 Donation Button
    st.markdown("---")
    donate_url = "https://www.grow-trees.com"  # You can change this to another trusted site
    st.markdown(
        f"<a href='{donate_url}' target='_blank'><button style='background-color:#4CAF50; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:8px;'>🌳 Donate to Plant Trees</button></a>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Store to history
    st.session_state.history.append({
        "Total": total_emission,
        "TreesNeeded": required_tree_count,
        **emissions
    })

    # Pie Chart
    st.subheader("📈 Emission Breakdown (Pie Chart)")
    pie_fig = px.pie(
        names=list(emissions.keys()),
        values=list(emissions.values()),
        title="Category-wise Emissions",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_fig)

    # Bar Chart
    st.subheader("📊 Your Emissions vs Averages")
    bar_fig = go.Figure(data=[
        go.Bar(name="You", x=["Carbon Footprint"], y=[total_emission]),
        go.Bar(name="India Avg", x=["Carbon Footprint"], y=[1.9]),
        go.Bar(name="Global Avg", x=["Carbon Footprint"], y=[4.7])
    ])
    bar_fig.update_layout(barmode='group')
    st.plotly_chart(bar_fig)

# History Section
if st.checkbox("📜 Show Calculation History"):
    for i, record in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**Entry #{i}** — Total: {record['Total']} t | Trees Needed: {record['TreesNeeded']}")
        st.caption(", ".join([f"{k}: {v}t" for k, v in record.items() if k not in ["Total", "TreesNeeded"]]))
        st.markdown("---")
