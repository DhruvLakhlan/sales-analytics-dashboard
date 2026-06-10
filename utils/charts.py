import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Neutral SaaS Color Palette (Stripe/Vercel Inspired)
COLOR_PALETTE = {
    "sales": "#3B82F6",        # Stripe Blue / Vercel Indigo
    "profit": "#10B981",       # SaaS Emerald Green
    "warning": "#F59E0B",      # Muted Amber
    "danger": "#EF4444",       # Muted Red
    "violet": "#6366F1",       # Indigo-Violet
    "slate_text": "#F8FAFC",   # High-contrast light text
    "slate_muted": "#94A3B8",  # Low-contrast slate text
    "grid_line": "#334155",    # Dark grid line slate
    "colors_discrete": ["#3B82F6", "#10B981", "#6366F1", "#F59E0B", "#EF4444", "#EC4899"]
}

def _apply_premium_layout(fig, title: str, show_legend: bool = True):
    """
    Apply a consistent, minimal SaaS dark visual styling to a Plotly figure.
    """
    fig.update_layout(
        title={
            'text': title.upper(),
            'y': 0.95,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 13, 'family': 'Inter, sans-serif', 'color': COLOR_PALETTE["slate_muted"], 'weight': 'bold'}
        },
        font=dict(
            family="Inter, sans-serif",
            size=11,
            color=COLOR_PALETTE["slate_muted"]
        ),
        paper_bgcolor="rgba(0,0,0,0)", # Transparent to inherit card bg
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot canvas
        margin=dict(l=40, r=20, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="left",
            x=0.05,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10, color=COLOR_PALETTE["slate_muted"])
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",  # Slate Card BG
            bordercolor=COLOR_PALETTE["grid_line"],
            font_size=11,
            font_color=COLOR_PALETTE["slate_text"],
            font_family="Inter, sans-serif"
        )
    )
    
    # Clean gridlines and axes matching SaaS theme
    fig.update_xaxes(
        showgrid=False,
        linecolor=COLOR_PALETTE["grid_line"],
        linewidth=1,
        ticks="outside",
        tickcolor=COLOR_PALETTE["grid_line"],
        tickfont=dict(color=COLOR_PALETTE["slate_muted"]),
        title_font=dict(color=COLOR_PALETTE["slate_muted"])
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=COLOR_PALETTE["grid_line"],
        linecolor=COLOR_PALETTE["grid_line"],
        linewidth=1,
        tickfont=dict(color=COLOR_PALETTE["slate_muted"]),
        title_font=dict(color=COLOR_PALETTE["slate_muted"])
    )
    
    return fig

def plot_sales_trend(df: pd.DataFrame):
    """
    Plot a monthly line chart of Sales over time.
    """
    if df.empty:
        return px.line(title="No Data Available")
        
    df_copy = df.copy()
    df_copy["Year-Month"] = df_copy["Order Date"].dt.strftime("%Y-%m")
    monthly_data = df_copy.groupby("Year-Month")["Sales"].sum().reset_index()
    monthly_data = monthly_data.sort_values("Year-Month")
    
    fig = px.line(
        monthly_data,
        x="Year-Month",
        y="Sales",
        markers=True,
        labels={"Sales": "Sales ($)", "Year-Month": "Month"},
        template="plotly_dark",
        color_discrete_sequence=[COLOR_PALETTE["sales"]]
    )
    
    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6),
        hovertemplate="<b>Month:</b> %{x}<br><b>Sales:</b> $%{y:,.2f}<extra></extra>"
    )
    
    return _apply_premium_layout(fig, "Monthly Sales Trend", show_legend=False)

def plot_profit_trend(df: pd.DataFrame):
    """
    Plot a monthly line chart of Profit over time.
    """
    if df.empty:
        return px.line(title="No Data Available")
        
    df_copy = df.copy()
    df_copy["Year-Month"] = df_copy["Order Date"].dt.strftime("%Y-%m")
    monthly_data = df_copy.groupby("Year-Month")["Profit"].sum().reset_index()
    monthly_data = monthly_data.sort_values("Year-Month")
    
    fig = px.line(
        monthly_data,
        x="Year-Month",
        y="Profit",
        markers=True,
        labels={"Profit": "Profit ($)", "Year-Month": "Month"},
        template="plotly_dark",
        color_discrete_sequence=[COLOR_PALETTE["profit"]]
    )
    
    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6),
        hovertemplate="<b>Month:</b> %{x}<br><b>Profit:</b> $%{y:,.2f}<extra></extra>"
    )
    
    return _apply_premium_layout(fig, "Monthly Profit Trend", show_legend=False)

