import os
import json
from datetime import datetime


def save_metrics(
    total_records,
    validated_records,
    quarantine_records,
    execution_time,
    run_id=None,
    engine_used=None,
    corrected_records=0,
    inserted_records=0,
    updated_records=0
):

    metrics = {

        "run_id": run_id,

        "engine_used": engine_used,

        "execution_time": execution_time,

        "total_records": total_records,

        "validated_records": validated_records,

        "corrected_records": corrected_records,

        "quarantine_records": quarantine_records,

        "inserted_records": inserted_records,

        "updated_records": updated_records,

        "consistency_check": (
            total_records ==
            validated_records + quarantine_records
        ),

        "status": "success",

        "created_at": str(datetime.now())

    }


    os.makedirs(
        "reports",
        exist_ok=True
    )


    with open(
        "reports/results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4,
            ensure_ascii=False
        )


    print("Metrics saved successfully")