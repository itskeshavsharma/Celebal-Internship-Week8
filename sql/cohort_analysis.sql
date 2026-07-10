--- Query 1 : Customer First Purchase (Cohort)
WITH first_purchase AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_purchase_date
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    first_purchase_date,
    strftime('%Y-%m', first_purchase_date) AS cohort_month
FROM first_purchase
ORDER BY first_purchase_date
LIMIT 20;

--- Query 2 : Monthly Cohort Retention
WITH first_purchase AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_purchase
    FROM orders
    GROUP BY customer_id
),
cohort_data AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', fp.first_purchase) AS cohort_month,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
    JOIN first_purchase fp
        ON o.customer_id = fp.customer_id
)
SELECT
    cohort_month,
    order_month,
    COUNT(DISTINCT customer_id) AS retained_customers
FROM cohort_data
GROUP BY
    cohort_month,
    order_month
ORDER BY
    cohort_month,
    order_month
LIMIT 20;

--- Query 3 : Repeat vs One-Time Customers
SELECT
    customer_id,
    COUNT(order_id) AS total_orders,
    CASE
        WHEN COUNT(order_id) = 1 THEN 'One-Time'
        ELSE 'Repeat'
    END AS customer_type
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 20;

--- Query 4 : Customer Spend Tier
WITH revenue AS (
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name
)
SELECT
    customer_id,
    customer_name,
    ROUND(revenue, 2) AS revenue,
    CASE
        WHEN revenue < 5000 THEN 'LOW'
        WHEN revenue BETWEEN 5000 AND 10000 THEN 'MEDIUM'
        ELSE 'HIGH'
    END AS spend_tier
FROM revenue
ORDER BY revenue DESC
LIMIT 20;

--- Query 5 : Purchase Frequency Segmentation
SELECT
    customer_id,
    COUNT(order_id) AS total_orders,
    CASE
        WHEN COUNT(order_id) = 1 THEN 'ONE-TIME'
        WHEN COUNT(order_id) BETWEEN 2 AND 5 THEN 'OCCASIONAL'
        ELSE 'LOYAL'
    END AS customer_segment
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 20;


--- Query 6 : RFM Analysis
WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name
)
SELECT
    customer_id,
    customer_name,
    ROUND(julianday('now') - julianday(last_order), 0) AS recency_days,
    frequency,
    ROUND(monetary, 2) AS monetary
FROM customer_metrics
ORDER BY monetary DESC
LIMIT 20;

--- Query 7 : Top 10 Loyal Customers
SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 10;

--- Query 8 : Churned Customers
WITH last_purchase AS (
    SELECT
        customer_id,
        MAX(order_date) AS last_order
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    last_order,
    ROUND(julianday('now') - julianday(last_order), 0) AS days_since_last_purchase,
    CASE
        WHEN julianday('now') - julianday(last_order) > 180 THEN 'CHURNED'
        ELSE 'ACTIVE'
    END AS customer_status
FROM last_purchase
ORDER BY days_since_last_purchase DESC
LIMIT 20;
