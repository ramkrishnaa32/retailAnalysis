import pytest
from lib.Utils import get_spark_session

@pytest.fixture(scope="session")
def spark():
    """Fixture to initialize and return a Spark session."""
    spark_session = get_spark_session('LOCAL')
    yield spark_session
    spark_session.stop()

@pytest.fixture
def expected_results(spark):
    "Give the expected results"
    schema = "state string, count int"
    df = spark.read \
              .format("csv") \
              .schema(schema) \
              .load("data/test_result/state_aggregate.csv")
    return df