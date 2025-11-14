-- 1️⃣ Customer + Orders
SELECT c.customer_id, c.name, o.order_id, o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- 2️⃣ Orders + Order Items + Products
SELECT o.order_id, p.product_name, oi.quantity, p.price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- 3️⃣ Products + Reviews
SELECT p.product_id, p.product_name, r.rating, r.review_text
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id;
