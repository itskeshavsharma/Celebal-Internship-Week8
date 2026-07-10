-- ============================================================
-- E-COMMERCE ANALYTICS SYSTEM
-- File : aggregations.sql
-- ============================================================


-- Query 1 : Total Revenue


SELECT
ROUND(SUM(quantity * unit_price * (1-discount_percent/100.0)),2) AS total_revenue
FROM order_items;



-- Query 2 : Revenue Per Customer


SELECT

c.customer_id,
c.customer_name,

ROUND(
SUM(
oi.quantity * oi.unit_price * (1-oi.discount_percent/100.0)
),2
) AS revenue

FROM customers c

JOIN orders o
ON c.customer_id=o.customer_id

JOIN order_items oi
ON o.order_id=oi.order_id

GROUP BY
c.customer_id,
c.customer_name

ORDER BY revenue DESC
LIMIT 20;



-- Query 3 : Revenue Per Category


SELECT

p.category,

ROUND(
SUM(
oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)
),2
) AS revenue

FROM products p

JOIN order_items oi
ON p.product_id=oi.product_id

GROUP BY p.category

ORDER BY revenue DESC
LIMIT 20;

-- Query 4 : Monthly Revenue


SELECT

strftime('%Y-%m',order_date) AS month,

ROUND(
SUM(
oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)
),2
) AS revenue

FROM orders o

JOIN order_items oi
ON o.order_id=oi.order_id

GROUP BY month

ORDER BY month;



-- Query 5 : Top 10 Customers


SELECT

c.customer_id,
c.customer_name,

ROUND(
SUM(
oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)
),2
) AS revenue

FROM customers c

JOIN orders o
ON c.customer_id=o.customer_id

JOIN order_items oi
ON o.order_id=oi.order_id

GROUP BY
c.customer_id,
c.customer_name

ORDER BY revenue DESC

LIMIT 10;



-- Query 6 : Top Products By Quantity


SELECT

p.product_name,

SUM(oi.quantity) AS total_quantity

FROM products p

JOIN order_items oi
ON p.product_id=oi.product_id

GROUP BY p.product_name

ORDER BY total_quantity DESC

LIMIT 10;



-- Query 7 : Top Products By Revenue


SELECT

p.product_name,

ROUND(
SUM(
oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)
),2
) AS revenue

FROM products p

JOIN order_items oi
ON p.product_id=oi.product_id

GROUP BY p.product_name

ORDER BY revenue DESC

LIMIT 10;



-- Query 8 : Average Order Value (AOV)


SELECT

ROUND(

AVG(order_total)

,2) AS average_order_value

FROM

(

SELECT

o.order_id,

SUM(
oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)
) AS order_total

FROM orders o

JOIN order_items oi
ON o.order_id=oi.order_id

GROUP BY o.order_id

);