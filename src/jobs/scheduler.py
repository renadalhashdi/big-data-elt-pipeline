import sys
import os
import time
from datetime import datetime
import schedule


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from materialized_views.daily_sales_summary import refresh_daily_sales
from materialized_views.top_products_summary import refresh_top_products


LOG_FILE = "reports/jobs_log.txt"


def write_log(job_name, start, end, status):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{job_name} | "
            f"Start: {start} | "
            f"End: {end} | "
            f"Status: {status}\n"
        )


def refresh_materialized_views_job():

    start = datetime.now()

    try:

        refresh_daily_sales()
        refresh_top_products()

        status = "SUCCESS"

    except Exception as e:

        status = f"FAILED: {e}"


    end = datetime.now()

    write_log(
        "refresh_materialized_views",
        start,
        end,
        status
    )


def daily_report_job():

    start = datetime.now()

    try:

        print("Daily report generated")

        status = "SUCCESS"

    except Exception as e:

        status = f"FAILED: {e}"


    end = datetime.now()

    write_log(
        "daily_report",
        start,
        end,
        status
    )


def run_scheduler():

    schedule.every().day.at("00:00").do(
        refresh_materialized_views_job
    )

    schedule.every().day.at("01:00").do(
        daily_report_job
    )


    print("Scheduler started")


    while True:

        schedule.run_pending()

        time.sleep(60)


if __name__ == "__main__":

    run_scheduler()