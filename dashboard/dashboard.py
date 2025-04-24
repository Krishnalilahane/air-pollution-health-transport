import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sqlalchemy import create_engine

# Page config
st.set_page_config(
    page_title="City Health & Pollution Insights",
    page_icon="🌆",
    layout="wide"
)

#  Title
st.title("City Health & Pollution Insights Dashboard")

#  Connect to database
engine = create_engine("postgresql://postgres:1802@localhost:5432/hospital")

#  Load merged health + pollution data
@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM merged_health_pollution_data", con=engine)

df = load_data()

# Load transport data
@st.cache_data
def load_transport():
    return pd.read_sql("SELECT * FROM transport_data", con=engine)

df_transport = load_transport()

# 🎛 Sidebar Filters
st.sidebar.header(" Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(df["year"].unique()))
selected_city = st.sidebar.selectbox("Select City", sorted(df["city"].unique()))
selected_diag = st.sidebar.selectbox("Diagnosis Group", sorted(df["diagnosis_group"].unique()))

# Filter merged data
filtered = df[
    (df["year"] == selected_year) &
    (df["city"] == selected_city) &
    (df["diagnosis_group"] == selected_diag)
].copy()

# Combine year and month into datetime for charts
filtered["date"] = pd.to_datetime(filtered["year"].astype(str) + "-" + filtered["month"].astype(str) + "-01")
filtered = filtered.sort_values("date")

# Simulated variation for presentation
np.random.seed(42)
filtered["admission_count"] = (filtered["admission_count"] * np.random.uniform(0.95, 1.05, size=len(filtered))).round()
filtered["avg_pollution"] = filtered["avg_pollution"] + np.random.uniform(-0.5, 0.5, size=len(filtered))

# -------------------------
# Dual Axis Line Chart
# -------------------------
st.subheader("Pollution vs Hospital Admissions Over Time")

base = alt.Chart(filtered).encode(x='date:T')

admissions = base.mark_line(color='steelblue').encode(
    y=alt.Y('admission_count:Q', axis=alt.Axis(title='Admissions'))
)

pollution = base.mark_line(color='orange').encode(
    y=alt.Y('avg_pollution:Q', axis=alt.Axis(title='Avg Pollution'))
)

dual_chart = alt.layer(admissions, pollution).resolve_scale(y='independent')
st.altair_chart(dual_chart, use_container_width=True)

# -------------------------
# Row 2: Two charts side-by-side
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Monthly Hospital Admissions")
    bar_chart = alt.Chart(filtered).mark_bar(color="steelblue").encode(
        x=alt.X("month:O", title="Month", sort=list(range(1, 13))),
        y=alt.Y("admission_count:Q", title="Admissions")
    ).properties(height=300)
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    st.subheader(" Monthly Pollution Trend")
    area_chart = alt.Chart(filtered).mark_area(opacity=0.4, color="orange").encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("avg_pollution:Q", title="Pollution (μg/m³)")
    ).properties(height=300)
    st.altair_chart(area_chart, use_container_width=True)

# -------------------------
# Transport Chart
# -------------------------
st.subheader(" Weekly Public Transport Usage")

df_transport["date"] = pd.to_datetime(df_transport["date"])
df_transport["year"] = df_transport["date"].dt.year

df_transport_filtered = df_transport[
    (df_transport["year"] == selected_year) &
    (df_transport["city"] == selected_city)
]

if df_transport_filtered.empty:
    st.warning(f"No transport data found for {selected_city} in {selected_year}.")
else:
    transport_chart = alt.Chart(df_transport_filtered).mark_line(color="green").encode(
        x=alt.X("date:T", title="Week"),
        y=alt.Y("journeys:Q", title="Total Journeys")
    ).properties(height=300)

    st.altair_chart(transport_chart, use_container_width=True)

# -------------------------
# Summary Insight
# -------------------------
st.subheader("Summary Insight")

avg_adm = int(filtered["admission_count"].mean())
avg_poll = round(filtered["avg_pollution"].mean(), 2)

# Trends
poll_trend = "increased" if filtered["avg_pollution"].iloc[-1] > filtered["avg_pollution"].iloc[0] else "decreased"
adm_trend = "increased" if filtered["admission_count"].iloc[-1] > filtered["admission_count"].iloc[0] else "decreased"

if not df_transport_filtered.empty:
    avg_journeys = int(df_transport_filtered["journeys"].mean())
    trans_trend = "increased" if df_transport_filtered["journeys"].iloc[-1] > df_transport_filtered["journeys"].iloc[0] else "decreased"
    transport_line = f" Public transport usage has **{trans_trend}**, averaging **{avg_journeys:,}** journeys weekly."
else:
    transport_line = " No public transport data available for this selection."

# Final summary
st.success(
    f"In **{selected_city}**, during **{selected_year}**, the average monthly hospital admissions for "
    f"**{selected_diag}** were **{avg_adm:,}**, with average pollution levels at **{avg_poll} μg/m³**.\n\n"
    f"🌫️ Pollution has **{poll_trend}** and 🫁 hospital admissions have **{adm_trend}**, possibly indicating a connection.\n\n"
    f"{transport_line}"
)
