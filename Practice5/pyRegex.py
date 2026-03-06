import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Extract all prices
price_pattern = r"\d[\d\s]*,\d{2}"
prices = re.findall(price_pattern, text)

# find product names
product_name = r"\d+\.\n(.+)"
products = re.findall(product_name, text)

# calculate total
price_numbers = [float(p.replace(" ", "").replace(",", ".").replace("\n", "")) for p in prices]
total_calc = sum(price_numbers)

# extract data and time
datetime_pattern = r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}"
datetime_match = re.search(datetime_pattern, text)
datetime_value = datetime_match.group() if datetime_match else None

# find payment method
payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group() if payment_match else None

# output
result = {
    "products": products,
    "prices": price_numbers,
    "calculated_total": total_calc,
    "datetime": datetime_value,
    "payment_method": payment_method
}
print(json.dumps(result, indent=4, ensure_ascii=False))
