import random
import json
from faker import Faker

fake = Faker()

def inject_typos(text):
    if len(text) < 2: return text
    chars = list(text)
    idx = random.randint(0, len(chars) - 2)
    chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
    return "".join(chars)

def mess_up_whitespace(text):
    return f"  {text.strip()}  "

def mess_up_price(value):
    options = [f"${value}", f"{value} USD", f"${value:,.2f}", f"{value}".replace(".", ",")]
    return random.choice(options)

def mess_up_date(dt):
    options = [
        dt.strftime("%Y-%m-%d"),
        dt.strftime("%m/%d/%Y"),
        dt.strftime("%b %d, %Y"),
        dt.strftime("%d-%m-%y")
    ]
    return random.choice(options)

def generate_ecommerce_record():
    record = {
        "order_id": random.randint(10000, 99999),
        "customer_name": fake.name(),
        "email": fake.email(),
        "product": fake.catch_phrase(),
        "price": round(random.uniform(5.0, 500.0), 2),
        "order_date": fake.date_time_this_year(),
        "status": random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
    }
    
    if random.random() < 0.5: record["customer_name"] = inject_typos(record["customer_name"])
    if random.random() < 0.3: record["email"] = mess_up_whitespace(record["email"])
    if random.random() < 0.4: record["product"] = record["product"].lower()
    if random.random() < 0.8: record["price"] = mess_up_price(record["price"])
    
    # FORCE the date to always become a string
    record["order_date"] = mess_up_date(record["order_date"])
    
    if random.random() < 0.2: record["status"] = record["status"].swapcase()

    return record
