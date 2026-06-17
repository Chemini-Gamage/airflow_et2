import pandas as pd

def build_star_schema(staging_data: dict):

    orders = staging_data["stg_orders"]
    items = staging_data["stg_items"]
    customers = staging_data["stg_customers"]
    payments = staging_data["stg_payments"]

    df = orders.merge(items, on="order_id") \
               .merge(customers, on="customer_id") \
               .merge(payments, on="order_id")

    df = df.dropna()

    df["quantity"] = 1
    df["total_amount"] = df["price"] * df["quantity"]

    df["order_date"] = pd.to_datetime(df["order_purchase_timestamp"])

    fact_sales = df[[
        "order_id",
        "product_id",
        "customer_id",
        "payment_type",
        "order_date",
        "price",
        "quantity",
        "total_amount"
    ]]

    dim_customers = customers[["customer_id"]].drop_duplicates()
    dim_products = items[["product_id"]].drop_duplicates()
    dim_payment = payments[["payment_type"]].drop_duplicates()

    dim_date = fact_sales[["order_date"]].drop_duplicates()
    dim_date["year"] = dim_date["order_date"].dt.year
    dim_date["month"] = dim_date["order_date"].dt.month
    dim_date["day"] = dim_date["order_date"].dt.day

    return {
        "fact_sales": fact_sales,
        "dim_customers": dim_customers,
        "dim_products": dim_products,
        "dim_payment": dim_payment,
        "dim_date": dim_date
    }