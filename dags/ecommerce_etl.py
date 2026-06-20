from airflow.decorators import dag, task
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from include.config import RAW_PATH, DB_URL
from include.stagging.load_staging import load_staging_data
from include.transform.star_schema import build_star_schema
from include.kafka.consumer import consume_orders
import pandas as pd
from sqlalchemy import create_engine, text, inspect

@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ecommerce", "etl", "kafka"],
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5)
    }
)
def ecommerce_etl_pipeline():

    @task
    def extract():
        staging_data = load_staging_data()

        new_orders = consume_orders()  # list of dicts

        if len(new_orders) > 0:
            new_orders_df = pd.DataFrame(new_orders)
            staging_data["stg_orders"] = pd.concat(
                [staging_data["stg_orders"], new_orders_df],
                ignore_index=True
            ).drop_duplicates(subset=["order_id"])

        return staging_data

    @task
    def transform(staging_data):
        return build_star_schema(staging_data)
    

    @task
    def analytics():
        engine = create_engine(DB_URL)

        daily = """
        CREATE TABLE IF NOT EXISTS daily_revenue AS
        SELECT DATE(order_date) as day,
            SUM(total_amount) as revenue
        FROM fact_sales
        GROUP BY 1;
        """

        with engine.begin() as conn:
            conn.execute(daily)

        return "analytics created"
       
    @task
    def load(dfs):
        engine = create_engine(DB_URL)
        table_names = list(dfs.keys())

        with engine.begin() as conn:
            existing = set(inspect(conn).get_table_names())
            to_truncate = [t for t in table_names if t in existing]
            if to_truncate:
                conn.execute(text(f"TRUNCATE TABLE {', '.join(to_truncate)} CASCADE"))

            for table_name, df in dfs.items():
                df.to_sql(table_name, conn, if_exists="append", index=False)

        return "Loaded star schema into warehouse"

    staging = extract()
    star = transform(staging)
    load(star) >> analytics()


dag = ecommerce_etl_pipeline()