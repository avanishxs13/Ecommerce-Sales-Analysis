import kagglehub
path = kagglehub.dataset_download("mashlyn/online-retail-ii-uci")
print("Path:", path)

import os

# Folder mein kya-kya hai dekho
for file in os.listdir(path):
    print(file)

    import pandas as pd
    import os

    # Path
    path = r"C:\Users\AVANISH\.cache\kagglehub\datasets\mashlyn\online-retail-ii-uci\versions\3"
    file_name = "online_retail_II.csv"

    # Load
    df = pd.read_csv(os.path.join(path, file_name), encoding="ISO-8859-1")

    print("=" * 50)
    print("BEFORE CLEANING")
    print("=" * 50)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("\nMissing values:\n", df.isnull().sum())
    print("\nFirst 5 rows:\n", df.head())

    # ---------- CLEANING ----------

    # 1. Cancelled invoices hatao (Invoice 'C' se start)
    df = df[~df['Invoice'].astype(str).str.startswith('C')]

    # 2. Negative ya zero Quantity hatao
    df = df[df['Quantity'] > 0]

    # 3. Zero ya negative Price hatao
    df = df[df['Price'] > 0]

    # 4. Missing Customer ID hatao
    df = df.dropna(subset=['Customer ID'])

    # 5. Date convert
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # 6. Revenue column banao
    df['Revenue'] = df['Quantity'] * df['Price']

    print("\n" + "=" * 50)
    print("AFTER CLEANING")
    print("=" * 50)
    print("Shape:", df.shape)
    print("\nData types:\n", df.dtypes)
    print("\nSample:\n", df.head())

    # 7. Cleaned file save karo
    output_path = r"C:\Users\AVANISH\PycharmProjects\Pythonprojects\online_retail_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Cleaned file saved: {output_path}")


import sqlite3
import pandas as pd

# Cleaned CSV load karo
df = pd.read_csv("online_retail_cleaned.csv")

# SQLite database banao
conn = sqlite3.connect("retail.db")
df.to_sql("retail", conn, if_exists="replace", index=False)

print("✅ Database ready: retail.db")
print(f"Rows: {len(df):,}")

import sqlite3
import pandas as pd

# Cleaned CSV load karo
df = pd.read_csv("online_retail_cleaned.csv")

# SQLite database banao
conn = sqlite3.connect("retail.db")
df.to_sql("retail", conn, if_exists="replace", index=False)

print("✅ Database ready: retail.db")
print(f"Rows: {len(df):,}")

# ==========================================
# 🎯 SQL ANALYSIS — 8 BUSINESS QUESTIONS
# ==========================================

def run_query(title, query):
    print("\n" + "=" * 60)
    print(f"📊 {title}")
    print("=" * 60)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result

# Q1: Overall KPIs
run_query("Q1: Overall KPIs", """
    SELECT 
        ROUND(SUM(Revenue), 2) AS total_revenue,
        COUNT(DISTINCT Invoice) AS total_orders,
        COUNT(DISTINCT "Customer ID") AS total_customers,
        ROUND(SUM(Revenue) / COUNT(DISTINCT Invoice), 2) AS avg_order_value
    FROM retail
""")

# Q2: Top 10 Countries by Revenue
run_query("Q2: Top 10 Countries by Revenue", """
    SELECT 
        Country,
        ROUND(SUM(Revenue), 2) AS revenue,
        COUNT(DISTINCT Invoice) AS orders
    FROM retail
    GROUP BY Country
    ORDER BY revenue DESC
    LIMIT 10
""")

# Q3: Monthly Revenue Trend
run_query("Q3: Monthly Revenue Trend", """
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS month,
        ROUND(SUM(Revenue), 2) AS revenue,
        COUNT(DISTINCT Invoice) AS orders
    FROM retail
    GROUP BY month
    ORDER BY month
""")

# Q4: Top 10 Customers by Revenue
run_query("Q4: Top 10 Customers by Revenue", """
    SELECT 
        "Customer ID" AS customer_id,
        ROUND(SUM(Revenue), 2) AS revenue,
        COUNT(DISTINCT Invoice) AS orders
    FROM retail
    GROUP BY "Customer ID"
    ORDER BY revenue DESC
    LIMIT 10
""")

# Q5: Top 10 Products by Revenue
run_query("Q5: Top 10 Products by Revenue", """
    SELECT 
        Description,
        ROUND(SUM(Revenue), 2) AS revenue,
        SUM(Quantity) AS total_quantity
    FROM retail
    GROUP BY Description
    ORDER BY revenue DESC
    LIMIT 10
""")

# Q6: Average Order Value by Country (Top 10)
run_query("Q6: Avg Order Value by Country (Top 10)", """
    SELECT 
        Country,
        ROUND(SUM(Revenue) / COUNT(DISTINCT Invoice), 2) AS avg_order_value,
        COUNT(DISTINCT Invoice) AS orders
    FROM retail
    GROUP BY Country
    HAVING orders > 50
    ORDER BY avg_order_value DESC
    LIMIT 10
""")

# Q7: Repeat vs One-time Customers
run_query("Q7: Repeat vs One-time Customers", """
    SELECT 
        CASE 
            WHEN order_count = 1 THEN 'One-time'
            ELSE 'Repeat'
        END AS customer_type,
        COUNT(*) AS num_customers
    FROM (
        SELECT "Customer ID", COUNT(DISTINCT Invoice) AS order_count
        FROM retail
        GROUP BY "Customer ID"
    )
    GROUP BY customer_type
""")

# Q8: Best Selling Month
run_query("Q8: Best Selling Month", """
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS month,
        ROUND(SUM(Revenue), 2) AS revenue
    FROM retail
    GROUP BY month
    ORDER BY revenue DESC
    LIMIT 5
""")

conn.close()
print("\n✅ All queries executed successfully!")