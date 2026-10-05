import os
import sys
import csv
import time

from pymongo import MongoClient


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


from config.settings import (
    MONGO_URI,
    DATABASE_NAME,
    RAW_COLLECTION
)


BATCH_SIZE = 1000


def load_to_mongodb(file_path):

    client = MongoClient(MONGO_URI)

    db = client[DATABASE_NAME]

    collection = db[RAW_COLLECTION]


    batch = []
    batch_number = 1
    total_inserted = 0


    start_time = time.time()


    with open(file_path, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)


        for row in reader:

            batch.append(row)


            if len(batch) >= BATCH_SIZE:

                insert_start = time.time()

                collection.insert_many(batch)

                elapsed = time.time() - insert_start


                total_inserted += len(batch)


                print(
                    f"Batch {batch_number}: "
                    f"{len(batch)} records | "
                    f"{elapsed:.4f} sec"
                )


                batch.clear()

                batch_number += 1


        if batch:

            insert_start = time.time()

            collection.insert_many(batch)

            elapsed = time.time() - insert_start


            total_inserted += len(batch)


            print(
                f"Batch {batch_number}: "
                f"{len(batch)} records | "
                f"{elapsed:.4f} sec"
            )


    total_time = time.time() - start_time


    print("----------------------")
    print("Total inserted:", total_inserted)
    print("Total time:", round(total_time, 4), "sec")


    client.close()



if __name__ == "__main__":

    file = "data/orders.csv"

    load_to_mongodb(file)