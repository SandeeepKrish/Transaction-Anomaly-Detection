-- Example SQL analytics
-- Works with PostgreSQL after loading transactions.csv into a transactions table.

SELECT merchant,
       COUNT(*) AS transactions,
       ROUND(AVG(amount), 2) AS avg_amount,
       ROUND(MAX(amount), 2) AS max_amount
FROM transactions
GROUP BY merchant
ORDER BY max_amount DESC;

SELECT category,
       COUNT(*) AS transactions,
       ROUND(SUM(amount), 2) AS total_value
FROM transactions
GROUP BY category
ORDER BY total_value DESC;
