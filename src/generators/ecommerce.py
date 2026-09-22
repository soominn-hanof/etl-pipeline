import random
from faker import Faker

# Initialize Faker
fake = Faker()

# --- DIRT INJECTION FUNCTIONS ---

def inject_typos(text):
    """Swaps two adjacent letters to simulate a typing error."""
    if len(text) < 2:
        return text
    chars = list(text)
    # Pick a random index (not the last character)
    idx = random.randint(0, len(chars) - 2)
    # Swap the characters
    chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
    return "".join(chars)

def mess_up_whitespace(text):
    """Adds extra spaces to the beginning and end of a string."""
    return f"  {text.strip()}  "

def mess_up_price(value):
    """Converts a clean float to a messy string with currency symbols or commas."""
    options = [
        f"${value}",               # e.g., "$45.5"
        f"{value} USD",            # e.g., "45.5 USD"
        f"${value:,.2f}",          # e.g., "$45.50"
        f"{value}".replace(".", ",") # e.g., "45,5" (European style)
    ]
    return random.choice(options)

def mess_up_date(dt):
    """Converts a datetime object to various string formats."""
    options = [
        dt.strftime("%Y-%m-%d"),      # "2024-03-15" (Clean)
        dt.strftime("%m/%d/%Y"),      # "03/15/2024"
        dt.strftime("%b %d, %Y"),     # "Mar 15, 2024"
        dt.strftime("%d-%m-%y")       # "15-03-24"
    ]
    return random.choice(options)

# --- MAIN GENERATOR FUNCTION ---

def generate_ecommerce_record():
    """Generates a single messy e-commerce JSON record."""
    
    # 1. Generate clean base data
    record = {
        "order_id": random.randint(10000, 99999),
        "customer_name": fake.name(),
        "email": fake.email(),
        "product": fake.catch_phrase(),
        "price": round(random.uniform(5.0, 500.0), 2),
        "order_date": fake.date_time_this_year(),
        "status": random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
    }
    
    # 2. Roll the dice to apply dirt to specific fields
    if random.random() < 0.5:  # 50% chance of typo in name
        record["customer_name"] = inject_typos(record["customer_name"])
        
    if random.random() < 0.3:  # 30% chance of weird whitespace in email
        record["email"] = mess_up_whitespace(record["email"])
        
    if random.random() < 0.4:  # 40% chance of lowercasing the product
        record["product"] = record["product"].lower()
        
    if random.random() < 0.8:  # 80% chance of messing up the price format
        record["price"] = mess_up_price(record["price"])
        
    if random.random() < 0.9:  # 90% chance of messing up the date format
        record["order_date"] = mess_up_date(record["order_date"])
        
    if random.random() < 0.2:  # 20% chance of random casing in status
        record["status"] = record["status"].swapcase()

    return record

# --- TEST BLOCK ---
# This code only runs if you execute this file directly.
# It allows us to test the generator before building the API.
if __name__ == "__main__":
    print("Generating 3 messy E-Commerce records:\n")
    for i in range(3):
        import json
        print(json.dumps(generate_ecommerce_record(), indent=2))
        print("-" * 40)
