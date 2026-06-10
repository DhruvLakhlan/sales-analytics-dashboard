import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark SaaS Custom CSS Theme Injection
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global font style overrides */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    
    /* Dark app background force */
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    
    /* Compact layout: reduce top padding by 50% */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Page Header */
    .page-header {
        margin-bottom: 0.5rem;
    }
    .page-title {
        font-size: 1.75rem !important;
        font-weight: 700;
        color: #F8FAFC !important;
        margin: 0 0 0.25rem 0 !important;
        padding: 0 !important;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Section Title Header overrides */
    .section-title {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0 !important;
        color: #CBD5E1 !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.5rem !important;
        text-transform: none;
    }
    
    /* Metric Widget Overrides */
    div[data-testid="stMetric"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
    border-color: #3B82F6 !important;
    transform: translateY(-2px);
    }
            
    div[data-testid="stMetricValue"] > div {
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
    }
    div[data-testid="stMetricLabel"] > div {
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #64748B !important;
        font-weight: 600 !important;
    }
    
    /* Hide standard Streamlit page sidebar links list */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Sidebar Layout Overrides */
    section[data-testid="stSidebar"] {
       background-color: #0B0F19 !important;
       border-right: 1px solid #1E293B !important;
       padding-top: 0 !important;
    }  

    }
            
    section[data-testid="stSidebar"] [data-testid="stSubheader"] {
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #475569 !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Custom Navigation Cards */
    div[data-testid="stPageLink"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0px !important; /* Full width clickable container */
        margin-bottom: 0.75rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stPageLink"] a {
        display: flex !important;
        flex-direction: column !important;
        padding: 12px 14px !important;
        text-decoration: none !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        border-left: 4px solid transparent !important;
        border-radius: 10px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    
    /* Navigation Hover & Active status */
    div[data-testid="stPageLink"]:hover {
        border-color: #3B82F6 !important;
        transform: translateY(-1px);
    }
    div[data-testid="stPageLink"]:has(a[aria-current="page"]) {
        background-color: #243049 !important;
    }
    div[data-testid="stPageLink"]:has(a[aria-current="page"]) a {
        border-left: 4px solid #3B82F6 !important;
        border-top-left-radius: 0 !important;
        border-bottom-left-radius: 0 !important;
    }
    div[data-testid="stPageLink"]:has(a[aria-current="page"]) a::after {
        color: #3B82F6 !important;
    }
    
    /* Tabs Overrides */
    button[data-baseweb="tab"] {
        color: #64748B !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    button[aria-selected="true"] {
        color: #3B82F6 !important;
        border-bottom-color: #3B82F6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Import local utilities
from utils.data_loader import load_data, get_or_create_sample_data
from utils.metrics import calculate_kpis
from utils.charts import (
    plot_sales_trend, plot_profit_trend, plot_regional_performance,
    plot_category_analysis, plot_subcategory_analysis, plot_top_customers
)

# Render Custom Sidebar Navigation Cards
# Sidebar Branding

st.sidebar.markdown("""
<div style="margin-top:-25px;">
    <h2 style="margin:0;color:white;">
        Sales Analytics
    </h2>
    <p style="margin:4px 0 12px 0;color:#94A3B8;">
        Business Intelligence Platform
    </p>
</div>
""", unsafe_allow_html=True)
st.sidebar.page_link(
    "app.py",
    label="Dashboard"
)

st.sidebar.page_link(
    "pages/analytics.py",
    label="Analytics"
)

st.sidebar.page_link(
    "pages/data_explorer.py",
    label="Data Explorer"
)

# Page Header
st.markdown("""
<div class="page-header">
    <h1 class="page-title">Dashboard</h1>
    <p class="page-subtitle">Monitor sales performance, profitability, and business trends.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Setup & Upload Section
st.sidebar.subheader("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload sales CSV file", type=["csv"])

# Load dataset (Upload or Sample fallback)
df = None
is_sample = False

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)

        # Save uploaded dataset
        st.session_state["df"] = df

        st.sidebar.success("File loaded successfully.")

    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")
        st.error(f"Please check your CSV layout. {str(e)}")
        st.stop()

elif "df" in st.session_state:
    # Reuse uploaded dataset
    df = st.session_state["df"]

else:
    try:
        df = get_or_create_sample_data()
        st.session_state["df"] = df

        is_sample = True
        st.sidebar.info("Using default demo data.")

    except Exception as e:
        st.error(f"Failed to generate demo data: {str(e)}")
        st.stop()

# Ensure we have date-time parsing for filtering
min_date = df["Order Date"].min().to_pydatetime()
max_date = df["Order Date"].max().to_pydatetime()

# Sidebar - Filters Section
st.sidebar.subheader("Filters")

# 1. Date Range Filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle date selection tuple edge-cases
start_date = min_date
end_date = max_date
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date = datetime.combine(date_range[0], datetime.min.time())
    end_date = datetime.combine(date_range[1], datetime.max.time())
elif isinstance(date_range, tuple) and len(date_range) == 1:
    start_date = datetime.combine(date_range[0], datetime.min.time())
    end_date = max_date
elif date_range:
    start_date = datetime.combine(date_range, datetime.min.time())
    end_date = datetime.combine(date_range, datetime.max.time())

# 2. Region Filter
regions = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=regions,
    default=regions
)

# 3. Category Filter
categories = sorted(df["Category"].unique())
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=categories,
    default=categories
)

# Apply Filters to DataFrame
filtered_df = df[
    (df["Order Date"] >= pd.Timestamp(start_date)) &
    (df["Order Date"] <= pd.Timestamp(end_date)) &
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories))
]

# Save to session state for sharing with subpages
st.session_state['df'] = df
st.session_state['filtered_df'] = filtered_df

# Validation: empty data check after filters
if filtered_df.empty:
    st.warning("No data matches the selected filter criteria. Please adjust your filters in the sidebar.")
    st.stop()

status1, status2, status3, status4 = st.columns(4)

with status1:
    st.info(f"Dataset: {'Demo' if is_sample else 'Uploaded'}")

with status2:
    st.info(f"Records: {len(filtered_df):,}")

with status3:
    st.info(f"Regions: {len(selected_regions)}")

with status4:
    st.info(f"Categories: {len(selected_categories)}")

# Compute KPIs
kpis = calculate_kpis(filtered_df)

# Render KPIs row
st.markdown("<div class='section-title'>Sales Overview</div>", unsafe_allow_html=True)

margin = (
    kpis['total_profit'] / kpis['total_sales'] * 100
    if kpis['total_sales'] > 0 else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Sales", f"${kpis['total_sales']:,.0f}")

with col2:
    st.metric("Total Profit", f"${kpis['total_profit']:,.0f}")

with col3:
    st.metric("Profit Margin", f"{margin:.1f}%")

with col4:
    st.metric("Total Orders", f"{kpis['total_orders']:,}")

with col5:
    st.metric("Average Order Value", f"${kpis['average_order_value']:,.2f}")

# Render Row 1: Sales & Profit Trend (Monthly)
st.markdown("<div class='section-title'>Historical Performance</div>", unsafe_allow_html=True)
trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    with st.container(border=True):
        sales_trend_chart = plot_sales_trend(filtered_df)
        st.plotly_chart(sales_trend_chart, use_container_width=True)

with trend_col2:
    with st.container(border=True):
        profit_trend_chart = plot_profit_trend(filtered_df)
        st.plotly_chart(profit_trend_chart, use_container_width=True)

# Render Row 2: Regional Performance & Category Analysis
st.markdown("<div class='section-title'>Regional and Category Breakdown</div>", unsafe_allow_html=True)
dist_col1, dist_col2 = st.columns(2)

with dist_col1:
    with st.container(border=True):
        regional_chart = plot_regional_performance(filtered_df)
        st.plotly_chart(regional_chart, use_container_width=True)

with dist_col2:
    with st.container(border=True):
        category_chart = plot_category_analysis(filtered_df)
        st.plotly_chart(category_chart, use_container_width=True)

# Render Row 3: Sub-Category & Top Customers
st.markdown("<div class='section-title'>Sub-Category & Customer Performance</div>", unsafe_allow_html=True)
breakdown_col1, breakdown_col2 = st.columns(2)

with breakdown_col1:
    with st.container(border=True):
        subcategory_chart = plot_subcategory_analysis(filtered_df)
        st.plotly_chart(subcategory_chart, use_container_width=True)

with breakdown_col2:
    with st.container(border=True):
        cust_tab1, cust_tab2 = st.tabs(["Top Customers by Sales", "Top Customers by Profit"])
        with cust_tab1:
            top_cust_sales_chart = plot_top_customers(filtered_df, metric="Sales")
            st.plotly_chart(top_cust_sales_chart, use_container_width=True)
        with cust_tab2:
            top_cust_profit_chart = plot_top_customers(filtered_df, metric="Profit")
            st.plotly_chart(top_cust_profit_chart, use_container_width=True)

# Data Preview & Export Section
st.markdown("<div class='section-title'>Data Preview & Export</div>", unsafe_allow_html=True)
preview_expander = st.expander("Click to view dataset preview, stats, and download reports")

with preview_expander:
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.markdown(f"**Total Records (Filtered / Base):** {len(filtered_df):,} / {len(df):,}")
    with stat_col2:
        st.markdown(f"**Total Columns:** {len(df.columns)}")
    with stat_col3:
        missing_count = df.isnull().sum().sum()
        st.markdown(f"**Missing Values in Upload:** {missing_count:,}")
        
    st.markdown("##### First 10 Rows (Filtered Dataset)")
    st.dataframe(filtered_df.head(10), use_container_width=True)
    
    missing_summary = df.isnull().sum()
    if missing_summary.sum() > 0:
        st.markdown("##### Missing Values by Column")
        st.table(missing_summary[missing_summary > 0])
        
    # Download Button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"filtered_sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
