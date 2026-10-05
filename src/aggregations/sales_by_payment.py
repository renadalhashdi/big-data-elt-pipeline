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


def sales_by_payment():

    pipeline = [

        {
            "$group": {
                "_id": "$payment_method",
                "orders_count": {
                    "$sum": 1
                },
                "total_sales": {
                    "$sum": "$price"
                }
            }
        },

        {
            "$sort": {
                "total_sales": -1
            }
        }

    ]

    return list(collection.aggregate(pipeline))


if __name__ == "__main__":

    result = sales_by_payment()

    for row in result:
        print(row)