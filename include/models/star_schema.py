def get_star_schema(dfs: dict):
    return {
        "fact_sales": dfs["fact_sales"],
        "dim_customers": dfs["dim_customers"],
        "dim_products": dfs["dim_products"],
        "dim_payment": dfs["dim_payment"],
        "dim_date": dfs["dim_date"],
    }