from airflow.decorators import dag, task
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from include.config import RAW_PATH, DB_URL
from include.stagging.load_staging import load_staging_data
from include.transform.star_schema import build_star_schema

@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ecommerce", "etl"],
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5)
    }
)
def ecommerce_etl_pipeline():

    @task
    def extract():
        return load_staging_data()

    @task
    def transform(staging_data):
        return build_star_schema(staging_data)

    @task
    def load(dfs):
        engine = create_engine(DB_URL)

        for table_name, df in dfs.items():
            df.to_sql(
                table_name,
                engine,
                if_exists="append",
                index=False
            )

        return "Loaded star schema into warehouse"

    staging = extract()
    star = transform(staging)
    load(star)


dag = ecommerce_etl_pipeline()