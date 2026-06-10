import streamlit as st
import pandas as pd
import plotly.express as px
from utils.metrics import get_profitability_by_category, get_customer_insights

# Configure page settings
st.set_page_config(
    page_title="Analytics",
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
    
    /* Custom SaaS Metric Cards */
    .saas-metric-card {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 1rem;
    }
    .saas-metric-label {
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #64748B !important;
        font-weight: 600 !important;
        margin-bottom: 0.25rem;
    }
    .saas-metric-value {
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
    }
    .saas-metric-subtext {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 0.25rem;
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

# Render Custom Sidebar Navigation Cards
st.sidebar.subheader("Navigation")
st.sidebar.page_link("app.py", label="Dashboard")
st.sidebar.page_link("pages/analytics.py", label="Analytics")
st.sidebar.page_link("pages/data_explorer.py", label="Data Explorer")

# Page Header
st.markdown("""
<div class="page-header">
    <h1 class="page-title">Analytics</h1>
    <p class="page-subtitle">Explore profitability margins and customer segments.</p>
</div>
""", unsafe_allow_html=True)

# Share session state loaded dataframe
if 'filtered_df' in st.session_state:
    filtered_df = st.session_state['filtered_df']
else:
    from utils.data_loader import get_or_create_sample_data
    filtered_df = get_or_create_sample_data()
    st.session_state['df'] = filtered_df
    st.session_state['filtered_df'] = filtered_df

# Check for empty dataframe
if filtered_df.empty:
    st.warning("No data available to analyze. Please upload data or adjust filters on the main dashboard page.")
    st.stop()

# Layout Tabs
tab1, tab2 = st.tabs(["Profitability Analysis", "Customer Insights"])

with tab1:
    st.markdown("<div class='section-title'>Category & Sub-Category Profitability</div>", unsafe_allow_html=True)
    
    # Calculate Profitability Metrics
    prof_metrics = get_profitability_by_category(filtered_df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="saas-metric-card">
            <div class="saas-metric-label">Most Profitable Category</div>
            <div class="saas-metric-value" style="color: #3B82F6;">{prof_metrics['most_profitable_category']}</div>
            <div class="saas-metric-subtext">Total Profit: <b>${prof_metrics['most_profitable_val']:,.2f}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="saas-metric-card">
            <div class="saas-metric-label">Least Profitable Category</div>
            <div class="saas-metric-value" style="color: #EF4444;">{prof_metrics['least_profitable_category']}</div>
            <div class="saas-metric-subtext">Total Profit: <b>${prof_metrics['least_profitable_val']:,.2f}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="saas-metric-card">
            <div class="saas-metric-label">Overall Profit Margin</div>
            <div class="saas-metric-value" style="color: #10B981;">{prof_metrics['overall_profit_margin']:.2f}%</div>
            <div class="saas-metric-subtext">Net Margin across all filtered sales</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Chart: Profit Margins by Category
    st.markdown("<div class='section-title'>Profit Margin by Category</div>", unsafe_allow_html=True)
    cat_margins_df = pd.DataFrame(list(prof_metrics['category_margins'].items()), columns=['Category', 'Margin %'])
    cat_margins_df = cat_margins_df.sort_values('Margin %', ascending=False)
    
    with st.container(border=True):
        fig_cat_margin = px.bar(
            cat_margins_df,
            x='Category',
            y='Margin %',
            text=cat_margins_df['Margin %'].apply(lambda x: f"{x:.1f}%"),
            color='Margin %',
            color_continuous_scale="Viridis",
            labels={"Margin %": "Profit Margin (%)"},
            template="plotly_dark"
        )
        fig_cat_margin.update_layout(
            title={
                'text': 'PROFIT MARGIN % BY CATEGORY',
                'y': 0.95,
                'x': 0.05,
                'xanchor': 'left',
                'yanchor': 'top',
                'font': {'size': 11, 'family': 'Inter, sans-serif', 'color': '#64748B', 'weight': 'bold'}
            },
            font=dict(family="Inter, sans-serif", size=11, color="#64748B"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        fig_cat_margin.update_xaxes(showgrid=False, linecolor="#334155", linewidth=1)
        fig_cat_margin.update_yaxes(showgrid=True, gridcolor="#334155", linecolor="#334155", linewidth=1)
        fig_cat_margin.update_traces(
            textposition='outside',
            hovertemplate="<b>Category:</b> %{x}<br><b>Margin:</b> %{y:.2f}%<extra></extra>"
        )
        st.plotly_chart(fig_cat_margin, use_container_width=True)
    
    # Detailed Table: Sub-Category Profitability
    st.markdown("<div class='section-title'>Detailed Sub-Category Financials</div>", unsafe_allow_html=True)
    sub_financials = filtered_df.groupby("Sub-Category").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    sub_financials["Profit Margin (%)"] = (sub_financials["Profit"] / sub_financials["Sales"] * 100).round(2)
    sub_financials = sub_financials.sort_values("Profit Margin (%)", ascending=False)
    
    formatted_table = sub_financials.copy()
    formatted_table["Sales"] = formatted_table["Sales"].apply(lambda x: f"${x:,.2f}")
    formatted_table["Profit"] = formatted_table["Profit"].apply(lambda x: f"${x:,.2f}")
    formatted_table["Profit Margin (%)"] = formatted_table["Profit Margin (%)"].apply(lambda x: f"{x:,.2f}%")
    
    st.dataframe(formatted_table, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("<div class='section-title'>Customer Cohort & Concentration Analysis</div>", unsafe_allow_html=True)
    
    # Calculate Customer Insights
    cust_insights = get_customer_insights(filtered_df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="saas-metric-card">
            <div class="saas-metric-label">Unique Customers</div>
            <div class="saas-metric-value" style="color: #6366F1;">{cust_insights['unique_customers']:,}</div>
            <div class="saas-metric-subtext">Total distinct customer accounts</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="saas-metric-card">
            <div class="saas-metric-label">Repeat Purchase Rate</div>
            <div class="saas-metric-value" style="color: #EC4899;">{cust_insights['repeat_rate_pct']:.1f}%</div>
            <div class="saas-metric-subtext">Repeat Customers: <b>{cust_insights['repeat_customers']:,}</b> (ordered &gt; 1 time)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="saas-metric-card">
            <div class="saas-metric-label">Top Customer Contribution</div>
            <div class="saas-metric-value" style="color: #F59E0B;">{cust_insights['top_customer_contribution_pct']:.2f}%</div>
            <div class="saas-metric-subtext">Top Customer: <b>{cust_insights['top_customer_name']}</b> (${cust_insights['top_customer_sales']:,.2f})</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Concentration chart (Pareto Principle visual)
    st.markdown("<div class='section-title'>Sales Concentration Curve</div>", unsafe_allow_html=True)
    
    cust_list = filtered_df.groupby("Customer Name")["Sales"].sum().reset_index()
    cust_list = cust_list.sort_values("Sales", ascending=False).reset_index(drop=True)
    cust_list["Cumulative Sales"] = cust_list["Sales"].cumsum()
    total_sales = cust_list["Sales"].sum()
    cust_list["Cumulative %"] = (cust_list["Cumulative Sales"] / total_sales * 100).round(2)
    cust_list["Customer Rank %"] = ((cust_list.index + 1) / len(cust_list) * 100).round(2)
    
    with st.container(border=True):
        fig_pareto = px.line(
            cust_list,
            x="Customer Rank %",
            y="Cumulative %",
            labels={"Customer Rank %": "% of Customer Base (Sorted by Sales)", "Cumulative %": "Cumulative % of Total Sales"},
            template="plotly_dark",
            color_discrete_sequence=["#3B82F6"]
        )
        fig_pareto.add_hline(y=80, line_dash="dash", line_color="#EF4444", annotation_text="80% of Sales", annotation_position="bottom right")
        fig_pareto.add_vline(x=20, line_dash="dash", line_color="#EF4444", annotation_text="Top 20% Customers", annotation_position="top left")
        
        fig_pareto.update_layout(
            title={
                'text': 'CUMULATIVE SALES CONCENTRATION (PARETO)',
                'y': 0.95,
                'x': 0.05,
                'xanchor': 'left',
                'yanchor': 'top',
                'font': {'size': 11, 'family': 'Inter, sans-serif', 'color': '#64748B', 'weight': 'bold'}
            },
            font=dict(family="Inter, sans-serif", size=11, color="#64748B"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=50, b=40)
        )
        fig_pareto.update_xaxes(showgrid=False, linecolor="#334155", linewidth=1)
        fig_pareto.update_yaxes(showgrid=True, gridcolor="#334155", linecolor="#334155", linewidth=1)
        fig_pareto.update_traces(
            hovertemplate="<b>Top % Customers:</b> %{x:.1f}%<br><b>% of Total Sales:</b> %{y:.1f}%<extra></extra>"
        )
        st.plotly_chart(fig_pareto, use_container_width=True)
    
    # Detailed customer rankings list
    st.markdown("<div class='section-title'>Top 25 Customers and Sales Contribution</div>", unsafe_allow_html=True)
    top_25 = cust_list.head(25).copy()
    top_25["Contribution %"] = (top_25["Sales"] / total_sales * 100).round(2)
    
    order_counts = filtered_df.groupby("Customer Name").size().reset_index(name="Order Count")
    top_25 = top_25.merge(order_counts, on="Customer Name", how="left")
    
    top_25_formatted = top_25[["Customer Name", "Sales", "Order Count", "Contribution %"]].copy()
    top_25_formatted["Sales"] = top_25_formatted["Sales"].apply(lambda x: f"${x:,.2f}")
    top_25_formatted["Contribution %"] = top_25_formatted["Contribution %"].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(top_25_formatted, use_container_width=True, hide_index=True)
