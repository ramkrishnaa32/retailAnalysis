from pyspark.sql.functions import *

# Filter order_status = 'CLOSED'
def filter_closed_orders(orders_df):
    df = orders_df.filter("order_status = 'CLOSED'")
    return df

# Joining both dataframes
def join_orders_customers(orders_df, customers_df):
    df = orders_df.join(customers_df, "customer_id")
    return df

# GroupBy at state level
def count_orders_by_state(joined_df):
    df = joined_df.groupBy('state').count()
    return df