

import os
import sys
import sqlite3
import argparse
from datetime import datetime, timedelta
from tabulate import tabulate
# Configuration

DATABASE_PATH = "database/ecommerce.db"
OUTPUT_DIR = "output"
REPORT_FILE = os.path.join(OUTPUT_DIR, "cli_report_output.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Utility Functions

REPORT_LINES = []

def print_header(title):
    h_top = "\n" + "=" * 70
    h_mid = title.center(70)
    h_bot = "=" * 70
    print(h_top)
    print(h_mid)
    print(h_bot)
    REPORT_LINES.append(h_top + "\n" + h_mid + "\n" + h_bot)


def validate_date(date_text):
    """
    Validate YYYY-MM-DD date format.
    """
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def connect_database():
    """
    Connect to SQLite database.
    """
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found: {DATABASE_PATH}")
        print("Run load_database.py first.")
        sys.exit(1)

    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def execute_query(conn, query, params=None):
    """
    Execute SQL query and return rows + headers.
    """
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    rows = cursor.fetchall()

    headers = [
        description[0]
        for description in cursor.description
    ]

    return headers, rows


def display_table(title, headers, rows):
    """
    Display results using tabulate.
    """
    print_header(title)

    if rows:
        table_str = tabulate(
            rows,
            headers=headers,
            tablefmt="grid"
        )
        print(table_str)
        REPORT_LINES.append(table_str)
    else:
        msg = "No records found."
        print(msg)
        REPORT_LINES.append(msg)


def save_report(report_text):
    """
    Save report into output folder.
    """
    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report_text)


# Date Utilities

def get_previous_period(start_date, end_date):
    """
    Calculate previous comparison period.
    """

    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    days = (end - start).days + 1

    previous_end = start - timedelta(days=1)

    previous_start = previous_end - timedelta(days=days - 1)

    return (
        previous_start.strftime("%Y-%m-%d"),
        previous_end.strftime("%Y-%m-%d")
    )


def percentage_change(current, previous):
    """
    Calculate percentage change.
    """

    if previous == 0:

        if current == 0:
            return "0%"

        return "+100%"

    percent = ((current - previous) / previous) * 100

    if percent >= 0:
        return f"+{percent:.2f}%"

    return f"{percent:.2f}%"

# Summary Metrics

def get_summary_metrics(
    conn,
    start_date,
    end_date
):
    """
    Returns
    Orders
    Revenue
    Customers
    """

    query = """

    SELECT

        COUNT(DISTINCT o.order_id),

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1-oi.discount_percent/100.0)

            ),2

        ),

        COUNT(DISTINCT o.customer_id)

    FROM orders o

    JOIN order_items oi

    ON o.order_id = oi.order_id

    WHERE date(o.order_date)

    BETWEEN ? AND ?;

    """

    _, rows = execute_query(
        conn,
        query,
        (start_date, end_date)
    )

    if rows:

        orders, revenue, customers = rows[0]

        return {

            "orders": orders or 0,

            "revenue": revenue or 0,

            "customers": customers or 0

        }

    return {

        "orders": 0,

        "revenue": 0,

        "customers": 0

    }

# Revenue Report

def revenue_report(conn, start_date, end_date):

    query = """

    SELECT

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1-oi.discount_percent/100.0)

            ),2

        ) AS Total_Revenue

    FROM orders o

    JOIN order_items oi

    ON o.order_id = oi.order_id

    WHERE date(o.order_date)

    BETWEEN ? AND ?;

    """

    headers, rows = execute_query(
        conn,
        query,
        (start_date, end_date)
    )

    display_table(
        "TOTAL REVENUE REPORT",
        headers,
        rows
    )


# Top Customers

def top_customers(conn, start_date, end_date):

    query = """

    SELECT

        c.customer_id,

        c.customer_name,

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1-oi.discount_percent/100.0)

            ),2

        ) AS Revenue

    FROM customers c

    JOIN orders o

    ON c.customer_id=o.customer_id

    JOIN order_items oi

    ON o.order_id=oi.order_id

    WHERE date(o.order_date)

    BETWEEN ? AND ?

    GROUP BY

        c.customer_id,

        c.customer_name

    ORDER BY Revenue DESC

    LIMIT 10;

    """

    headers, rows = execute_query(
        conn,
        query,
        (start_date, end_date)
    )

    display_table(
        "TOP 10 CUSTOMERS",
        headers,
        rows
    )


