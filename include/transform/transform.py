import pandas as pd

def transform_data():

    # -------------------------
    # LOAD DATA
    # -------------------------
    customers = pd.read_csv("data/Ecommerce Order Dataset/train/df_Customers.csv")
    orders = pd.read_csv("data/Ecommerce Order Dataset/train/df_Orders.csv")
    items = pd.read_csv("data/Ecommerce Order Dataset/train/df_OrderItems.csv")
    payments = pd.read_csv("data/Ecommerce Order Dataset/train/df_Payments.csv")

    # -------------------------
    # MERGE TABLES
    # -------------------------
    df = orders.merge(items, on="order_id") \
               .merge(customers, on="customer_id") \
               .merge(payments, on="order_id")

    df = df.dropna()
    df = df[df["order_date"] > last_run_date]

    # -------------------------
    # BUSINESS LOGIC FIXES
    # -------------------------
    df["quantity"] = 1
    df["total_amount"] = df["quantity"] * df["price"]

    # ensure datetime
    if "order_purchase_timestamp" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_purchase_timestamp"])
    else:
        df["order_date"] = pd.to_datetime(df["order_date"])

    # -------------------------
    # FACT TABLE
    # -------------------------
    df_fact = df[[
        "order_id",
        "product_id",
        "customer_id",
        "payment_type",
        "order_date",
        "price",
        "quantity",
        "total_amount"
    ]].copy()

    # -------------------------
    # DIM TABLES
    # -------------------------
    df_customers = df[["customer_id"]].drop_duplicates()

    df_products = df[["product_id"]].drop_duplicates()

    df_payment = df[["payment_type"]].drop_duplicates()

    df_date = df[["order_date"]].drop_duplicates().copy()
    df_date["year"] = df_date["order_date"].dt.year
    df_date["month"] = df_date["order_date"].dt.month
    df_date["day"] = df_date["order_date"].dt.day
    df_date["weekday"] = df_date["order_date"].dt.day_name()

    # -------------------------
    # RETURN STAR SCHEMA
    # -------------------------
    return {
        "fact_sales": df_fact,
        "dim_customers": df_customers,
        "dim_products": df_products,
        "dim_payment": df_payment,
        "dim_date": df_date
    }