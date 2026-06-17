from sqlalchemy import text
from datetime import datetime

def get_last_run(engine, table_name):
    query = f"""
        SELECT last_run
        FROM etl_watermark
        WHERE table_name = '{table_name}'
    """

    result = engine.execute(text(query)).fetchone()

    if result:
        return result[0]
    return datetime(2020, 1, 1)