# Top Products

def top_products(conn, start_date, end_date):

    query = """

    SELECT

        p.product_name,

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1-oi.discount_percent/100.0)

            ),2

        ) AS Revenue,

        SUM(oi.quantity) AS Quantity

    FROM products p

    JOIN order_items oi

    ON p.product_id=oi.product_id

    JOIN orders o

    ON oi.order_id=o.order_id

    WHERE date(o.order_date)

    BETWEEN ? AND ?

    GROUP BY

        p.product_name

    ORDER BY Revenue DESC

    LIMIT 10;

    """

    headers, rows = execute_query(
        conn,
        query,
        (start_date, end_date)
    )

    display_table(
        "TOP PRODUCTS",
        headers,
        rows
    )


# Monthly Revenue

def monthly_revenue(conn, start_date, end_date):

    query = """

    SELECT

        strftime('%Y-%m',o.order_date)

        AS Month,

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1-oi.discount_percent/100.0)

            ),2

        ) AS Revenue

    FROM orders o

    JOIN order_items oi

    ON o.order_id=oi.order_id

    WHERE date(o.order_date)

    BETWEEN ? AND ?

    GROUP BY Month

    ORDER BY Month;

    """

    headers, rows = execute_query(
        conn,
        query,
        (start_date, end_date)
    )

    display_table(
        "MONTHLY REVENUE",
        headers,
        rows
    )


# Customer Cohort

def retention_report(conn):

    query = """

    WITH first_purchase AS (

        SELECT

            customer_id,

            MIN(order_date)

            AS first_purchase

        FROM orders

        GROUP BY customer_id

    )

    SELECT

        strftime('%Y-%m',first_purchase)

        AS Cohort,

        COUNT(customer_id)

        AS Customers

    FROM first_purchase

    GROUP BY Cohort

    ORDER BY Cohort;

    """

    headers, rows = execute_query(
        conn,
        query
    )

    display_table(
        "CUSTOMER COHORT REPORT",
        headers,
        rows
    )


# Customer Segmentation

def customer_segmentation(conn):

    query = """

    SELECT

        customer_id,

        COUNT(order_id)

        AS Orders,

        CASE

            WHEN COUNT(order_id)=1

            THEN 'One-Time'

            WHEN COUNT(order_id)

            BETWEEN 2 AND 5

            THEN 'Occasional'

            ELSE 'Loyal'

        END

        AS Segment

    FROM orders

    GROUP BY customer_id

    ORDER BY Orders DESC
    Limit 20;

    """

    headers, rows = execute_query(
        conn,
        query
    )

    display_table(
        "CUSTOMER SEGMENTATION",
        headers,
        rows
    )

# Trend Analysis

def trend_analysis(
    conn,
    report_type,
    start_date,
    end_date
):

    if report_type == "daily":

        period = "date(o.order_date)"

    elif report_type == "weekly":

        period = "strftime('%Y-W%W',o.order_date)"

    else:

        period = "strftime('%Y-%m',o.order_date)"


    query = f"""

    SELECT

        {period} AS Period,

        COUNT(DISTINCT o.order_id) AS Orders,

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1-oi.discount_percent/100.0)

            ),2

        ) AS Revenue,

        COUNT(DISTINCT o.customer_id)

        AS Customers

    FROM orders o

    JOIN order_items oi

    ON o.order_id=oi.order_id

    WHERE date(o.order_date)

    BETWEEN ? AND ?

    GROUP BY Period

    ORDER BY Period;

    """

    headers, rows = execute_query(
        conn,
        query,
        (start_date, end_date)
    )

    display_table(
        f"{report_type.upper()} TREND ANALYSIS",
        headers,
        rows
    )


# Dashboard Summary

