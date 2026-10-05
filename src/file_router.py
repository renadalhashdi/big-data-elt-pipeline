import os
import sys

# إضافة مسار المشروع الرئيسي
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from config.settings import FILE_SIZE_THRESHOLD_MB


def get_file_size_mb(file_path):

    size_bytes = os.path.getsize(file_path)

    size_mb = size_bytes / (1024 * 1024)

    return size_mb



def route_file(file_path):

    file_size = get_file_size_mb(file_path)

    print(f"File size: {file_size:.2f} MB")


    if file_size <= FILE_SIZE_THRESHOLD_MB:

        return "PYTHON_BATCH"

    else:

        return "PYSPARK"



if __name__ == "__main__":

    # الملف الكبير الحقيقي
    file = "data/orders_huge_mixed_quality.csv"

    method = route_file(file)

    print("Selected Engine:", method)