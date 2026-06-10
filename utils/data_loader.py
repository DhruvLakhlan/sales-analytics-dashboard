import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Expected columns for dashboard validation
REQUIRED_COLUMNS = [
    "Order Date",
    "Sales",
    "Profit",
    "Region",
    "Category",
    "Sub-Category",
    "Customer Name"
]

def load_data(file_or_path) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame and perform initial preprocessing.
    
    Args:
        file_or_path: File path (str) or file-like object from st.file_uploader.
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame.
        
    Raises:
        ValueError: If there is an issue reading the file or missing required columns.
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_or_path)
    except Exception as e:
        raise ValueError(f"Failed to read the CSV file. Error: {str(e)}")
    
    # Clean column names (strip whitespace)
    df.columns = [col.strip() for col in df.columns]
    
    # Validate required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"The uploaded file is missing the following required columns: {', '.join(missing_cols)}. "
            f"Please ensure your dataset contains: {', '.join(REQUIRED_COLUMNS)}."
        )
        
    # Preprocess Order Date
    try:
        # Try dynamic parsing of date formats
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
        # Check if there are any unparseable dates
        if df["Order Date"].isnull().all():
            raise ValueError("Could not parse 'Order Date' column. Please verify it contains valid date formats (e.g., YYYY-MM-DD).")
    except Exception as e:
        raise ValueError(f"Error parsing 'Order Date' column: {str(e)}")
        
    # Coerce numeric columns and handle missing values
    df["Sales"] = pd.to_numeric(df["Sales"], errors='coerce').fillna(0.0)
    df["Profit"] = pd.to_numeric(df["Profit"], errors='coerce').fillna(0.0)
    
    # Strip string columns to avoid whitespace-based group errors
    str_cols = ["Region", "Category", "Sub-Category", "Customer Name"]
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
        
    return df

def generate_mock_data(output_path: str) -> pd.DataFrame:
    """
    Generate a realistic Kaggle Superstore-like dataset and save it to output_path.
    
    Args:
        output_path: Path where the CSV should be saved.
        
    Returns:
        pd.DataFrame: The generated DataFrame.
    """
    np.random.seed(42)
    n_rows = 1500
    
    # Setup values
    regions = ["West", "East", "Central", "South"]
    categories = {
        "Technology": ["Phones", "Accessories", "Copiers", "Machines"],
        "Furniture": ["Chairs", "Furnishings", "Bookcases", "Tables"],
        "Office Supplies": ["Paper", "Binders", "Storage", "Appliances", "Art", "Envelopes", "Labels", "Fasteners", "Supplies"]
    }
    
    customers = [
        "Claire Gute", "Pete Kaisen", "Brosina Hoffman", "Andrew Allen", "Irene Maddox",
        "Harold Ryan", "Ken Black", "Sandra Flanagan", "Emily Burns", "Eric Hoffmann",
        "Lena Creighton", "Ryan Crowe", "Georgia Nippi", "Tracy Blumstein", "Gary Hansen",
        "Albert Patina", "Linda Cazzolari", "Stewart Rivera", "Yoseph Carroll", "Bobby Osgood",
        "John Lee", "Alejandro Grove", "Zusha Benson", "Arthur Prichep", "Joel Eaton",
        "Maria Etezadi", "Nick Crecia", "Valerie Mitchum", "Toby Swindell", "Paul Prost"
    ]
    
    # Generate random components
    regions_chosen = np.random.choice(regions, size=n_rows)
    cat_keys = list(categories.keys())
    cats_chosen = np.random.choice(cat_keys, size=n_rows, p=[0.3, 0.25, 0.45])
    
    subcats_chosen = []
    for cat in cats_chosen:
        subcats_chosen.append(np.random.choice(categories[cat]))
        
    customers_chosen = np.random.choice(customers, size=n_rows)
    
    # Generate realistic dates (between 2023-01-01 and 2025-12-31)
    start_date = datetime(2023, 1, 1)
    date_offsets = np.random.randint(0, 365 * 3, size=n_rows)
    dates_chosen = [start_date + timedelta(days=int(offset)) for offset in date_offsets]
    
    # Generate Sales (skewed distribution)
    # Most items are cheap ($10-$100), some are expensive ($500-$2000)
    base_sales = np.random.exponential(scale=150, size=n_rows) + 5
    # Boost copiers, machines, tables, chairs
    for i in range(n_rows):
        sub = subcats_chosen[i]
        if sub in ["Copiers", "Machines", "Tables"]:
            base_sales[i] *= np.random.uniform(3.0, 8.0)
        elif sub in ["Chairs", "Phones", "Bookcases"]:
            base_sales[i] *= np.random.uniform(1.5, 4.0)
    sales = np.round(base_sales, 2)
    
    # Generate Profit
    # Furniture/Tables are often negative or low profit, Copiers are high profit
    profit = np.zeros(n_rows)
    for i in range(n_rows):
        cat = cats_chosen[i]
        sub = subcats_chosen[i]
        s = sales[i]
        
        if sub == "Tables":
            # Tables often lose money
            profit[i] = s * np.random.uniform(-0.35, 0.10)
        elif sub == "Copiers":
            # Copiers are highly profitable
            profit[i] = s * np.random.uniform(0.35, 0.55)
        elif cat == "Furniture":
            # Low margin overall
            profit[i] = s * np.random.uniform(-0.15, 0.25)
        elif cat == "Technology":
            # Good margins
            profit[i] = s * np.random.uniform(0.10, 0.45)
        else:
            # Office Supplies: steady margins
            profit[i] = s * np.random.uniform(0.05, 0.35)
            
    profit = np.round(profit, 2)
    
    # Construct DataFrame
    mock_df = pd.DataFrame({
        "Order Date": [d.strftime("%Y-%m-%d") for d in dates_chosen],
        "Sales": sales,
        "Profit": profit,
        "Region": regions_chosen,
        "Category": cats_chosen,
        "Sub-Category": subcats_chosen,
        "Customer Name": customers_chosen
    })
    
    # Ensure asset directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    mock_df.to_csv(output_path, index=False)
    
    return load_data(output_path)

def get_or_create_sample_data() -> pd.DataFrame:
    """
    Get existing sample data or generate a new one if it does not exist.
    """
    # Look for assets folder in current workspace or parent of utils
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_path = os.path.join(base_dir, "assets", "sample_superstore.csv")
    
    if os.path.exists(sample_path):
        try:
            return load_data(sample_path)
        except Exception:
            # If loaded with error (corrupted file etc), regenerate
            return generate_mock_data(sample_path)
    else:
        return generate_mock_data(sample_path)
