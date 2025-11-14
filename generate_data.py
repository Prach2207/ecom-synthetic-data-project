import csv
import os
import random
from datetime import datetime, timedelta


def ensure_data_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def random_date(start: datetime, end: datetime) -> datetime:
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def generate_customers(count: int):
    first_names = [
        "Ava",
        "Noah",
        "Liam",
        "Emma",
        "Olivia",
        "Sophia",
        "James",
        "Lucas",
        "Mason",
        "Ethan",
        "Harper",
        "Isabella",
        "Mia",
        "Amelia",
        "Evelyn",
        "Ella",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Gonzalez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
    ]
    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Seattle",
        "Denver",
        "Boston",
        "Miami",
        "Atlanta",
        "Austin",
        "Portland",
    ]

    customers = []
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2024, 12, 31)

    for idx in range(1, count + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        full_name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}{idx}@example.com"
        joined = random_date(start_date, end_date)
        customers.append(
            {
                "id": idx,
                "name": full_name,
                "email": email,
                "city": random.choice(cities),
                "joined_date": joined.strftime("%Y-%m-%d"),
                "joined_dt": joined,
            }
        )
    return customers


def generate_products(count: int):
    categories = {
        "Electronics": [
            "Smartphone",
            "Laptop",
            "Wireless Earbuds",
            "Smartwatch",
            "Bluetooth Speaker",
        ],
        "Home": ["Vacuum Cleaner", "Air Purifier", "Coffee Maker", "Blender", "Toaster"],
        "Outdoors": ["Camping Tent", "Travel Backpack", "Hiking Boots", "Cooler"],
        "Beauty": ["Skin Care Set", "Hair Dryer", "Electric Toothbrush"],
        "Fitness": ["Yoga Mat", "Adjustable Dumbbells", "Fitness Tracker", "Foam Roller"],
    }

    products = []
    product_id = 1
    while len(products) < count:
        category = random.choice(list(categories.keys()))
        name = random.choice(categories[category])
        price = round(random.uniform(10, 500), 2)
        products.append(
            {
                "id": product_id,
                "name": name,
                "category": category,
                "price": price,
            }
        )
        product_id += 1
    return products


def generate_orders(count: int, customers):
    orders = []
    end_date = datetime(2025, 3, 31)
    for idx in range(1, count + 1):
        customer = random.choice(customers)
        customer_joined = customer["joined_dt"]
        order_date = random_date(customer_joined, end_date)
        orders.append(
            {
                "id": idx,
                "customer_id": customer["id"],
                "order_date": order_date.strftime("%Y-%m-%d"),
                "order_dt": order_date,
            }
        )
    return orders


def generate_order_items(target_count: int, orders, products):
    order_totals = {order["id"]: 0.0 for order in orders}
    order_items = []
    order_item_id = 1

    def add_item(order, product, quantity):
        nonlocal order_item_id
        subtotal = product["price"] * quantity
        order_items.append(
            {
                "id": order_item_id,
                "order_id": order["id"],
                "product_id": product["id"],
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )
        order_totals[order["id"]] += subtotal
        order_item_id += 1

    # Ensure each order has at least one item
    for order in orders:
        product = random.choice(products)
        quantity = random.randint(1, 4)
        add_item(order, product, quantity)

    # Add remaining items
    while len(order_items) < target_count:
        order = random.choice(orders)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        add_item(order, product, quantity)

    return order_items, order_totals


def generate_reviews(count: int, customers, products, orders):
    review_phrases = [
        "Absolutely love it, highly recommend!",
        "Solid quality for the price.",
        "Shipping was fast and the product works great.",
        "Not quite what I expected but still decent.",
        "Fantastic experience from checkout to delivery.",
        "Quality could be better, but customer service helped.",
        "Exceeded my expectations!",
        "Packaging was damaged but product survived.",
        "Would buy again without hesitation.",
        "Great value, already telling my friends.",
    ]

    reviews = []
    for idx in range(1, count + 1):
        order = random.choice(orders)
        customer_id = order["customer_id"]
        product = random.choice(products)
        base_date = order["order_dt"]
        review_date = random_date(base_date, base_date + timedelta(days=60))
        rating = random.choices([5, 4, 3, 2, 1], weights=[0.45, 0.3, 0.15, 0.07, 0.03])[0]
        reviews.append(
            {
                "id": idx,
                "customer_id": customer_id,
                "product_id": product["id"],
                "order_id": order["id"],
                "rating": rating,
                "review_text": random.choice(review_phrases),
                "review_date": review_date.strftime("%Y-%m-%d"),
            }
        )
    return reviews


def generate_payments(orders, order_totals):
    payment_methods = ["credit_card", "paypal", "bank_transfer", "gift_card"]
    statuses = ["completed", "pending", "failed", "refunded"]

    payments = []
    for order in orders:
        amount = round(order_totals[order["id"]], 2)
        # In case rounding created zero for some reason, ensure a minimum
        if amount == 0:
            amount = round(random.uniform(20, 200), 2)
        payments.append(
            {
                "id": order["id"],
                "order_id": order["id"],
                "amount": amount,
                "payment_method": random.choice(payment_methods),
                "status": random.choices(statuses, weights=[0.8, 0.1, 0.05, 0.05])[0],
            }
        )
    return payments


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            filtered = {field: row[field] for field in fieldnames}
            writer.writerow(filtered)


def main():
    random.seed(42)
    data_dir = "data"
    ensure_data_dir(data_dir)

    customers = generate_customers(100)
    products = generate_products(50)
    orders = generate_orders(200, customers)
    order_items, order_totals = generate_order_items(400, orders, products)
    payments = generate_payments(orders, order_totals)
    reviews = generate_reviews(300, customers, products, orders)

    write_csv(
        os.path.join(data_dir, "customers.csv"),
        ["id", "name", "email", "city", "joined_date"],
        customers,
    )
    write_csv(
        os.path.join(data_dir, "products.csv"),
        ["id", "name", "category", "price"],
        products,
    )
    write_csv(
        os.path.join(data_dir, "orders.csv"),
        ["id", "customer_id", "order_date"],
        orders,
    )
    write_csv(
        os.path.join(data_dir, "order_items.csv"),
        ["id", "order_id", "product_id", "quantity"],
        order_items,
    )
    write_csv(
        os.path.join(data_dir, "payments.csv"),
        ["id", "order_id", "amount", "payment_method", "status"],
        payments,
    )
    write_csv(
        os.path.join(data_dir, "reviews.csv"),
        ["id", "customer_id", "product_id", "order_id", "rating", "review_text", "review_date"],
        reviews,
    )
    print("Synthetic CSV files generated in ./data/")


if __name__ == "__main__":
    main()

