import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

from pymongo import MongoClient
from config.settings import MONGO_URI, DATABASE_NAME, VALID_COLLECTION


client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

collection = db[VALID_COLLECTION]


def top_customers():

    pipeline = [

        {
            "$group": {
                "_id": "$customer_id",
                "customer_name": {
                    "$first": "$customer_name"
                },
                "total_orders": {
                    "$sum": 1
                },
                "total_spent": {
                    "$sum": "$price"
                }
            }
        },

        {
            "$sort": {
                "total_spent": -1
            }
        }

    ]

    return list(collection.aggregate(pipeline))


if __name__ == "__main__":

    result = top_customers()

    for row in result[:10]:
        print(row)