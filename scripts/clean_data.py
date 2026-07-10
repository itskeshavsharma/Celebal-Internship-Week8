import os
import pandas as pd

RAW_PATH = "data/raw"
CLEAN_PATH = "data/cleaned"

os.makedirs(CLEAN_PATH, exist_ok=True)

def clean_orders(orders):

    orders = orders.copy()

    orders["customer_id"] = (
        orders["customer_id"]
        .astype(str)
        .str.strip()
    )

    orders = orders[
        orders["customer_id"] != ""
    ]

    orders["customer_id"] = pd.to_numeric(
        orders["customer_id"],
        errors="coerce"
    )

    orders = orders[
        orders["customer_id"].notna()
    ]

    orders["customer_id"] = (
        orders["customer_id"]
        .astype(int)
    )

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    orders = orders[
        orders["order_date"].notna()
    ]

    today = pd.Timestamp.now()

    orders = orders[
        orders["order_date"] <= today
    ]

    return orders

def check_referential_integrity(
    orders,
    order_items
):

    invalid_items = order_items[
        ~order_items["order_id"].isin(
            orders["order_id"]
        )
    ]

    return invalid_items[
        "item_id"
    ].tolist()


print("=" * 60)
print("Loading Raw Datasets...")
print("=" * 60)

customers = pd.read_csv(
    os.path.join(
        RAW_PATH,
        "customers.csv"
    )
)

products = pd.read_csv(
    os.path.join(
        RAW_PATH,
        "products.csv"
    )
)

orders = pd.read_csv(
    os.path.join(
        RAW_PATH,
        "orders.csv"
    )
)

order_items = pd.read_csv(
    os.path.join(
        RAW_PATH,
        "order_items.csv"
    )
)

print("Datasets Loaded Successfully!\n")

# Customers

print("Cleaning Customers...")

before = len(customers)

customers.drop_duplicates(
    subset="customer_id",
    inplace=True
)

duplicates_removed = before - len(customers)

customers["customer_name"] = (
    customers["customer_name"]
    .fillna("Unknown Customer")
    .str.strip()
)

customers["email"] = (
    customers["email"]
    .fillna("unknown@example.com")
    .str.strip()
)

email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

customers.loc[
    ~customers["email"].str.match(
        email_pattern,
        na=False
    ),
    "email"
] = "unknown@example.com"

# Products

print("Cleaning Products...")

before = len(products)

products.drop_duplicates(
    subset="product_id",
    inplace=True
)

product_duplicates = before - len(products)

products["product_name"] = (
    products["product_name"]
    .astype(str)
    .str.strip()
    .str.title()
)

products["category"] = (
    products["category"]
    .astype(str)
    .str.strip()
    .str.title()
)

products["price"] = pd.to_numeric(
    products["price"],
    errors="coerce"
)

negative_price = len(
    products[
        (products["price"].isna())
        |
        (products["price"] < 0)
    ]
)

products = products[
    products["price"].notna()
]

products = products[
    products["price"] >= 0
]

# Orders

print("Cleaning Orders...")

before = len(orders)

orders.drop_duplicates(
    subset="order_id",
    inplace=True
)

order_duplicates = before - len(orders)

before_clean = len(orders)
orders = clean_orders(orders)
future_orders = before_clean - len(orders)

# Order Items

print("Cleaning Order Items...")

before = len(order_items)

order_items.drop_duplicates(
    subset="item_id",
    inplace=True
)

item_duplicates = before - len(order_items)

order_items["quantity"] = pd.to_numeric(
    order_items["quantity"],
    errors="coerce"
)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"],
    errors="coerce"
)

order_items["discount_percent"] = pd.to_numeric(
    order_items["discount_percent"],
    errors="coerce"
)

negative_qty = len(
    order_items[
        (order_items["quantity"].isna())
        |
        (order_items["quantity"] <= 0)
    ]
)

order_items = order_items[
    order_items["quantity"].notna()
]

order_items = order_items[
    order_items["quantity"] > 0
]

order_items["unit_price"] = (
    order_items["unit_price"]
    .fillna(
        order_items["unit_price"].median()
    )
)

invalid_price = len(
    order_items[
        order_items["unit_price"] <= 0
    ]
)

order_items = order_items[
    order_items["unit_price"] > 0
]

order_items["discount_percent"] = (
    order_items["discount_percent"]
    .fillna(0)
)

invalid_discount = len(
    order_items[
        (order_items["discount_percent"] < 0)
        |
        (order_items["discount_percent"] > 100)
    ]
)

order_items = order_items[
    (order_items["discount_percent"] >= 0)
    &
    (order_items["discount_percent"] <= 100)
]

# Referential Integrity

print("Validating Relationships...")

invalid_orders = len(
    check_referential_integrity(
        orders,
        order_items
    )
)

order_items = order_items[
    order_items["order_id"].isin(
        orders["order_id"]
    )
]

invalid_products = len(
    order_items[
        ~order_items["product_id"].isin(
            products["product_id"]
        )
    ]
)

order_items = order_items[
    order_items["product_id"].isin(
        products["product_id"]
    )
]

customers.reset_index(
    drop=True,
    inplace=True
)

products.reset_index(
    drop=True,
    inplace=True
)

orders.reset_index(
    drop=True,
    inplace=True
)

order_items.reset_index(
    drop=True,
    inplace=True
)

customers.to_csv(
    os.path.join(
        CLEAN_PATH,
        "customers_clean.csv"
    ),
    index=False
)

products = products[
    [
        "product_id",
        "product_name",
        "category",
        "price"
    ]
]

products.to_csv(
    os.path.join(
        CLEAN_PATH,
        "products_clean.csv"
    ),
    index=False
)

orders.to_csv(
    os.path.join(
        CLEAN_PATH,
        "orders_clean.csv"
    ),
    index=False
)

order_items.to_csv(
    os.path.join(
        CLEAN_PATH,
        "order_items_clean.csv"
    ),
    index=False
)

print("\n" + "=" * 60)
print("DATA CLEANING SUMMARY")
print("=" * 60)

print(f"Customer Duplicates Removed : {duplicates_removed}")
print(f"Product Duplicates Removed  : {product_duplicates}")
print(f"Order Duplicates Removed    : {order_duplicates}")
print(f"Item Duplicates Removed     : {item_duplicates}")
print(f"Future Orders Removed       : {future_orders}")
print(f"Negative Prices Removed     : {negative_price}")
print(f"Negative Quantity Removed   : {negative_qty}")
print(f"Invalid Discounts Removed   : {invalid_discount}")
print(f"Invalid Unit Prices Removed : {invalid_price}")
print(f"Invalid Order IDs Removed   : {invalid_orders}")
print(f"Invalid Product IDs Removed : {invalid_products}")

print("\nFinal Dataset Sizes\n")

print(f"Customers   : {len(customers)}")
print(f"Products    : {len(products)}")
print(f"Orders      : {len(orders)}")
print(f"Order Items : {len(order_items)}")

print("\nCleaned CSV Files Saved Successfully!")
print("=" * 60)