def dashboard_summary(
    conn,
    start_date,
    end_date
):

    previous_start, previous_end = get_previous_period(
        start_date,
        end_date
    )

    current = get_summary_metrics(
        conn,
        start_date,
        end_date
    )

    previous = get_summary_metrics(
        conn,
        previous_start,
        previous_end
    )

    headers = [

        "Metric",

        "Current",

        "Previous",

        "% Change"

    ]

    rows = [

        [

            "Orders",

            current["orders"],

            previous["orders"],

            percentage_change(

                current["orders"],

                previous["orders"]

            )

        ],

        [

            "Revenue",

            current["revenue"],

            previous["revenue"],

            percentage_change(

                current["revenue"],

                previous["revenue"]

            )

        ],

        [

            "Customers",

            current["customers"],

            previous["customers"],

            percentage_change(

                current["customers"],

                previous["customers"]

            )

        ]

    ]

    display_table(

        "SUMMARY DASHBOARD",

        headers,

        rows

    )


# Export Full Report

def export_report(

    conn,

    report_type,

    start_date,

    end_date

):

    previous_start, previous_end = get_previous_period(

        start_date,

        end_date

    )

    current = get_summary_metrics(

        conn,

        start_date,

        end_date

    )

    previous = get_summary_metrics(

        conn,

        previous_start,

        previous_end

    )

    report = []

    report.append("=" * 70)

    report.append("E-COMMERCE ANALYTICS REPORT")

    report.append("=" * 70)

    report.append(f"Generated : {datetime.now()}")

    report.append(f"Period    : {start_date} to {end_date}")

    report.append(f"Trend     : {report_type}")

    report.append("")

    # Append all the captured tables and headers
    report.extend(REPORT_LINES)

    report.append("")
    report.append("=" * 70)

    save_report(

        "\n".join(report)

    )

    print("\nReport exported successfully.")

    print(REPORT_FILE)

# Interactive Menu

def interactive_mode():

    print_header("E-Commerce Analytics Reporting Tool")

    while True:

        report_type = input(
            "\nSelect Trend Type (daily / weekly / monthly): "
        ).strip().lower()

        if report_type in [
            "daily",
            "weekly",
            "monthly"
        ]:
            break

        print("Invalid option. Try again.")

    while True:

        start_date = input(
            "Enter Start Date (YYYY-MM-DD): "
        ).strip()

        if validate_date(start_date):
            break

        print("Invalid date format.")

    while True:

        end_date = input(
            "Enter End Date (YYYY-MM-DD): "
        ).strip()

        if validate_date(end_date):
            break

        print("Invalid date format.")

    return report_type, start_date, end_date


# Main

def main():

    parser = argparse.ArgumentParser(
        description="E-Commerce Analytics Reporting CLI"
    )

    parser.add_argument(
        "-t",
        "--type",
        choices=[
            "daily",
            "weekly",
            "monthly"
        ],
        help="Trend Type"
    )

    parser.add_argument(
        "-s",
        "--start",
        help="Start Date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "-e",
        "--end",
        help="End Date (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    if args.type and args.start and args.end:

        if not validate_date(args.start):

            print("Invalid Start Date")

            return

        if not validate_date(args.end):

            print("Invalid End Date")

            return

        report_type = args.type

        start_date = args.start

        end_date = args.end

    else:

        report_type, start_date, end_date = interactive_mode()

    conn = None

    try:

        conn = connect_database()

        # ---------------- Dashboard ----------------

        dashboard_summary(

            conn,

            start_date,

            end_date

        )

        # ---------------- Reports ----------------

        revenue_report(

            conn,

            start_date,

            end_date

        )

        top_customers(

            conn,

            start_date,

            end_date

        )

        top_products(

            conn,

            start_date,

            end_date

        )

        monthly_revenue(

            conn,

            start_date,

            end_date

        )

        retention_report(conn)

        customer_segmentation(conn)

        trend_analysis(

            conn,

            report_type,

            start_date,

            end_date

        )

        export_report(

            conn,

            report_type,

            start_date,

            end_date

        )

        print("\nAll reports generated successfully.")

    except sqlite3.Error as e:

        print("\nDatabase Error")

        print(e)

    except Exception as e:

        print("\nUnexpected Error")

        print(e)

    finally:

        if conn:

            conn.close()

            print("\nSQLite connection closed.")


# Entry Point

if __name__ == "__main__":

    main()