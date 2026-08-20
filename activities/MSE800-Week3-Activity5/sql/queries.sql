-- MSE800 Week 3, Activity 5 — report queries (money exchange database)

-- Q1. Total value exchanged (in quote currency) by each customer.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(t.transaction_id) AS transactions,
    COALESCE(SUM(t.amount_quote), 0) AS total_quote_value
FROM customer AS c
LEFT JOIN exchange_transaction AS t ON t.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY c.customer_id;

-- Q2. The most recent exchange rate for each currency pair.
SELECT DISTINCT ON (base_currency, quote_currency)
    base_currency,
    quote_currency,
    rate,
    effective_date
FROM exchange_rate
ORDER BY base_currency, quote_currency, effective_date DESC;
