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

source = db[VALID_COLLECTION]

view = db["top_products_summary"]


def refresh_top_products():

    view.delete_many({})


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


    result = list(source.aggregate(pipeline))


    if result:
        view.insert_many(result)


    print(
        "top_products_summary refreshed"
    )


if __name__ == "__main__":
    refresh_top_products()