import pandas as pd
import numpy as np

def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate core KPIs: Total Sales, Total Profit, Total Orders, Average Order Value.
    
    Args:
        df: Filtered or unfiltered sales DataFrame.
        
    Returns:
        dict: KPI metrics containing float and int values.
    """
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "total_orders": 0,
            "average_order_value": 0.0
        }
        
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    
    average_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    
    return {
        "total_sales": float(total_sales),
        "total_profit": float(total_profit),
        "total_orders": int(total_orders),
        "average_order_value": float(average_order_value)
    }

def get_profitability_by_category(df: pd.DataFrame) -> dict:
    """
    Find profitability metrics across product categories.
    
    Args:
        df: Sales DataFrame.
        
    Returns:
        dict: Profitability details (most profitable, least profitable, profit margins).
    """
    if df.empty:
        return {
            "most_profitable_category": "N/A",
            "most_profitable_val": 0.0,
            "least_profitable_category": "N/A",
            "least_profitable_val": 0.0,
            "overall_profit_margin": 0.0,
            "category_margins": {}
        }
        
    # Group by Category and sum sales & profit
    cat_summary = df.groupby("Category").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    
    # Calculate margins
    cat_summary["Margin"] = (cat_summary["Profit"] / cat_summary["Sales"] * 100).fillna(0.0)
    
    # Find most and least profitable by absolute profit
    most_prof_idx = cat_summary["Profit"].idxmax() if not cat_summary.empty else None
    least_prof_idx = cat_summary["Profit"].idxmin() if not cat_summary.empty else None
    
    most_prof = cat_summary.loc[most_prof_idx]["Category"] if most_prof_idx is not None else "N/A"
    most_prof_val = cat_summary.loc[most_prof_idx]["Profit"] if most_prof_idx is not None else 0.0
    
    least_prof = cat_summary.loc[least_prof_idx]["Category"] if least_prof_idx is not None else "N/A"
    least_prof_val = cat_summary.loc[least_prof_idx]["Profit"] if least_prof_idx is not None else 0.0
    
    # Overall margin
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0
    
    # Category margins to dict
    cat_margins = dict(zip(cat_summary["Category"], cat_summary["Margin"]))
    
    return {
        "most_profitable_category": most_prof,
        "most_profitable_val": float(most_prof_val),
        "least_profitable_category": least_prof,
        "least_profitable_val": float(least_prof_val),
        "overall_profit_margin": float(overall_margin),
        "category_margins": cat_margins
    }

def get_customer_insights(df: pd.DataFrame) -> dict:
    """
    Calculate customer insights: Unique customers, repeat rate, and top customer contribution.
    
    Args:
        df: Sales DataFrame.
        
    Returns:
        dict: Customer insights.
    """
    if df.empty:
        return {
            "unique_customers": 0,
            "repeat_customers": 0,
            "repeat_rate_pct": 0.0,
            "top_customer_name": "N/A",
            "top_customer_contribution_pct": 0.0,
            "top_customer_sales": 0.0
        }
        
    # Count of unique customers
    unique_cust_names = df["Customer Name"].nunique()
    
    # Count how many times each customer ordered
    cust_orders = df["Customer Name"].value_counts()
    repeat_customers = (cust_orders > 1).sum()
    repeat_rate = (repeat_customers / unique_cust_names * 100) if unique_cust_names > 0 else 0.0
    
    # Customer sales aggregation
    cust_sales = df.groupby("Customer Name")["Sales"].sum().reset_index()
    total_sales = df["Sales"].sum()
    
    if not cust_sales.empty and total_sales > 0:
        top_cust_idx = cust_sales["Sales"].idxmax()
        top_cust_name = cust_sales.loc[top_cust_idx]["Customer Name"]
        top_cust_sales = cust_sales.loc[top_cust_idx]["Sales"]
        top_contribution = (top_cust_sales / total_sales * 100)
    else:
        top_cust_name = "N/A"
        top_cust_sales = 0.0
        top_contribution = 0.0
        
    return {
        "unique_customers": int(unique_cust_names),
        "repeat_customers": int(repeat_customers),
        "repeat_rate_pct": float(repeat_rate),
        "top_customer_name": top_cust_name,
        "top_customer_contribution_pct": float(top_contribution),
        "top_customer_sales": float(top_cust_sales)
    }
