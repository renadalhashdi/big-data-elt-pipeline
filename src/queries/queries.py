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


def query_1_by_city(city):

    return list(
        collection.find(
            {"city": city},
            {"_id": 0}
        ).limit(10)
    )


def query_2_by_customer(customer_id):

    return list(
        collection.find(
            {"customer_id": customer_id},
            {"_id": 0}
        ).limit(10)
    )


def query_3_by_product(product):

    return list(
        collection.find(
            {"product": product},
            {"_id": 0}
        ).limit(10)
    )


def query_4_by_payment_status(status):

    return list(
        collection.find(
            {"payment_status": status},
            {"_id": 0}
        ).limit(10)
    )


def query_5_city_and_status(city, status):

    return list(
        collection.find(
            {
                "city": city,
                "status": status
            },
            {"_id": 0}
        ).limit(10)
    )


if __name__ == "__main__":

    print("Query 1:")
    print(query_1_by_city("تعز"))

    print("\nQuery 2:")
    print(query_2_by_customer("عميل-1"))

    print("\nQuery 3:")
    print(query_3_by_product("هاتف سامسونج A54"))

    print("\nQuery 4:")
    print(query_4_by_payment_status("تم الدفع"))

    print("\nQuery 5:")
    print(query_5_city_and_status("تعز", "مؤكد"))