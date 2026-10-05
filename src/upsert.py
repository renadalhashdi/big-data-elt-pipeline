import os
import sys

from pymongo import MongoClient, UpdateOne


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


from config.settings import (
    MONGO_URI,
    DATABASE_NAME,
    VALID_COLLECTION
)


def upsert_validated_data():

    client = MongoClient(MONGO_URI)

    db = client[DATABASE_NAME]

    collection = db[VALID_COLLECTION]


    # إنشاء Unique Index على id_order
    collection.create_index(
        "id_order",
        unique=True
    )


    records = list(collection.find({}, {"_id":0}))


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


    if operations:

        result = collection.bulk_write(operations)

        print("Matched:", result.matched_count)
        print("Modified:", result.modified_count)
        print("Upserted:", len(result.upserted_ids))


if __name__ == "__main__":

    upsert_validated_data()