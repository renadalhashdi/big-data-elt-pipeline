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

view = db["daily_sales_summary"]


def refresh_daily_sales():

    view.delete_many({})


    pipeline = [

        {
            "$group": {
                "_id": {
                    "$substr": [
                        "$order_date",
                        0,
                        10
                    ]
                },
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
                "_id": 1
            }
        }

    ]


    result = list(source.aggregate(pipeline))


    if result:
        view.insert_many(result)


    print(
        "daily_sales_summary refreshed"
    )


if __name__ == "__main__":
    refresh_daily_sales()