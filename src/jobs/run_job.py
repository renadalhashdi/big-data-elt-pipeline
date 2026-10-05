import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from jobs.scheduler import (
    refresh_materialized_views_job,
    daily_report_job
)


if __name__ == "__main__":

    print("Running Materialized Views Job...")
    refresh_materialized_views_job()

    print("Running Daily Report Job...")
    daily_report_job()

    print("Jobs completed")