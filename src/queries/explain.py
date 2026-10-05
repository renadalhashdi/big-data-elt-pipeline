import sys
import os
import json

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


def run_explain():

    collection = db[VALID_COLLECTION]

    results = {}

    queries = {

        "query_city": {
            "city": "تعز"
        },

        "query_product": {
            "product": "هاتف سامسونج A54"
        },

        "query_compound": {
            "city": "تعز",
            "status": "قيد الانتظار"
        }

    }


    for name, query in queries.items():

        explain_result = db.command(
            "explain",
            {
                "find": VALID_COLLECTION,
                "filter": query
            },
            verbosity="executionStats"
        )


        stats = explain_result["executionStats"]


        results[name] = {

            "executionTimeMillis":
                stats["executionTimeMillis"],

            "totalDocsExamined":
                stats["totalDocsExamined"],

            "documentsReturned":
                stats["nReturned"]

        }


    os.makedirs(
        "reports",
        exist_ok=True
    )


    with open(
        "reports/explain_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )


    print("Explain results saved")


if __name__ == "__main__":
    run_explain()