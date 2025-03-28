import pytest
from lib.DataReader import read_customers, read_orders
from lib.DataManipulation import filter_closed_orders, count_orders_by_state, filter_orders
from lib.ConfigReader import get_app_config

@pytest.mark.parametrize("func, expected_count", [
    (read_customers, 12435),
    (read_orders, 68884),
])

def test_data_reading(spark, func, expected_count):
    """Test data reading functions."""
    assert func(spark, 'LOCAL').count() == expected_count, f"Expected {expected_count} records, but got different count."

@pytest.mark.transformation()
def test_filter_closed_orders(spark):
    """Test filtering closed orders."""
    df = read_orders(spark, 'LOCAL')
    closed_orders_count = filter_closed_orders(df).count()
    expected_count = 7556
    assert closed_orders_count == expected_count, f"Expected {expected_count} closed orders, but got {closed_orders_count}."

@pytest.mark.skip("skiping it")
def test_app_config():
    """Test application config retrieval."""
    config = get_app_config('LOCAL')
    expected_path = 'data/orders.csv'
    assert config['orders.file.path'] == expected_path, f"Expected '{expected_path}', but got '{config['orders.file.path']}'."

@pytest.mark.transformation()
def test_count_orders_by_state(spark, expected_results):
    df = read_customers(spark, 'LOCAL')
    actual_results = count_orders_by_state(df)
    assert actual_results.collect() == expected_results.collect(), f"Expected '{expected_results}', but got '{actual_results}'."

@pytest.mark.latest
def test_check_closed_orders(spark):
    orders_df = read_orders(spark, 'LOCAL')
    actual_result = filter_orders(orders_df, "CLOSED").count()
    expected_result = 7556
    assert actual_result == expected_result, f"Expected '{expected_result}', but got '{actual_result}'."

@pytest.mark.latest
def test_check_pendingpayment_orders(spark):
    orders_df = read_orders(spark, 'LOCAL')
    actual_result = filter_orders(orders_df, "PENDING_PAYMENT").count()
    expected_result = 15030
    assert actual_result == expected_result, f"Expected '{expected_result}', but got '{actual_result}'."

@pytest.mark.latest
def test_check_complete_orders(spark):
    orders_df = read_orders(spark, 'LOCAL')
    actual_result = filter_orders(orders_df, "COMPLETE").count()
    expected_result = 22900
    assert actual_result == expected_result, f"Expected '{expected_result}', but got '{actual_result}'."

@pytest.mark.counttest
@pytest.mark.parametrize("status, expected_result", [
    ("CLOSED", 7556),
    ("COMPLETE", 22900),
    ("PENDING_PAYMENT", 15030),
])
def test_orders_count(spark, status, expected_result):
    """Test that filtering orders by status returns the expected count."""
    orders_df = read_orders(spark, 'LOCAL')
    filtered_df = filter_orders(orders_df, status)
    actual_result = filtered_df.count()
    assert actual_result == expected_result, (
        f"Mismatch for status '{status}': Expected {expected_result}, but got {actual_result}."
    )

# Run tests using: python -m pytest -v
