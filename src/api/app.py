import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from fastapi import FastAPI

from queries.create_indexes import create_indexes
from queries.queries import (
    query_1_by_city,
    query_2_by_customer,
    query_3_by_product,
    query_4_by_payment_status,
    query_5_city_and_status
)

from aggregations.sales_by_city import sales_by_city
from aggregations.top_products import top_products
from aggregations.top_customers import top_customers
from aggregations.sales_by_status import sales_by_status
from aggregations.sales_by_payment import sales_by_payment

from materialized_views.daily_sales_summary import refresh_daily_sales
from materialized_views.top_products_summary import refresh_top_products

from jobs.run_job import (
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
