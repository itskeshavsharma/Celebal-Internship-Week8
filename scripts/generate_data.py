import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 500
NUM_ORDER_ITEMS = 1500

RAW_PATH = "data/raw"

os.makedirs(RAW_PATH, exist_ok=True)

CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

ORDER_STATUS = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

REGIONS = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST"
]

CATEGORIES = {
    "Electronics": {
        "Laptop": [
            "Dell",
            "HP",
            "Lenovo",
            "Asus"
        ],
        "Mobile": [
            "Samsung",
            "Apple",
            "OnePlus",
            "Xiaomi"
        ],
        "Tablet": [
            "Apple",
            "Samsung"
        ],
        "Monitor": [
            "LG",
            "Dell"
        ],
        "Keyboard": [
            "Logitech",
            "HP"
        ],
        "Mouse": [
            "Logitech",
            "Dell"
        ]
    },

    "Books": {
        "Programming": [
            "Python",
            "Java",
            "SQL",
            "C++"
        ],
        "Algorithms": [
            "DSA",
            "Competitive Coding"
        ],
        "Data Science": [
            "ML",
            "AI"
        ]
    },

    "Clothing": {
        "Shirt": [
            "Nike",
            "Puma",
            "Levis"
        ],
        "Jeans": [
            "Levis",
            "Spykar"
        ],
        "Jacket": [
            "Woodland",
            "Puma"
        ],
        "T-Shirt": [
            "Nike",
            "Adidas"
        ]
    },

    "Home": {
        "Chair": [
            "Ikea"
        ],
        "Table": [
            "Ikea"
        ],
        "Lamp": [
            "Philips"
        ],
        "Sofa": [
            "HomeTown"
        ]
    }
}


def generate_customers():

    customers = []

    for cid in range(1, NUM_CUSTOMERS + 1):

        customers.append({

            "customer_id": cid,

            "customer_name": fake.name(),

            "email": fake.email(),

            "registration_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            ),

            "customer_type": random.choice(CUSTOMER_TYPES)

        })

    df = pd.DataFrame(customers)

    duplicate_rows = df.sample(5)

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    for i in random.sample(range(len(df)), 10):
        df.loc[i, "email"] = "invalidemail.com"

    for i in random.sample(range(len(df)), 5):
        df.loc[i, "customer_name"] = None

    return df


def generate_products():

    products = []

    product_id = 1

    while product_id <= NUM_PRODUCTS:

        category = random.choice(
            list(CATEGORIES.keys())
        )

        subcategory = random.choice(
            list(CATEGORIES[category].keys())
        )

        brand = random.choice(
            CATEGORIES[category][subcategory]
        )

        product_name = (
            f"{brand} {subcategory} Model {random.randint(100,999)}"
        )

        products.append({

            "product_id": product_id,

            "product_name": product_name,

            "category": category,

            "subcategory": subcategory,

            "brand": brand,

            "price": random.randint(500,50000)

        })

        product_id += 1

    df = pd.DataFrame(products)

    duplicate_products = df.sample(5)

    df = pd.concat(
        [df, duplicate_products],
        ignore_index=True
    )

    for i in random.sample(range(len(df)),10):

        df.loc[i,"product_name"]="   "+df.loc[i,"product_name"]+" "

    for i in random.sample(range(len(df)),5):

        df.loc[i,"price"]=-100

    return df

def generate_orders():

    orders = []

    start = datetime(2023, 1, 1)

    for order_id in range(1, NUM_ORDERS + 1):

        order_date = start + timedelta(
            days=random.randint(0, 900)
        )

        orders.append({

            "order_id": order_id,

            "customer_id": random.randint(
                1,
                NUM_CUSTOMERS
            ),

            "order_date": order_date.date(),

            "status": random.choices(

                ORDER_STATUS,

                weights=[5,10,70,10,5]

            )[0],

            "region_code": random.choice(REGIONS)

        })

    df = pd.DataFrame(orders)

    for i in random.sample(range(NUM_ORDERS),5):

        df.loc[i,"order_date"] = (
            datetime.now().date()
            + timedelta(days=30)
        )

    for i in random.sample(range(NUM_ORDERS),5):

        df.loc[i,"customer_id"] = None

    return df


def generate_order_items():

    items = []

    for item_id in range(
        1,
        NUM_ORDER_ITEMS + 1
    ):

        product_price = random.randint(
            500,
            50000
        )

        items.append({

            "item_id": item_id,

            "order_id": random.randint(
                1,
                NUM_ORDERS
            ),

            "product_id": random.randint(
                1,
                NUM_PRODUCTS
            ),

            "quantity": random.randint(
                1,
                5
            ),

            "unit_price": round(
                product_price *
                random.uniform(
                    1.10,
                    1.40
                ),
                2
            ),

            "discount_percent": random.choice(
                [
                    0,
                    5,
                    10,
                    15,
                    20,
                    25,
                    30
                ]
            )

        })

    df = pd.DataFrame(items)

    for i in random.sample(
        range(NUM_ORDER_ITEMS),
        10
    ):

        df.loc[i,"order_id"] = 99999

    for i in random.sample(
        range(NUM_ORDER_ITEMS),
        10
    ):

        df.loc[i,"quantity"] = -5

    for i in random.sample(
        range(NUM_ORDER_ITEMS),
        5
    ):

        df.loc[i,"discount_percent"] = 150

    for i in random.sample(
        range(NUM_ORDER_ITEMS),
        5
    ):

        df.loc[i,"unit_price"] = -100

    return df


def save_csv(df, filename):

    path = os.path.join(
        RAW_PATH,
        filename
    )

    df.to_csv(
        path,
        index=False
    )

    print(
        f"[OK] {filename:<20} {len(df)} rows"
    )


def main():

    print("=" * 60)
    print("Generating Realistic E-Commerce Dataset")
    print("=" * 60)

    customers = generate_customers()

    products = generate_products()

    orders = generate_orders()

    order_items = generate_order_items()

    save_csv(
        customers,
        "customers.csv"
    )

    save_csv(
        products,
        "products.csv"
    )

    save_csv(
        orders,
        "orders.csv"
    )

    save_csv(
        order_items,
        "order_items.csv"
    )

    print("\n" + "=" * 60)

    print("Dataset Generation Summary")

    print("=" * 60)

    print(f"Customers      : {len(customers)}")

    print(f"Products       : {len(products)}")

    print(f"Orders         : {len(orders)}")

    print(f"Order Items    : {len(order_items)}")

    print("=" * 60)

    print("Raw CSV files saved successfully!")

    print("=" * 60)


if __name__ == "__main__":

    main()