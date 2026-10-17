import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.elt_pipeline import run_pipeline
from src.file_router import route_file
from src.batch_loader import load_to_mongodb
from src.spark_loader import load_with_spark


from fastapi import FastAPI

from src.queries.create_indexes import create_indexes
from src.queries.queries import (
    query_1_by_city,
    query_2_by_customer,
    query_3_by_product,
    query_4_by_payment_status,
    query_5_city_and_status
)

from src.aggregations.sales_by_city import sales_by_city
from src.aggregations.top_products import top_products
from src.aggregations.top_customers import top_customers
from src.aggregations.sales_by_status import sales_by_status
from src.aggregations.sales_by_payment import sales_by_payment

from src.materialized_views.daily_sales_summary import refresh_daily_sales
from src.materialized_views.top_products_summary import refresh_top_products

from src.jobs.run_job import (
    refresh_materialized_views_job,
    daily_report_job
)


app = FastAPI(
    title="Big Data ELT Pipeline API",
    version="2.0"
)


@app.post("/ingest")
def ingest():

    from main import main

    file_path = "data/orders_clean.csv"

    main(file_path)

    return {
        "message": "Ingestion completed"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }


@app.post("/indexes")
def indexes():
    create_indexes()

    return {
        "message": "Indexes created"
    }


@app.get("/queries")
def queries():

    return {
        "available_queries": [
            "city",
            "customer",
            "product",
            "payment_status",
            "city_status"
        ]
    }


@app.get("/queries/city/{city}")
def query_city(city: str):

    return query_1_by_city(city)


@app.get("/queries/customer/{customer_id}")
def query_customer(customer_id: str):

    return query_2_by_customer(customer_id)


@app.get("/queries/product/{product}")
def query_product(product: str):

    return query_3_by_product(product)


@app.get("/aggregations")
def aggregations():

    return {
        "available_reports": [
            "sales_by_city",
            "top_products",
            "top_customers",
            "sales_by_status",
            "sales_by_payment"
        ]
    }


@app.get("/aggregations/sales_by_city")
def aggregation_city():

    return sales_by_city()


@app.get("/aggregations/top_products")
def aggregation_products():

    return top_products()


@app.get("/aggregations/top_customers")
def aggregation_customers():

    return top_customers()


@app.get("/aggregations/sales_by_status")
def aggregation_status():

    return sales_by_status()


@app.get("/aggregations/sales_by_payment")
def aggregation_payment():

    return sales_by_payment()


@app.post("/refresh-mv")
def refresh_mv():

    refresh_daily_sales()
    refresh_top_products()

    return {
        "message": "Materialized Views refreshed"
    }


@app.get("/jobs")
def jobs():

    return {
        "jobs": [
            "refresh_materialized_views",
            "daily_report"
        ]
    }


@app.post("/jobs/run")
def run_jobs():

    refresh_materialized_views_job()
    daily_report_job()

    return {
        "message": "Jobs executed"
    }
def main(file_path):

    print("======================")
    print("DATA PIPELINE START")
    print("======================")

    engine = route_file(file_path)

    print("Selected Engine:", engine)

    if engine == "PYTHON_BATCH":

        print("Running Python Batch Loader...")
        load_to_mongodb(file_path)

    elif engine == "PYSPARK":

        print("Running PySpark Loader...")
        load_with_spark(file_path)

    else:
        print("Unknown Engine")
        return

    print("======================")
    print("Running ELT Pipeline")
    print("======================")

    run_pipeline()
if __name__ == "__main__":
    file_path = "data/orders_clean.csv"
    main(file_path)