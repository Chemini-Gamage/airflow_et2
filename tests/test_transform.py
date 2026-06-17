from include.transform.transform import transform_data

def test_transform():
    result = transform_data()
    assert len(result["fact_sales"]) > 0