import re
import json


def clean_price(price):

    corrections = []

    if price is None:
        return None, corrections

    try:
        value = re.sub(r"[^\d.]", "", str(price))

        if value == "":
            return None, corrections

        if value != str(price):
            corrections.append("Removed currency symbols from price")

        return float(value), corrections

    except:
        return None, corrections



def clean_email(email):

    if email is None:
        return None

    email = str(email).strip().lower()

    if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return email

    return None



def extract_item_data(product):

    try:

        if product is None:
            return None, None

        text = str(product).strip()

        text = text.strip('"')
        text = text.replace('""""', '"')
        text = text.replace('""', '"')

        start = text.find("[")
        end = text.rfind("]")

        if start == -1 or end == -1:
            return None, None

        text = text[start:end+1]

        items = json.loads(text)

        if isinstance(items, list) and len(items) > 0:

            item = items[0]

            return item.get("name"), item.get("qty")

        return None, None

    except:
        return None, None



def clean_product(product):

    corrections = []

    name, qty = extract_item_data(product)

    if name:
        corrections.append(
            "Extracted product from items_json"
        )

        return name, corrections

    return None, corrections



def validate_quantity(quantity):

    if quantity is None:
        return None

    try:

        quantity = int(quantity)

        if quantity > 0:
            return quantity

        return None

    except:
        return None



def clean_record(record):

    errors = []
    corrections = []


    record["price"], price_corr = clean_price(
        record.get("price")
    )

    corrections.extend(price_corr)



    record["email"] = clean_email(
        record.get("email")
    )

    if record["email"] is None:
        errors.append("Invalid email")



    product, quantity = extract_item_data(
        record.get("product")
    )


    if product:

        record["product"] = product

    else:

        errors.append("Invalid product")



    record["quantity"] = validate_quantity(
        quantity
    )


    if record["quantity"] is None:

        errors.append("Invalid quantity")


    return record, errors, corrections