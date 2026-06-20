import pandas as pd


def build_star_schema(staging_data: dict):

    orders = staging_data["stg_orders"]
    items = staging_data["stg_items"]
    customers = staging_data["stg_customers"]
    payments = staging_data["stg_payments"]

    df = (
        orders.merge(items, on="order_id")
              .merge(customers, on="customer_id")
              .merge(payments, on="order_id")
    )

    df = df.dropna()

    df["quantity"] = 1
    df["total_amount"] = df["price"] * df["quantity"]

    df["order_date"] = pd.to_datetime(df["order_purchase_timestamp"])

    dim_customers = (
        df[["customer_id"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_customers["customer_key"] = dim_customers.index + 1

    dim_products = (
        df[["product_id"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_products["product_key"] = dim_products.index + 1

    dim_payment = (
        df[["payment_type"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_payment["payment_key"] = dim_payment.index + 1

    dim_date = (
        df[["order_date"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_date["date_key"] = dim_date.index + 1
    dim_date["year"] = dim_date["order_date"].dt.year
    dim_date["month"] = dim_date["order_date"].dt.month
    dim_date["day"] = dim_date["order_date"].dt.day
    dim_date["weekday"] = dim_date["order_date"].dt.day_name()

    fact_sales = df.copy()

    fact_sales = fact_sales.merge(dim_customers, on="customer_id", how="left")
    fact_sales = fact_sales.merge(dim_products, on="product_id", how="left")
    fact_sales = fact_sales.merge(dim_payment, on="payment_type", how="left")
    fact_sales = fact_sales.merge(dim_date, on="order_date", how="left")

    fact_sales = fact_sales[[
        "order_id",
        "customer_key",
        "product_key",
        "payment_key",
        "date_key",
        "quantity",
        "price",
        "total_amount",
    ]]

    return {
        "fact_sales": fact_sales,
        "dim_customers": dim_customers,
        "dim_products": dim_products,
        "dim_payment": dim_payment,
        "dim_date": dim_date,
    }
