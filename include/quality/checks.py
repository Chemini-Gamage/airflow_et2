def validate_fact_table(df):
    assert df["order_id"].notnull().all(), "order_id has nulls"
    assert df["total_amount"].min() >= 0, "negative revenue found"
    assert len(df) > 0, "fact table is empty"

    return True