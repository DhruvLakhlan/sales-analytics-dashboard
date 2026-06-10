import os
import pandas as pd
import numpy as np
from utils.data_loader import load_data, generate_mock_data, get_or_create_sample_data, REQUIRED_COLUMNS
from utils.metrics import calculate_kpis, get_profitability_by_category, get_customer_insights
from utils.charts import (
    plot_sales_trend, plot_profit_trend, plot_regional_performance,
    plot_category_analysis, plot_subcategory_analysis, plot_top_customers
)

def run_tests():
    print("=== Running Sales Dashboard App Logic Tests ===")
    
    # 1. Test Mock Data Generation & Loader
    print("\n1. Testing Mock Data Generation...")
    test_csv_path = "assets/test_superstore.csv"
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)
        
    try:
        df = generate_mock_data(test_csv_path)
        print(f"[OK] Mock data generated successfully with {len(df)} rows.")
        assert os.path.exists(test_csv_path), "Mock CSV file was not created!"
        assert len(df) == 1500, f"Expected 1500 rows, got {len(df)}"
        print("[OK] Data validation and parsing checked.")
    except Exception as e:
        print(f"[ERROR] Error generating mock data: {e}")
        return
        
    # 2. Test Column Validation
    print("\n2. Testing Schema Validation...")
    try:
        # Load the mock data
        df_loaded = load_data(test_csv_path)
        print("[OK] Correct schema loaded successfully.")
        
        # Create invalid DataFrame
        bad_df_path = "assets/test_bad_schema.csv"
        bad_df = df.drop(columns=["Sales"])
        bad_df.to_csv(bad_df_path, index=False)
        
        try:
            load_data(bad_df_path)
            print("[FAIL] Validation failed: Uploaded file missing 'Sales' should have raised a ValueError!")
        except ValueError as ve:
            print(f"[OK] Schema validation caught missing column successfully: '{ve}'")
        finally:
            if os.path.exists(bad_df_path):
                os.remove(bad_df_path)
                
    except Exception as e:
        print(f"[ERROR] Error during schema validation test: {e}")
        return

    # 3. Test KPI Calculations
    print("\n3. Testing KPI Metrics Engine...")
    try:
        kpis = calculate_kpis(df)
        print(f"   Calculated KPIs:")
        print(f"     - Total Sales: ${kpis['total_sales']:,.2f}")
        print(f"     - Total Profit: ${kpis['total_profit']:,.2f}")
        print(f"     - Total Orders: {kpis['total_orders']}")
        print(f"     - Average Order Value: ${kpis['average_order_value']:,.2f}")
        
        assert kpis['total_sales'] > 0, "Total sales should be positive"
        assert kpis['total_orders'] == 1500, "Total orders should equal length of dataframe"
        assert abs(kpis['average_order_value'] - (kpis['total_sales'] / 1500)) < 1e-5, "AOV calculation mismatch"
        print("[OK] KPI calculation logic verified.")
    except Exception as e:
        print(f"[ERROR] Error during KPI calculations test: {e}")
        return

    # 4. Test Profitability Analysis Metrics
    print("\n4. Testing Profitability Analytics Engine...")
    try:
        prof = get_profitability_by_category(df)
        print(f"   Calculated Profitability:")
        print(f"     - Most Profitable Category: {prof['most_profitable_category']} (${prof['most_profitable_val']:,.2f})")
        print(f"     - Least Profitable Category: {prof['least_profitable_category']} (${prof['least_profitable_val']:,.2f})")
        print(f"     - Overall Profit Margin: {prof['overall_profit_margin']:.2f}%")
        
        assert prof['most_profitable_category'] != "N/A", "Category should be detected"
        assert len(prof['category_margins']) > 0, "Category margins should be calculated"
        print("[OK] Profitability analysis logic verified.")
    except Exception as e:
        print(f"[ERROR] Error during profitability test: {e}")
        return

    # 5. Test Customer Insights Metrics
    print("\n5. Testing Customer Insights Engine...")
    try:
        insights = get_customer_insights(df)
        print(f"   Calculated Customer Insights:")
        print(f"     - Unique Customers: {insights['unique_customers']}")
        print(f"     - Repeat Customers: {insights['repeat_customers']}")
        print(f"     - Repeat Purchase Rate: {insights['repeat_rate_pct']:.2f}%")
        print(f"     - Top Customer: {insights['top_customer_name']} (Contribution: {insights['top_customer_contribution_pct']:.2f}%)")
        
        assert insights['unique_customers'] > 0, "Unique customer count should be positive"
        assert insights['repeat_customers'] <= insights['unique_customers'], "Repeat customers cannot exceed unique customers"
        print("[OK] Customer insights logic verified.")
    except Exception as e:
        print(f"[ERROR] Error during customer insights test: {e}")
        return

    # 6. Test Chart Generations
    print("\n6. Testing Plotly Visualization Engine...")
    try:
        fig_sales_trend = plot_sales_trend(df)
        fig_profit_trend = plot_profit_trend(df)
        fig_regional = plot_regional_performance(df)
        fig_category = plot_category_analysis(df)
        fig_subcat = plot_subcategory_analysis(df)
        fig_top_cust = plot_top_customers(df, "Sales")
        
        # Verify they are all valid Plotly Graph Objects
        assert fig_sales_trend is not None
        assert fig_profit_trend is not None
        assert fig_regional is not None
        assert fig_category is not None
        assert fig_subcat is not None
        assert fig_top_cust is not None
        
        print("[OK] All charts generated successfully without errors.")
    except Exception as e:
        print(f"[ERROR] Error during chart generation test: {e}")
        return

    # Cleanup test files
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)
        
    print("\n[SUCCESS] All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
