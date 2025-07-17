# carbon-emission-calculator
carbon-emission-calculator 

# 🌱 Carbon Emission Calculator Pro

A Streamlit-based web app that helps individuals estimate their annual carbon footprint based on lifestyle inputs like transportation, electricity, shopping, and more. It also suggests how many trees need to be planted to offset the calculated emissions.

---

## 🚀 Features

- 📊 Calculates carbon emissions across:
  - Transportation 🚗
  - Electricity usage 💡
  - Waste generation 🗑️
  - Shopping 🛒
  - Flights ✈️
  - Heating 🏠
- 📈 Visual representation:
  - Pie chart (category-wise breakdown)
  - Bar chart (comparison with national & global averages)
- 🌳 Suggests how many trees to plant to offset emissions
- 💰 Donation button to contribute to tree planting
- 🧾 Session-based emission history

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) — for building the web UI
- [Plotly](https://plotly.com/python/) — for pie & bar charts
- Python — core language

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/carbon-emission-calculator.git
cd carbon-emission-calculator

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
