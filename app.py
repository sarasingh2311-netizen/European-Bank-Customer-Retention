
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# PAGE SETTINGS
# --------------------------

st.set_page_config(
    page_title="European Bank Customer Retention Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 European Bank Customer Retention Dashboard")
st.markdown("### Customer Engagement & Relationship Strength Analysis")

# --------------------------
# LOAD DATA
# --------------------------

df = pd.read_csv("Processed_Bank_Data.csv")

# --------------------------
# SIDEBAR FILTERS
# --------------------------

st.sidebar.header("Filter Data")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + list(df["Geography"].unique())
)

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + list(df["Gender"].unique())
)

if country != "All":
    df = df[df["Geography"] == country]

if gender != "All":
    df = df[df["Gender"] == gender]

# --------------------------
# KPI CALCULATIONS
# --------------------------

total_customers = len(df)

churn_rate = df["Exited"].mean() * 100

active_customers = df["IsActiveMember"].sum()

avg_balance = df["Balance"].mean()

avg_salary = df["EstimatedSalary"].mean()

# --------------------------
# KPI CARDS
# --------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("👥 Total Customers", total_customers)

col2.metric("❌ Churn Rate", f"{churn_rate:.2f}%")

col3.metric("✅ Active Members", active_customers)

col4.metric("💰 Avg Balance", f"{avg_balance:,.0f}")

col5.metric("💵 Avg Salary", f"{avg_salary:,.0f}")

st.markdown("---")
# --------------------------
# CHARTS
# --------------------------

st.subheader("📊 Customer Churn Overview")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        df,
        x="Exited",
        color="Exited",
        title="Customer Churn Distribution",
        labels={"Exited": "Exited (0=No, 1=Yes)"}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        df,
        x="Geography",
        color="Exited",
        barmode="group",
        title="Geography vs Churn"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------

col3, col4 = st.columns(2)

with col3:
    fig = px.histogram(
        df,
        x="Gender",
        color="Exited",
        barmode="group",
        title="Gender vs Churn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.histogram(
        df,
        x="NumOfProducts",
        color="Exited",
        barmode="group",
        title="Products vs Churn"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------

st.subheader("👥 Customer Activity")

fig = px.histogram(
    df,
    x="IsActiveMember",
    color="Exited",
    barmode="group",
    title="Active Members vs Churn"
)

st.plotly_chart(fig, use_container_width=True)
# --------------------------
# BALANCE DISTRIBUTION
# --------------------------

st.subheader("💰 Balance Distribution")

fig = px.histogram(
    df,
    x="Balance",
    nbins=30,
    title="Customer Balance Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------
# HIGH VALUE CUSTOMER DETECTOR
# --------------------------

st.subheader("⭐ High Value Disengaged Customers")

balance_filter = st.slider(
    "Select Minimum Balance",
    min_value=0,
    max_value=int(df["Balance"].max()),
    value=100000
)

premium = df[
    (df["Balance"] >= balance_filter) &
    (df["IsActiveMember"] == 0)
]

st.write(f"Total High Value Inactive Customers: {len(premium)}")

st.dataframe(premium)

# --------------------------
# RELATIONSHIP SCORE
# --------------------------

if "RelationshipScore" in df.columns:

    st.subheader("📈 Relationship Strength")

    fig = px.histogram(
        df,
        x="RelationshipScore",
        nbins=20,
        title="Relationship Strength Score"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# DOWNLOAD DATA
# --------------------------

st.subheader("📥 Download Processed Data")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="Processed_Bank_Data.csv",
    mime="text/csv"
)