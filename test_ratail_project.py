import pytest
from lib.Utils import get_spark_session
from lib.DataReader import read_customers, read_orders
from lib.DataManipulation import filter_closed_orders
from lib.ConfigReader import get_app_config

@pytest.mark.parametrize("func, expected_count", [
    (read_customers, 12435),
    (read_orders, 68884),
])

def test_data_reading(spark, func, expected_count):
    """Test data reading functions."""
    assert func(spark, 'LOCAL').count() == expected_count, f"Expected {expected_count} records, but got different count."

def test_filter_closed_orders(spark):
    """Test filtering closed orders."""
    df = read_orders(spark, 'LOCAL')
    closed_orders_count = filter_closed_orders(df).count()
    expected_count = 7556
    assert closed_orders_count == expected_count, f"Expected {expected_count} closed orders, but got {closed_orders_count}."

def test_app_config():
    """Test application config retrieval."""
    config = get_app_config('LOCAL')
    expected_path = 'data/orders.csv'
    assert config['orders.file.path'] == expected_path, f"Expected '{expected_path}', but got '{config['orders.file.path']}'."

# Run tests using: python -m pytest -v
