-- E-Commerce Analytics System
-- Database Schema

PRAGMA foreign_keys = ON;

-- Drop Existing Tables

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Customers Table

CREATE TABLE customers (

    customer_id INTEGER PRIMARY KEY,

    customer_name TEXT NOT NULL,

    email TEXT NOT NULL,

    registration_date DATE NOT NULL,

    customer_type TEXT NOT NULL
        CHECK(customer_type IN ('REGULAR','PREMIUM','VIP'))

);

--- Products Table

CREATE TABLE products (

    product_id INTEGER PRIMARY KEY,

    product_name TEXT NOT NULL,

    category TEXT NOT NULL,

    price REAL NOT NULL
        CHECK(price >= 0)

);

--- Orders Table

CREATE TABLE orders (

    order_id INTEGER PRIMARY KEY,

    customer_id INTEGER NOT NULL,

    order_date DATE NOT NULL,

    status TEXT NOT NULL
        CHECK(status IN
        (
            'PLACED',
            'SHIPPED',
            'DELIVERED',
            'CANCELLED',
            'RETURNED'
        )),

    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id)

);

--- Order Items Table

CREATE TABLE order_items (

    item_id INTEGER PRIMARY KEY,

    order_id INTEGER NOT NULL,

    product_id INTEGER NOT NULL,

    quantity INTEGER NOT NULL
        CHECK(quantity > 0),

    unit_price REAL NOT NULL
        CHECK(unit_price >= 0),

    discount_percent REAL DEFAULT 0
        CHECK(discount_percent BETWEEN 0 AND 100),

    FOREIGN KEY(order_id)
    REFERENCES orders(order_id),

    FOREIGN KEY(product_id)
    REFERENCES products(product_id)

);

--- Indexes

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_date
ON orders(order_date);

CREATE INDEX idx_products_category
ON products(category);

CREATE INDEX idx_order_items_order
ON order_items(order_id);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

--- Verify Tables

SELECT name
FROM sqlite_master
WHERE type='table';

--- Verify Indexes

SELECT name
FROM sqlite_master
WHERE type='index';