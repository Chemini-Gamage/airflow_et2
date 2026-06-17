import pandas as pd

def load_staging_data():
    base_path = "include/data/Ecommerce Order Dataset/train"

    customers = pd.read_csv(f"{base_path}/df_Customers.csv")
    orders = pd.read_csv(f"{base_path}/df_Orders.csv")
    items = pd.read_csv(f"{base_path}/df_OrderItems.csv")
    payments = pd.read_csv(f"{base_path}/df_Payments.csv")

    return {
        "stg_customers": customers,
        "stg_orders": orders,
        "stg_items": items,
        "stg_payments": payments,
    }
