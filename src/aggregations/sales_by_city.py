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


def sales_by_city():

    pipeline = [

        {
            "$group": {
                "_id": "$city",
                "total_sales": {
                    "$sum": "$price"
                },
                "orders_count": {
                    "$sum": 1
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

    result = sales_by_city()

    for row in result[:10]:
        print(row)