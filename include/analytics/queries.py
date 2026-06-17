ANALYTICS_QUERIES = {

"total_revenue": """
SELECT SUM(total_amount) FROM fact_sales;
""",

"monthly_revenue": """
SELECT
    d.year,
    d.month,
    SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.order_date = d.order_date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
""",

"top_products": """
SELECT
    product_id,
    SUM(total_amount) AS revenue
FROM fact_sales
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;
""",

"payment_distribution": """
SELECT
    payment_type,
    COUNT(*) AS orders
FROM fact_sales
GROUP BY payment_type
ORDER BY orders DESC;
"""
}