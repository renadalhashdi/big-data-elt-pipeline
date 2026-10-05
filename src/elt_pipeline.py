import os
import sys
import time
from datetime import datetime
from uuid import uuid4

from pymongo import MongoClient, UpdateOne


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


from config.settings import (
    MONGO_URI,
    DATABASE_NAME,
    RAW_COLLECTION,
    VALID_COLLECTION,
    QUARANTINE_COLLECTION
)

from quality_rules import clean_record
from metrics import save_metrics



def upsert_records(collection, records):

    if not records:
        return 0, 0, 0


    collection.create_index(
        "id_order",
        unique=True
    )


    operations = []


    for record in records:

        operations.append(
            UpdateOne(
                {
                    "id_order": record["id_order"]
                },
                {
                    "$set": record
                },
                upsert=True
            )
        )


    result = collection.bulk_write(
        operations
    )


    return (
        result.matched_count,
        result.modified_count,
        len(result.upserted_ids)
    )



def run_pipeline():

    start_time = time.time()

    run_id = str(uuid4())


    client = MongoClient(MONGO_URI)

    db = client[DATABASE_NAME]


    raw = db[RAW_COLLECTION]

    valid = db[VALID_COLLECTION]

    quarantine = db[QUARANTINE_COLLECTION]


    valid_records = []

    quarantine_records = []


    total_records = 0

    corrected_count = 0



    for record in raw.find({}, {"_id": 0}):

        total_records += 1


        record["run_id"] = run_id

        record["processed_at"] = str(
            datetime.now()
        )


        cleaned_record, errors, corrections = clean_record(
            record
        )


        if corrections:

            cleaned_record["corrections"] = corrections

            corrected_count += 1



        if errors:

            cleaned_record["errors"] = errors

            cleaned_record["classification"] = "Quarantined"

            quarantine_records.append(
                cleaned_record
            )


        else:

            if corrections:

                cleaned_record["classification"] = "Corrected"

            else:

                cleaned_record["classification"] = "Valid"


            valid_records.append(
                cleaned_record
            )



    matched_valid, modified_valid, inserted_valid = upsert_records(
        valid,
        valid_records
    )


    matched_quarantine, modified_quarantine, inserted_quarantine = upsert_records(
        quarantine,
        quarantine_records
    )


    execution_time = time.time() - start_time



    save_metrics(

        total_records=total_records,

        validated_records=len(valid_records),

        quarantine_records=len(quarantine_records),

        execution_time=execution_time,

        run_id=run_id,

        engine_used="ELT_PIPELINE",

        corrected_records=corrected_count,

        inserted_records=(
            inserted_valid + inserted_quarantine
        ),

        updated_records=(
            modified_valid + modified_quarantine
        )
    )



    print("======================")

    print("Run ID:", run_id)

    print("Total:", total_records)

    print("Valid/Corrected:", len(valid_records))

    print("Corrected:", corrected_count)

    print("Quarantine:", len(quarantine_records))

    print(
        "Inserted:",
        inserted_valid + inserted_quarantine
    )

    print(
        "Updated:",
        modified_valid + modified_quarantine
    )

    print("======================")



if __name__ == "__main__":

    run_pipeline()