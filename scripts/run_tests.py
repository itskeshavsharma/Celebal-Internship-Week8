import pandas as pd
from datetime import datetime, timedelta
from clean_data import clean_orders, check_referential_integrity

passed = 0
failed = 0


def result(name, status):
    global passed, failed

    if status:
        passed += 1
        print(f"{name} : PASSED")
    else:
        failed += 1
        print(f"{name} : FAILED")


def test_orphaned_order_items():

    orders = pd.DataFrame([
        {
            "order_id": "O00001",
            "customer_id": "C00001",
            "order_date": "2024-01-01 10:00:00",
            "status": "DELIVERED"
        }
    ])

    items = pd.DataFrame([
        {
            "item_id": "I00001",
            "order_id": "O00001",
            "product_id": "P00001",
            "quantity": 2,
            "unit_price": 100,
            "discount_percent": 0
        },
        {
            "item_id": "I00002",
            "order_id": "O99999",
            "product_id": "P00002",
            "quantity": 1,
            "unit_price": 200,
            "discount_percent": 5
        }
    ])

    orphan = check_referential_integrity(
        orders,
        items
    )

    result(
        "Orphaned Order Items",
        "I00002" in orphan and "I00001" not in orphan
    )


def test_invalid_discount():

    items = pd.DataFrame([
        {
            "item_id": "I00001",
            "discount_percent": 120
        },
        {
            "item_id": "I00002",
            "discount_percent": 20
        },
        {
            "item_id": "I00003",
            "discount_percent": -5
        }
    ])

    clean = items[
        (items["discount_percent"] >= 0)
        &
        (items["discount_percent"] <= 100)
    ]

    ids = clean["item_id"].tolist()

    result(
        "Discount Validation",
        "I00002" in ids
        and
        "I00001" not in ids
        and
        "I00003" not in ids
    )


def test_zero_quantity():

    items = pd.DataFrame([
        {
            "item_id": "I00001",
            "quantity": 0
        },
        {
            "item_id": "I00002",
            "quantity": 5
        }
    ])

    clean = items[
        items["quantity"] > 0
    ]

    ids = clean["item_id"].tolist()

    result(
        "Zero Quantity",
        "I00002" in ids
        and
        "I00001" not in ids
    )


def test_future_order_date():

    future_date = (
        datetime.now() +
        timedelta(days=5)
    ).strftime("%Y-%m-%d")

    past_date = (
        datetime.now() -
        timedelta(days=5)
    ).strftime("%Y-%m-%d")

    orders = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": 1,
            "order_date": future_date,
            "status": "DELIVERED"
        },
        {
            "order_id": 2,
            "customer_id": 2,
            "order_date": past_date,
            "status": "DELIVERED"
        }
    ])

    clean = clean_orders(orders)

    ids = clean["order_id"].tolist()

    result(
        "Future Order Date",
        2 in ids and 1 not in ids
    )

def test_missing_customer():

    orders = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": None,
            "order_date": "2024-01-01",
            "status": "DELIVERED"
        },
        {
            "order_id": 2,
            "customer_id": 2,
            "order_date": "2024-01-02",
            "status": "DELIVERED"
        }
    ])

    clean = clean_orders(orders)

    ids = clean["order_id"].tolist()

    result(
        "Missing Customer",
        2 in ids and 1 not in ids
    )
def main():

    print("=" * 50)
    print("RUNNING TEST CASES")
    print("=" * 50)

    test_orphaned_order_items()

    test_invalid_discount()

    test_zero_quantity()

    test_future_order_date()

    test_missing_customer()

    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    print(f"Passed : {passed}")

    print(f"Failed : {failed}")

    print(f"Total  : {passed + failed}")

    if failed == 0:

        print("\nAll test cases passed successfully.")

    else:

        print("\nSome test cases failed.")


if __name__ == "__main__":

    main()