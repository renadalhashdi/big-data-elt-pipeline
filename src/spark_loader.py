import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType
)


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


from config.settings import (
    MONGO_URI,
    DATABASE_NAME,
    RAW_COLLECTION
)



def load_with_spark(file_path):

    spark = (
        SparkSession.builder
        .appName("BigDataPipeline")
        .master("local[2]")

        .config(
            "spark.driver.memory",
            "6g"
        )

        .config(
            "spark.executor.memory",
            "6g"
        )

        .config(
            "spark.jars.packages",
            "org.mongodb.spark:mongo-spark-connector_2.13:11.1.0"
        )

        .config(
            "spark.mongodb.write.connection.uri",
            MONGO_URI
        )

        .getOrCreate()
    )


    schema = StructType([

        StructField("id_order", StringType(), True),

        StructField("order_date", StringType(), True),

        StructField("status", StringType(), True),

        StructField("customer_id", StringType(), True),

        StructField("customer_name", StringType(), True),

        StructField("phone", StringType(), True),

        StructField("email", StringType(), True),

        StructField("city", StringType(), True),

        StructField("district", StringType(), True),

        StructField("delivery_type", StringType(), True),

        StructField("delivery_cost", StringType(), True),

        StructField("payment_method", StringType(), True),

        StructField("payment_status", StringType(), True),

        StructField("payment_amount", StringType(), True),

        StructField("currency", StringType(), True),

        StructField("price", StringType(), True),

        StructField("product", StringType(), True)

    ])



    df = (
        spark.read
        .option("header", True)
        .option("quote", '"')
        .option("escape", '"')
        .option("multiLine", True)
        .schema(schema)
        .csv(file_path)
    )


    print("Input Records:")
    print(df.count())


    print("Writing Raw MongoDB...")


    (
        df.write
        .format("mongodb")
        .mode("overwrite")

        .option(
            "database",
            DATABASE_NAME
        )

        .option(
            "collection",
            RAW_COLLECTION
        )

        .option(
            "connection.uri",
            MONGO_URI
        )

        .save()
    )


    print("Spark Write Raw: SUCCESS")


    spark.stop()



if __name__ == "__main__":

    load_with_spark(
        "data/orders_clean.csv"
    )