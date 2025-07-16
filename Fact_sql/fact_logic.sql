DROP TABLE IF EXISTS fact_sales;

CREATE TABLE fact_sales AS
SELECT
    s.invoice_id,
    s.branch,
    s.city,
    c.customer_id,
	c.customer_type,
	c.gender,
    p.product_id,
	p.product_line,
	p.unit_price,
    s.quantity,
    s.quantity * p.unit_price             AS total,
    s.quantity * p.unit_price * 0.05      AS tax_5_percent,
    s.cogs,
    s.quantity * p.unit_price * 0.05      AS gross_income,
    (s.quantity * p.unit_price * 0.05) / (s.quantity * p.unit_price) * 100 AS gross_margin_percentage,
    s.date,
    s.time,
    s.payment        AS payment_method,
    s.rating

FROM stage_sales s
LEFT JOIN dim_customer c ON s.customer_id = c.customer_id
LEFT JOIN dim_product p ON s.product_id = p.product_id;
