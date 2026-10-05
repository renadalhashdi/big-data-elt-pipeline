import csv


input_file = "data/orders_huge_mixed_quality.csv"

output_file = "data/orders_clean.csv"


with open(input_file, "r", encoding="utf-8") as f:

    lines = f.readlines()


with open(output_file, "w", encoding="utf-8", newline="") as out:

    writer = csv.writer(out)

    header = [
        "id_order",
        "order_date",
        "status",
        "customer_id",
        "customer_name",
        "phone",
        "email",
        "city",
        "district",
        "delivery_type",
        "delivery_cost",
        "payment_method",
        "payment_status",
        "payment_amount",
        "currency",
        "price",
        "product"
    ]

    writer.writerow(header)


    for line in lines[1:]:

        line = line.strip()


        if line.startswith('"'):

            line = line[1:]


        if line.endswith('"'):

            line = line[:-1]


        parts = line.split(",", 16)


        if len(parts) == 17:

            writer.writerow(parts)


print("CSV cleaned successfully")