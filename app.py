
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Telecom Intelligence",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071426, #0b1d32);
    color: #e5f4ff;
}
[data-testid="stMetric"] {
    background: #112941;
    border: 1px solid #1d5268;
    padding: 18px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #52e0d0;
}
</style>
""", unsafe_allow_html=True)

st.title("Telecom Revenue & Network Intelligence")
st.caption(
    "Synthetic portfolio dataset | Revenue assurance and anomaly monitoring"
)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------
data_path = Path(__file__).parent / "data" / "telecom_revenue_data.csv"

if not data_path.exists():
    st.error("Dataset not found. Check that the data folder is beside app.py.")
    st.stop()

df = pd.read_csv(data_path)

required_columns = [
    "record_id", "region", "service_type", "month",
    "monthly_revenue", "billed_amount",
    "activation_delay_days", "collection_amount"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {', '.join(missing_columns)}")
    st.stop()

# --------------------------------------------------
# 3. ANOMALY DETECTION
# --------------------------------------------------
df["billing_gap"] = (
    df["monthly_revenue"] - df["billed_amount"]
).round(2)

df["collection_gap"] = (
    df["billed_amount"] - df["collection_amount"]
).round(2)

df["billing_anomaly"] = (
    df["billed_amount"] < df["monthly_revenue"] * 0.50
)

df["activation_anomaly"] = (
    df["activation_delay_days"] > 10
)

df["collection_anomaly"] = (
    (df["collection_amount"] == 0)
    & (df["billed_amount"] > 0)
)

df["potential_anomaly"] = (
    df["billing_anomaly"]
    | df["activation_anomaly"]
    | df["collection_anomaly"]
)

df["anomaly_score"] = (
    df["billing_anomaly"].astype(int) * 3
    + df["activation_anomaly"].astype(int) * 2
    + df["collection_anomaly"].astype(int) * 3
)

# Updated priority rules, aligned with the notebook
df["priority"] = np.select(
    [
        df["billing_anomaly"] | df["collection_anomaly"],
        df["activation_anomaly"]
    ],
    [
        "High",
        "Medium"
    ],
    default="No Alert"
)

# --------------------------------------------------
# 4. SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select regions",
    options=sorted(df["region"].dropna().unique()),
    default=sorted(df["region"].dropna().unique())
)

services = st.sidebar.multiselect(
    "Select services",
    options=sorted(df["service_type"].dropna().unique()),
    default=sorted(df["service_type"].dropna().unique())
)

priorities = st.sidebar.multiselect(
    "Alert priority",
    options=["High", "Medium", "No Alert"],
    default=["High", "Medium", "No Alert"]
)

filtered = df[
    df["region"].isin(regions)
    & df["service_type"].isin(services)
    & df["priority"].isin(priorities)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Change your selections.")
    st.stop()

# --------------------------------------------------
# 5. KPI CARDS
# --------------------------------------------------
revenue = filtered["monthly_revenue"].sum()
billed = filtered["billed_amount"].sum()
collections = filtered["collection_amount"].sum()

alerts = int(filtered["potential_anomaly"].sum())
high_alerts = int((filtered["priority"] == "High").sum())
billing_gap = filtered["billing_gap"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Records", f"{len(filtered):,}")
c2.metric("Revenue", f"₹{revenue / 1e7:.2f} Cr")
c3.metric("Billed Amount", f"₹{billed / 1e7:.2f} Cr")
c4.metric("Potential Alerts", f"{alerts:,}")

c5, c6, c7 = st.columns(3)

c5.metric("High-Priority Records", f"{high_alerts:,}")
c6.metric("Collections", f"₹{collections / 1e7:.2f} Cr")
c7.metric("Revenue-Billing Gap", f"₹{billing_gap:,.0f}")

st.divider()

# --------------------------------------------------
# 6. REVENUE BY REGION
# --------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Revenue by Region")

    region_data = (
        filtered.groupby("region", as_index=False)
        .agg(
            Revenue=("monthly_revenue", "sum"),
            Billed=("billed_amount", "sum")
        )
    )

    chart = px.bar(
        region_data,
        x="region",
        y=["Revenue", "Billed"],
        barmode="group",
        template="plotly_dark",
        labels={"value": "Amount (₹)", "region": "Region"}
    )

    st.plotly_chart(chart, use_container_width=True)

# --------------------------------------------------
# 7. ALERT PRIORITY DISTRIBUTION
# --------------------------------------------------
with right:
    st.subheader("Potential Alerts by Priority")

    priority_data = (
        filtered.groupby("priority")
        .size()
        .reset_index(name="Records")
    )

    chart = px.pie(
        priority_data,
        names="priority",
        values="Records",
        hole=0.55,
        template="plotly_dark"
    )

    st.plotly_chart(chart, use_container_width=True)

# --------------------------------------------------
# 8. MONTHLY REVENUE TREND
# --------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Monthly Revenue Trend")

    monthly = (
        filtered.groupby("month", as_index=False)
        .agg(
            Revenue=("monthly_revenue", "sum"),
            Billed=("billed_amount", "sum")
        )
        .sort_values("month")
    )

    chart = px.line(
        monthly,
        x="month",
        y=["Revenue", "Billed"],
        markers=True,
        template="plotly_dark",
        labels={"value": "Amount (₹)", "month": "Month"}
    )

    st.plotly_chart(chart, use_container_width=True)

# --------------------------------------------------
# 9. ALERTS BY REGION
# --------------------------------------------------
with right:
    st.subheader("Potential Alerts by Region")

    regional = (
        filtered.groupby("region", as_index=False)
        .agg(
            Alerts=("potential_anomaly", "sum")
        )
    )

    chart = px.bar(
        regional,
        x="region",
        y="Alerts",
        template="plotly_dark"
    )

    st.plotly_chart(chart, use_container_width=True)

# --------------------------------------------------
# 10. ANOMALY INVESTIGATION
# --------------------------------------------------
st.subheader("Anomaly Investigation")

alerts_df = filtered[filtered["potential_anomaly"]].copy()

if alerts_df.empty:
    st.info("No potential anomalies found for the selected filters.")
else:
    search_region = st.selectbox(
        "Investigate region",
        options=["All regions"] + sorted(
            alerts_df["region"].dropna().unique().tolist()
        )
    )

    if search_region != "All regions":
        alerts_df = alerts_df[
            alerts_df["region"] == search_region
        ]

    display_columns = [
        "record_id", "region", "service_type", "month",
        "monthly_revenue", "billed_amount",
        "billing_gap", "activation_delay_days",
        "collection_amount", "collection_gap",
        "anomaly_score", "priority"
    ]

    st.dataframe(
        alerts_df[display_columns].sort_values(
            "anomaly_score", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download filtered alerts CSV",
        data=alerts_df[display_columns].to_csv(
            index=False
        ).encode("utf-8"),
        file_name="telecom_anomaly_alerts.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# 11. FOOTER
# --------------------------------------------------
st.caption(
    "Portfolio demonstration using synthetic data. "
    "Alerts are rule-based indicators, not confirmed revenue losses or fraud."
)
