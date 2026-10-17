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

from src.quality_rules import clean_record
from src.metrics import save_metrics



def upsert_records(collection, records):

    if not records:
        return 0, 0, 0
    existing_indexes = collection.index_information()

    if "id_order_1" in existing_indexes:
        old_index = existing_indexes["id_order_1"]

        if not old_index.get("sparse", False):
            collection.drop_index("id_order_1")

    collection.create_index(
        "id_order",
        unique=True,
        sparse=True
    )
 

    operations = []
    records_without_id = []

    for record in records:

        id_order = record.get("id_order")

        if id_order:
            operations.append(
                UpdateOne(
                    {
                        "id_order": id_order
                    },
                    {
                        "$set": record
                    },
                    upsert=True
                )
            )
        else:
            record_without_id = record.copy()
            record_without_id.pop("id_order", None)
            records_without_id.append(record_without_id)


        matched_count = 0
        modified_count = 0
        inserted_count = 0

    if operations:
        result = collection.bulk_write(
            operations
        )

        matched_count = result.matched_count
        modified_count = result.modified_count
        inserted_count = len(result.upserted_ids)

    if records_without_id:
        result = collection.insert_many(
            records_without_id
        )

        inserted_count += len(result.inserted_ids)

    return (
        matched_count,
        modified_count,
        inserted_count
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


        print("Cleaning record:", total_records)


        cleaned_record, errors, corrections = clean_record(
            record
        )


        print("Record cleaned")


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