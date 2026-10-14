-- ============================================
-- E-commerce Sales Analysis - Business Queries
-- Database: retail.db (table: retail)
-- ============================================

-- Q1: Overall KPIs
SELECT 
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(DISTINCT Invoice) AS total_orders,
    COUNT(DISTINCT "Customer ID") AS total_customers,
    ROUND(SUM(Revenue) / COUNT(DISTINCT Invoice), 2) AS avg_order_value
FROM retail;

-- Q2: Top 10 Countries by Revenue
SELECT 
    Country,
    ROUND(SUM(Revenue), 2) AS revenue,
    COUNT(DISTINCT Invoice) AS orders
FROM retail
GROUP BY Country
ORDER BY revenue DESC
LIMIT 10;

-- Q3: Monthly Revenue Trend
SELECT 
    strftime('%Y-%m', InvoiceDate) AS month,
    ROUND(SUM(Revenue), 2) AS revenue,
    COUNT(DISTINCT Invoice) AS orders
FROM retail
GROUP BY month
ORDER BY month;

-- Q4: Top 10 Customers by Revenue
SELECT 
    "Customer ID" AS customer_id,
    ROUND(SUM(Revenue), 2) AS revenue,
    COUNT(DISTINCT Invoice) AS orders
FROM retail
GROUP BY "Customer ID"
ORDER BY revenue DESC
LIMIT 10;

-- Q5: Top 10 Products by Revenue
SELECT 
    Description,
    ROUND(SUM(Revenue), 2) AS revenue,
    SUM(Quantity) AS total_quantity
FROM retail
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;

-- Q6: Average Order Value by Country
SELECT 
    Country,
    ROUND(SUM(Revenue) / COUNT(DISTINCT Invoice), 2) AS avg_order_value,
    COUNT(DISTINCT Invoice) AS orders
FROM retail
GROUP BY Country
HAVING orders > 50
ORDER BY avg_order_value DESC
LIMIT 10;

-- Q7: Repeat vs One-time Customers
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
GROUP BY customer_type;

-- Q8: Best Selling Months
SELECT 
    strftime('%Y-%m', InvoiceDate) AS month,
    ROUND(SUM(Revenue), 2) AS revenue
FROM retail
GROUP BY month
ORDER BY revenue DESC
LIMIT 5;
