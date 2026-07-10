
import os
import sqlite3
import pandas as pd


# Configuration


DATABASE_DIR = "database"
DATABASE_PATH = os.path.join(DATABASE_DIR, "ecommerce.db")
CLEAN_DATA_PATH = "data/cleaned"

TABLES = [
    "customers",
    "products",
    "orders",
    "order_items"
]



# Utility Functions


def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def create_database_folder():
    os.makedirs(DATABASE_DIR, exist_ok=True)


def recreate_database():
    """
    Deletes the old database if it exists.
    """
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("Existing database removed.")


def connect_database():
    """
    Creates SQLite connection and enables foreign keys.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    print_header("Connected to SQLite Database")

    return conn, cursor



# Create Tables


def create_tables(cursor):

    cursor.executescript("""

    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers(

        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        email TEXT,
        registration_date DATE,
        customer_type TEXT

    );

    CREATE TABLE products(

        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        price REAL

    );

    CREATE TABLE orders(

        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        status TEXT,

        FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)

    );

    CREATE TABLE order_items(

        item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        discount_percent REAL,

        FOREIGN KEY(order_id)
        REFERENCES orders(order_id),

        FOREIGN KEY(product_id)
        REFERENCES products(product_id)

    );

    """)

    print("Tables Created Successfully!")



# Load Clean CSV Files


def load_clean_data():

    print_header("Loading Cleaned CSV Files")

    customers = pd.read_csv(
        os.path.join(CLEAN_DATA_PATH, "customers_clean.csv")
    )

    products = pd.read_csv(
        os.path.join(CLEAN_DATA_PATH, "products_clean.csv")
    )

    orders = pd.read_csv(
        os.path.join(CLEAN_DATA_PATH, "orders_clean.csv")
    )

    order_items = pd.read_csv(
        os.path.join(CLEAN_DATA_PATH, "order_items_clean.csv")
    )

    print("All cleaned datasets loaded successfully.\n")

    return customers, products, orders, order_items


# Insert Data into Database


def load_data_to_database(
    conn,
    customers,
    products,
    orders,
    order_items
):

    print_header("Loading Data into Database")

    customers.to_sql(
        "customers",
        conn,
        if_exists="append",
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

    products.to_sql(
        "products",
        conn,
        if_exists="append",
        index=False
    )

    orders = orders[
        [
            "order_id",
            "customer_id",
            "order_date",
            "status"
        ]
    ]

    orders.to_sql(
        "orders",
        conn,
        if_exists="append",
        index=False
    )

    order_items.to_sql(
        "order_items",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    print("Data Loaded Successfully!")

# Verify Database


def verify_database(cursor):

    print_header("ROW COUNTS")

    for table in TABLES:

        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table:<15} : {count}")

    print("=" * 60)



# Main Function


def main():

    conn = None

    try:

        create_database_folder()

        recreate_database()

        conn, cursor = connect_database()

        create_tables(cursor)

        customers, products, orders, order_items = load_clean_data()

        load_data_to_database(
            conn,
            customers,
            products,
            orders,
            order_items
        )

        verify_database(cursor)

        print("\nDatabase Created Successfully!")

    except FileNotFoundError as e:

        print("\nRequired file not found.")
        print(e)

    except sqlite3.Error as e:

        print("\nSQLite Error:")
        print(e)

    except Exception as e:

        print("\nUnexpected Error:")
        print(e)

    finally:

        if conn:

            conn.close()

            print("\nSQLite Connection Closed.")



# Entry Point


if __name__ == "__main__":

    main()