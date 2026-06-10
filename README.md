# 📊 Premium Sales Analytics Dashboard

A modern, production-ready Sales Analytics Dashboard built in Python using **Streamlit**, **Pandas**, **NumPy**, and **Plotly**. This application is designed to ingest sales transaction logs (such as the Kaggle Superstore dataset), clean and parse fields, and generate an interactive dashboard for regional, categorical, and customer segment insights.

---

## 🌟 Features

- **Dynamic Interactive KPI Indicators**: Track Total Sales, Net Profit, Profit Margin, Order Count, and Average Order Value (AOV).
- **Interactive Data Visualizations**: Hover-responsive charts for monthly sales/profit trends, regional breakdowns, category/sub-category composition, and top customers.
- **Advanced Customer Insights**: Analyze retention rate, unique customer counts, and sales concentration curves (Pareto Principle representation).
- **Robust CSV Ingestion & Validation**: Automatic date parsing, whitespace clearing, missing numeric value imputation, and validation alerts for missing columns.
- **Local Data Download**: Export the filtered report dataset back to a clean CSV at the click of a button.
- **Mock Demo Data Generation**: Automatically generates a realistic Kaggle Superstore-like dataset containing 1,500+ records to immediately demonstrate the dashboard if no user file is uploaded.
- **Glassmorphic Responsive Design**: Tailored theme styling utilizing CSS variables that adapt natively to dark and light modes.

---

## 📋 Required CSV Data Schema

Your uploaded CSV file must contain the following headers (the uploader will clean leading/trailing spaces in the headers and cells):

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **Order Date** | Date / Datetime | Date of order. Supports formats like `YYYY-MM-DD` or `MM/DD/YYYY`. | `2024-05-18` |
| **Sales** | Numeric (Float) | Revenue amount of the row. Do not include currency symbols ($). | `249.99` |
| **Profit** | Numeric (Float) | Net profit or loss value. Can be negative for losses. | `45.20` |
| **Region** | String / Text | Geographical territory of the transaction. | `West` |
| **Category** | String / Text | High-level product vertical classification. | `Technology` |
| **Sub-Category** | String / Text | Specific product subgroup classification. | `Phones` |
| **Customer Name**| String / Text | Name of the buyer. | `Claire Gute` |

---

## ⚙️ Local Setup and Execution

Follow these steps to run the application on your local machine:

### 1. Prerequisites
Ensure you have **Python 3.9** or newer installed. You can check your version by running:
```bash
python --version
```

### 2. Install Dependencies
Open a command prompt or terminal in the project's root folder (`sales-dashboard/`) and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
Start the Streamlit development server:
```bash
streamlit run app.py
```

Streamlit will automatically bundle the app and launch a browser window pointing to:
`http://localhost:8501`

---

## 🚀 Deploying to Streamlit Cloud

Streamlit Cloud provides free, instant deployment for your Streamlit applications directly from GitHub:

1. **Upload to GitHub**: Create a repository and push the contents of the `sales-dashboard` folder. The structure should have `app.py` in the root of the repository:
   ```text
   ├── app.py
   ├── requirements.txt
   ├── pages/
   │   ├── analytics.py
   │   └── about.py
   └── utils/
       ├── data_loader.py
       ├── charts.py
       └── metrics.py
   ```
2. **Log into Streamlit**: Go to [Streamlit Community Cloud](https://share.streamlit.io/) and authorize with your GitHub account.
3. **Deploy App**:
   - Click the **New app** button.
   - Choose your repository, branch, and specify the main file path as `app.py`.
   - Click **Deploy!**
4. **Access the Application**: Your app will build, install the contents of `requirements.txt`, and become active on a public, shareable URL.

---

## 📂 Project Architecture

```text
sales-dashboard/
│
├── app.py                  # Streamlit entry point, layout structuring, sidebar filters
├── requirements.txt        # Python dependency manager
├── README.md               # User manual
│
├── pages/
│   ├── analytics.py        # Analytics subpage (margins, Pareto customer concentration)
│   └── about.py            # Reference guide (CSV layouts, local/cloud setup)
│
├── utils/
│   ├── data_loader.py      # CSV parser, required column validation, mock data generator
│   ├── metrics.py          # Metric engine (KPIs, profit margins, retention metrics)
│   └── charts.py           # Visualization engine (Plotly line, bar, pie, and donut charts)
│
└── assets/
    └── sample_superstore.csv # Mock Superstore CSV generated dynamically on first boot
```
