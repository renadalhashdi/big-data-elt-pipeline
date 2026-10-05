import os
import sys


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


from file_router import route_file
from batch_loader import load_to_mongodb
from spark_loader import load_with_spark
from elt_pipeline import run_pipeline



def main(file_path):

    print("======================")
    print("DATA PIPELINE START")
    print("======================")


    engine = route_file(file_path)


    print("Selected Engine:", engine)


    if engine == "PYTHON_BATCH":

        print("Running Python Batch Loader...")

        load_to_mongodb(file_path)


    elif engine == "PYSPARK":

        print("Running PySpark Loader...")

        load_with_spark(file_path)


    else:

        print("Unknown Engine")

        return



    print("======================")
    print("Running ELT Pipeline")
    print("======================")


    run_pipeline()

if __name__ == "__main__":


    file_path = (
        "data/orders_clean.csv"
    )


    main(file_path)
    main(file_path)