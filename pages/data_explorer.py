import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="Data Explorer",
    layout="wide"
)

# Custom CSS for uniform dark SaaS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
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
        margin-bottom: 1.5rem;
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
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        color: #64748B !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        text-transform: uppercase;
    }
    
    /* Metric Widget Overrides */
    div[data-testid="stMetric"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
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
    
    /* Search block card */
    .search-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Render Custom Sidebar Navigation Cards
st.sidebar.subheader("Navigation")
st.sidebar.page_link("app.py", label="Dashboard")
st.sidebar.page_link("pages/analytics.py", label="Analytics")
st.sidebar.page_link("pages/data_explorer.py", label="Data Explorer")

# Page Header
st.markdown("""
<div class="page-header">
    <h1 class="page-title">Data Explorer</h1>
    <p class="page-subtitle">Search, filter, and export raw transaction logs.</p>
</div>
""", unsafe_allow_html=True)

# Share session state loaded dataframe
if 'df' in st.session_state:
    df = st.session_state['df']
    filtered_df = st.session_state['filtered_df']
else:
    from utils.data_loader import get_or_create_sample_data
    df = get_or_create_sample_data()
    st.session_state['df'] = df
    st.session_state['filtered_df'] = df
    filtered_df = df

# Filter Options
st.markdown("<div class='section-title'>Search and Filter Filters</div>", unsafe_allow_html=True)

with st.container(border=True):
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Customer Name or Sub-Category",
            value="",
            placeholder="Type customer or product sub-category..."
        )
        
    with col2:
        regions = ["All Regions"] + sorted(list(df["Region"].unique()))
        selected_region = st.selectbox("Filter by Region", options=regions)
        
    with col3:
        categories = ["All Categories"] + sorted(list(df["Category"].unique()))
        selected_category = st.selectbox("Filter by Category", options=categories)

# Apply Search & Dropdown Filters
explorer_df = df.copy()

if search_query:
    q = search_query.lower()
    explorer_df = explorer_df[
        explorer_df["Customer Name"].str.lower().str.contains(q) |
        explorer_df["Sub-Category"].str.lower().str.contains(q)
    ]
    
if selected_region != "All Regions":
    explorer_df = explorer_df[explorer_df["Region"] == selected_region]
    
if selected_category != "All Categories":
    explorer_df = explorer_df[explorer_df["Category"] == selected_category]

# Summary Statistics Row
st.markdown("<div class='section-title'>Explorer Metrics</div>", unsafe_allow_html=True)
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric(
        label="Records Found",
        value=f"{len(explorer_df):,}"
    )
with stat_col2:
    st.metric(
        label="Total Sales",
        value=f"${explorer_df['Sales'].sum():,.2f}"
    )
with stat_col3:
    st.metric(
        label="Total Profit",
        value=f"${explorer_df['Profit'].sum():,.2f}"
    )
with stat_col4:
    margin = (explorer_df['Profit'].sum() / explorer_df['Sales'].sum() * 100) if explorer_df['Sales'].sum() > 0 else 0
    st.metric(
        label="Profit Margin",
        value=f"{margin:.2f}%"
    )

# Render main data table
st.markdown("<div class='section-title'>Transaction Table</div>", unsafe_allow_html=True)

# Standard sortable Streamlit dataframe
st.dataframe(explorer_df, use_container_width=True, hide_index=True)

# CSV Export Button
csv_data = explorer_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Filtered Result as CSV",
    data=csv_data,
    file_name=f"explorer_sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)
