
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(page_title="UK Real Estate Analyzer", layout="wide")

st.title("🏡 UK Real Estate Analyzer")
st.markdown("A visual dashboard to explore property risk, rental yields, appreciation, and city-level summaries.")

# --- Sample CSV (50 rows) ---
SAMPLE_CSV = """PropertyID,Location,PurchasePrice,CurrentValue,AnnualRent,VacancyRate,address,price,bedrooms
1,London,510000,525000,25200,0.012,London 1,510000,3
2,Oxford,455000,470000,22300,0.015,Oxford 2,455000,3
3,Cambridge,485000,500000,23500,0.011,Cambridge 3,485000,3
4,Bath,425000,440000,20500,0.02,Bath 4,425000,2
5,Edinburgh,460000,480000,22800,0.013,Edinburgh 5,460000,3
6,Leicester,250000,255000,8050,0.03,Leicester 6,250000,2
7,Nottingham,260000,265000,8500,0.04,Nottingham 7,260000,3
8,Derby,245000,250000,7900,0.035,Derby 8,245000,2
9,Sheffield,275000,280000,9100,0.04,Sheffield 9,275000,3
10,Liverpool,285000,290000,9350,0.038,Liverpool 10,285000,3
11,Glasgow,180000,160000,7050,0.08,Glasgow 11,180000,2
12,Birmingham,200000,190000,7500,0.09,Birmingham 12,200000,2
13,Manchester,220000,210000,7800,0.07,Manchester 13,220000,3
14,Liverpool,190000,180000,7200,0.085,Liverpool 14,190000,2
15,Leeds,210000,200000,7700,0.08,Leeds 15,210000,3
16,London,520000,535000,25500,0.011,London 16,520000,3
17,Oxford,460000,475000,22500,0.016,Oxford 17,460000,3
18,Cambridge,490000,505000,23800,0.012,Cambridge 18,490000,3
19,Bath,430000,445000,21000,0.021,Bath 19,430000,2
20,Edinburgh,465000,485000,23000,0.014,Edinburgh 20,465000,3
21,Leicester,255000,260000,8100,0.03,Leicester 21,255000,2
22,Nottingham,265000,270000,8600,0.04,Nottingham 22,265000,3
23,Derby,250000,255000,7950,0.035,Derby 23,250000,2
24,Sheffield,280000,285000,9200,0.04,Sheffield 24,280000,3
25,Liverpool,290000,295000,9400,0.038,Liverpool 25,290000,3
26,Glasgow,185000,165000,7100,0.082,Glasgow 26,185000,2
27,Birmingham,205000,195000,7550,0.088,Birmingham 27,205000,2
28,Manchester,225000,215000,7850,0.072,Manchester 28,225000,3
29,Liverpool,195000,185000,7250,0.084,Liverpool 29,195000,2
30,Leeds,215000,205000,7750,0.079,Leeds 30,215000,3
31,London,530000,545000,26000,0.01,London 31,530000,3
32,Oxford,470000,485000,22800,0.015,Oxford 32,470000,3
33,Cambridge,495000,510000,24000,0.012,Cambridge 33,495000,3
34,Bath,435000,450000,21200,0.02,Bath 34,435000,2
35,Edinburgh,470000,490000,23200,0.013,Edinburgh 35,470000,3
36,Leicester,260000,265000,8150,0.03,Leicester 36,260000,2
37,Nottingham,270000,275000,8650,0.04,Nottingham 37,270000,3
38,Derby,255000,260000,8000,0.035,Derby 38,255000,2
39,Sheffield,285000,290000,9250,0.04,Sheffield 39,285000,3
40,Liverpool,295000,300000,9450,0.038,Liverpool 40,295000,3
41,Glasgow,190000,170000,7150,0.081,Glasgow 41,190000,2
42,Birmingham,210000,200000,7600,0.089,Birmingham 42,210000,2
43,Manchester,230000,220000,7900,0.071,Manchester 43,230000,3
44,Liverpool,200000,190000,7300,0.083,Liverpool 44,200000,2
45,Leeds,220000,210000,7800,0.078,Leeds 45,220000,3
46,London,540000,555000,26500,0.011,London 46,540000,3
47,Oxford,480000,495000,23000,0.016,Oxford 47,480000,3
48,Cambridge,500000,515000,24200,0.012,Cambridge 48,500000,3
49,Bath,440000,455000,21500,0.022,Bath 49,440000,2
50,Edinburgh,475000,495000,23400,0.014,Edinburgh 50,475000,3
"""

