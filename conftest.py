import pytest
from lib.Utils import get_spark_session

@pytest.fixture(scope="session")
def spark():
    """Fixture to initialize and return a Spark session."""
    spark_session = get_spark_session('LOCAL')
    yield spark_session
    spark_session.stop()