def plot_regional_performance(df: pd.DataFrame):
    """
    Grouped bar chart showing Sales and Profit by region.
    """
    if df.empty:
        return px.bar(title="No Data Available")
        
    region_data = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    
    melted = region_data.melt(
        id_vars=["Region"], 
        value_vars=["Sales", "Profit"],
        var_name="Metric",
        value_name="Amount"
    )
    
    fig = px.bar(
        melted,
        x="Region",
        y="Amount",
        color="Metric",
        barmode="group",
        color_discrete_map={
            "Sales": COLOR_PALETTE["sales"],
            "Profit": COLOR_PALETTE["profit"]
        },
        template="plotly_dark"
    )
    
    fig.update_traces(
        hovertemplate="<b>Region:</b> %{x}<br><b>%{customdata[0]}:</b> $%{y:,.2f}<extra></extra>",
        customdata=np.stack((melted['Metric'],), axis=-1)
    )
    
    return _apply_premium_layout(fig, "Performance by Region")

def plot_category_analysis(df: pd.DataFrame):
    """
    Donut chart showing Sales contribution of Category.
    """
    if df.empty:
        return px.pie(title="No Data Available")
        
    cat_data = df.groupby("Category")["Sales"].sum().reset_index()
    
    fig = px.pie(
        cat_data,
        names="Category",
        values="Sales",
        hole=0.5, # Slightly larger hole for cleaner donut chart
        color_discrete_sequence=COLOR_PALETTE["colors_discrete"],
        template="plotly_dark"
    )
    
    fig.update_traces(
        textinfo="percent",
        hovertemplate="<b>Category:</b> %{label}<br><b>Sales:</b> $%{value:,.2f}<br><b>Share:</b> %{percent:.1%}<extra></extra>"
    )
    
    return _apply_premium_layout(fig, "Sales by Category")

def plot_subcategory_analysis(df: pd.DataFrame):
    """
    Sorted bar chart of top-performing Sub-Categories.
    """
    if df.empty:
        return px.bar(title="No Data Available")
        
    sub_data = df.groupby("Sub-Category")[["Sales", "Profit"]].sum().reset_index()
    sub_data = sub_data.sort_values("Sales", ascending=True)
    
    fig = px.bar(
        sub_data,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        color_continuous_scale="Tealgrn", # Minimal teal green theme
        labels={"Sales": "Sales ($)", "Sub-Category": "Sub-Category"},
        template="plotly_dark"
    )
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Profit ($)", 
            thickness=12, 
            len=0.7, 
            title_font=dict(color=COLOR_PALETTE["slate_muted"]),
            tickfont=dict(color=COLOR_PALETTE["slate_muted"])
        )
    )
    fig.update_traces(
        hovertemplate="<b>Sub-Category:</b> %{y}<br><b>Sales:</b> $%{x:,.2f}<br><b>Profit:</b> $%{customdata[0]:,.2f}<extra></extra>",
        customdata=np.stack((sub_data['Profit'],), axis=-1)
    )
    
    return _apply_premium_layout(fig, "Sub-Category Performance", show_legend=False)

def plot_top_customers(df: pd.DataFrame, metric="Sales"):
    """
    Horizontal bar chart of top 10 customers.
    """
    if df.empty:
        return px.bar(title="No Data Available")
        
    cust_data = df.groupby("Customer Name")[[metric]].sum().reset_index()
    cust_data = cust_data.sort_values(metric, ascending=True).tail(10)
    
    color = COLOR_PALETTE["sales"] if metric == "Sales" else COLOR_PALETTE["profit"]
    
    fig = px.bar(
        cust_data,
        x=metric,
        y="Customer Name",
        orientation="h",
        labels={metric: f"Total {metric} ($)", "Customer Name": "Customer Name"},
        template="plotly_dark",
        color_discrete_sequence=[color]
    )
    
    fig.update_traces(
        hovertemplate=f"<b>Customer:</b> %{{y}}<br><b>{metric}:</b> $%{{x:,.2f}}<extra></extra>"
    )
    
    return _apply_premium_layout(fig, f"Top Customers by {metric}", show_legend=False)
