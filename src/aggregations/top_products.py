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


def top_products():

    pipeline = [

        {
            "$group": {
                "_id": "$product",
                "total_quantity": {
                    "$sum": "$quantity"
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

    result = top_products()

    for row in result[:10]:
        print(row)