import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from pymongo import MongoClient
from config.settings import MONGO_URI, DATABASE_NAME, VALID_COLLECTION


client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

collection = db[VALID_COLLECTION]


def create_indexes():

    print("Creating indexes...")


    # Index 1
    collection.create_index(
        [("city", 1)],
        name="city_index"
    )


    # Index 2
    collection.create_index(
        [("product", 1)],
        name="product_index"
    )


    # Compound Index
    collection.create_index(
        [
            ("city", 1),
            ("status", 1)
        ],
        name="city_status_compound_index"
    )


    print("Indexes created successfully")


if __name__ == "__main__":
    create_indexes()