def load_data(uploaded_file):
    if uploaded_file is None:
        df = pd.read_csv(StringIO(SAMPLE_CSV))
    else:
        df = pd.read_csv(uploaded_file)
    # Ensure numeric types
    for c in ["PurchasePrice","CurrentValue","AnnualRent","VacancyRate","price","bedrooms"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # Derived metrics
    df = df.dropna(subset=["PurchasePrice","CurrentValue","AnnualRent","VacancyRate"])
    df["RentalYield"] = (df["AnnualRent"] / df["PurchasePrice"]) * 100
    df["Appreciation"] = df["CurrentValue"] - df["PurchasePrice"]
    df["AppreciationPct"] = (df["Appreciation"] / df["PurchasePrice"]) * 100
    # Risk score: higher vacancy and lower yields increase risk; higher appreciation reduces it
    df["RiskScore"] = (df["VacancyRate"] * 100) - df["RentalYield"] - (df["AppreciationPct"] / 2)
    # Risk band
    def risk_band(s):
        if s <= 0:
            return "Low"
        if s <= 10:
            return "Medium"
        return "High"
    df["RiskBand"] = df["RiskScore"].apply(risk_band)
    return df

st.sidebar.header("Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
sample_download = st.sidebar.button("Download sample CSV")

if sample_download:
    st.sidebar.markdown("Sample CSV ready for download below. Right-click and save link as...")
    st.sidebar.download_button("Download sample CSV", SAMPLE_CSV, file_name="sample_properties.csv")

df = load_data(uploaded_file)

# Filters
st.sidebar.markdown("### Filters")
locations = ["All"] + sorted(df["Location"].unique().tolist())
sel_loc = st.sidebar.selectbox("Location", locations, index=0)
min_price, max_price = int(df["PurchasePrice"].min()), int(df["PurchasePrice"].max())
price_range = st.sidebar.slider("Purchase Price range (£)", min_price, max_price, (min_price, max_price))
bed_min, bed_max = int(df["bedrooms"].min()), int(df["bedrooms"].max())
beds = st.sidebar.slider("Bedrooms", bed_min, bed_max, (bed_min, bed_max))

filtered = df[(df["PurchasePrice"] >= price_range[0]) & (df["PurchasePrice"] <= price_range[1]) &
              (df["bedrooms"] >= beds[0]) & (df["bedrooms"] <= beds[1])]
if sel_loc != "All":
    filtered = filtered[filtered["Location"] == sel_loc]

# Top KPIs
st.markdown("## Snapshot")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Avg Purchase Price (£)", f"{filtered['PurchasePrice'].mean():,.0f}")
k2.metric("Avg Rental Yield (%)", f"{filtered['RentalYield'].mean():.2f}")
k3.metric("Avg Vacancy Rate (%)", f"{filtered['VacancyRate'].mean()*100:.2f}")
k4.metric("Avg Appreciation (£)", f"{filtered['Appreciation'].mean():,.0f}")

st.markdown("---")

# Layout: left charts, right charts
left, right = st.columns((2,1))

with left:
    st.subheader("Rental Yield vs Vacancy Rate (by property)")
    fig_scatter = px.scatter(
        filtered,
        x="VacancyRate",
        y="RentalYield",
        color="RiskBand",
        size="PurchasePrice",
        hover_data=["address","bedrooms","PurchasePrice","CurrentValue","AnnualRent","RiskScore"],
        labels={"VacancyRate":"Vacancy Rate","RentalYield":"Rental Yield (%)"}
    )
    fig_scatter.update_layout(height=450, title="Vacancy Rate vs Rental Yield")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Property Appreciation (CurrentValue vs PurchasePrice)")
    fig_app = px.bar(
        filtered.sort_values("Appreciation", ascending=False).head(25),
        x="address",
        y=["PurchasePrice","CurrentValue"],
        barmode="group",
        title="Top 25 Properties - Purchase Price vs Current Value"
    )
    fig_app.update_layout(xaxis_tickangle=-45, height=420)
    st.plotly_chart(fig_app, use_container_width=True)

with right:
    st.subheader("City Overview")
    city_avg = filtered.groupby("Location").agg({
        "PurchasePrice":"mean",
        "CurrentValue":"mean",
        "AnnualRent":"mean",
        "RentalYield":"mean",
        "VacancyRate":"mean",
        "Appreciation":"mean"
    }).reset_index()
    st.dataframe(city_avg.style.format({
        "PurchasePrice":"£{:,.0f}",
        "CurrentValue":"£{:,.0f}",
        "AnnualRent":"£{:,.0f}",
        "RentalYield":"{:.2f}",
        "VacancyRate":"{:.2%}",
        "Appreciation":"£{:,.0f}"
    }), use_container_width=True)

    st.markdown("### Risk Distribution")
    risk_count = filtered["RiskBand"].value_counts().reindex(["Low","Medium","High"]).fillna(0)
    fig_pie = px.pie(values=risk_count.values, names=risk_count.index, title="Risk Band Share")
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Risk gauge for selected city or overall
st.subheader("Risk Gauge")
gauge_target = filtered["RiskScore"].mean()
gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=float(gauge_target),
    title={"text":"Average Risk Score (lower = better)"},
    delta={'reference':0},
    gauge={
        'axis': {'range': [-20, 40]},
        'steps': [
            {'range': [-20, 0], 'color': "lightgreen"},
            {'range': [0, 10], 'color': "gold"},
            {'range': [10, 40], 'color': "lightcoral"}
        ],
        'bar': {'color': "darkblue"}
    }
))
gauge.update_layout(height=300)
st.plotly_chart(gauge, use_container_width=True)

st.markdown("---")

st.subheader("Data Explorer")
st.dataframe(filtered.reset_index(drop=True).style.format({
    "PurchasePrice":"£{:,.0f}",
    "CurrentValue":"£{:,.0f}",
    "AnnualRent":"£{:,.0f}",
    "RentalYield":"{:.2f}",
    "VacancyRate":"{:.2%}",
    "Appreciation":"£{:,.0f}",
    "RiskScore":"{:.2f}"
}), use_container_width=True)

# Download filtered data
csv = filtered.to_csv(index=False)
st.download_button("Download filtered data as CSV", csv, file_name="filtered_properties.csv")

st.markdown("----")
st.markdown("**Notes:** RiskScore is a heuristic combining vacancy rate, rental yield and appreciation percentage; adjust formula as needed for your model.")
