-- ============================================================
-- E-Commerce Analytics System
-- Window Functions SQL
-- ============================================================


-- Query 1 : Rank Customers by Lifetime Revenue


SELECT
    c.customer_id,
    c.customer_name,

    ROUND(
        SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue,

    RANK() OVER(
        ORDER BY
        SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) DESC
    ) AS customer_rank

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY
c.customer_id,
c.customer_name

ORDER BY total_revenue DESC
LIMIT 20;



-- Query 2 : Dense Rank Customers

SELECT

    customer_id,

    customer_name,

    total_revenue,

    DENSE_RANK() OVER(

        ORDER BY total_revenue DESC

    ) AS dense_rank

FROM (

    SELECT

        c.customer_id,

        c.customer_name,

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ) AS total_revenue

    FROM customers c

    JOIN orders o
    ON c.customer_id = o.customer_id

    JOIN order_items oi
    ON o.order_id = oi.order_id

    GROUP BY

        c.customer_id,

        c.customer_name

)

ORDER BY total_revenue DESC

LIMIT 20;


-- Query 3 : Running Revenue By Month


SELECT

month,

monthly_revenue,

SUM(monthly_revenue)
OVER(
ORDER BY month
) AS running_total

FROM(

SELECT

strftime('%Y-%m',o.order_date) AS month,

ROUND(
SUM(
oi.quantity*oi.unit_price*
(1-oi.discount_percent/100.0)
),2
) AS monthly_revenue

FROM orders o

JOIN order_items oi
ON o.order_id=oi.order_id

GROUP BY month

);



-- Query 4 : Moving Average Revenue


SELECT

month,

monthly_revenue,

ROUND(

AVG(monthly_revenue)

OVER(

ORDER BY month

ROWS BETWEEN 2 PRECEDING
AND CURRENT ROW

),2

) AS moving_average

FROM(

SELECT

strftime('%Y-%m',o.order_date) AS month,

SUM(
oi.quantity*oi.unit_price*
(1-oi.discount_percent/100.0)
) AS monthly_revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY month

);



-- Query 5 : Previous Order Date (LAG)


SELECT

customer_id,

order_id,

order_date,

LAG(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

AS previous_order

FROM orders
Limit 20;



-- Query 6 : Next Order Date (LEAD)


SELECT

customer_id,

order_id,

order_date,

LEAD(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

AS next_order

FROM orders
Limit 20;



-- Query 7 : Row Number Per Customer


SELECT

customer_id,

order_id,

order_date,

ROW_NUMBER()

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

AS order_number

FROM orders
Limit 20;



-- Query 8 : Top Product Per Category


SELECT *

FROM(

SELECT

p.category,

p.product_name,

ROUND(

SUM(

oi.quantity*oi.unit_price*
(1-oi.discount_percent/100.0)

),2

) AS revenue,

ROW_NUMBER()

OVER(

PARTITION BY p.category

ORDER BY

SUM(

oi.quantity*oi.unit_price*
(1-oi.discount_percent/100.0)

) DESC

)

AS rn

FROM products p

JOIN order_items oi

ON p.product_id=oi.product_id

GROUP BY

p.category,

p.product_name

)

WHERE rn=1;