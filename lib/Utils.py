from pyspark.sql import SparkSession
from lib import ConfigReader

# Initiating spark session
def get_spark_session(env):
    if env == "LOCAL":
        return SparkSession.builder \
            .config(conf=ConfigReader.get_spark_config(env)) \
            .master("local[2]") \
            .getOrCreate()
    else:
        return SparkSession.builder \
            .config(conf=ConfigReader.get_spark_config(env)) \
            .enableHiveSupport() \
            .getOrCreate()
