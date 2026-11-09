
-- Smart Agriculture Intelligence System
-- Database: data/instamart_demo.db

-- 1. Total farm activities and activity value by farmer
SELECT
    customer_id AS farmer_id,
    COUNT(*) AS total_activities,
    ROUND(SUM(order_value), 2) AS total_activity_value
FROM orders
GROUP BY customer_id
ORDER BY total_activity_value DESC;


-- 2. Farmer complaints by category
SELECT
    category,
    COUNT(*) AS total_complaints
FROM tickets
GROUP BY category
ORDER BY total_complaints DESC;


-- 3. Monthly farm activity value
SELECT
    substr(order_date, 1, 7) AS activity_month,
    ROUND(SUM(order_value), 2) AS total_activity_value
FROM orders
GROUP BY activity_month
ORDER BY activity_month;


-- 4. Farmer activity frequency segmentation
SELECT
    customer_id AS farmer_id,
    COUNT(*) AS activity_count,
    CASE
        WHEN COUNT(*) >= 8 THEN 'Highly Active Farmer'
        WHEN COUNT(*) >= 4 THEN 'Moderately Active Farmer'
        ELSE 'Less Active Farmer'
    END AS farmer_segment
FROM orders
GROUP BY customer_id
ORDER BY activity_count DESC;


-- 5. Crop-wise farm activity analysis
SELECT
    crop_type,
    COUNT(*) AS activity_count,
    ROUND(SUM(order_value), 2) AS total_activity_value
FROM orders
GROUP BY crop_type
ORDER BY total_activity_value DESC;

