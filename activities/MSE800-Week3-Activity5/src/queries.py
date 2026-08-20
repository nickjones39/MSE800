"""Analytical queries for the money-exchange reports.

Both queries summarise the transaction history: the first totals the value each
customer has exchanged, and the second lists the most recent exchange rate for
each currency pair.
"""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row

CUSTOMER_TOTALS_SQL = """
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        COUNT(t.transaction_id) AS transactions,
        COALESCE(SUM(t.amount_quote), 0) AS total_quote_value
    FROM customer AS c
    LEFT JOIN exchange_transaction AS t ON t.customer_id = c.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    ORDER BY c.customer_id
"""

LATEST_RATES_SQL = """
    SELECT DISTINCT ON (base_currency, quote_currency)
        base_currency,
        quote_currency,
        rate,
        effective_date
    FROM exchange_rate
    ORDER BY base_currency, quote_currency, effective_date DESC
"""


class QueryService:
    """Runs the report queries and returns rows as lists of dictionaries."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection

    def _fetch(self, sql: str) -> list[dict[str, Any]]:
        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def customer_totals(self) -> list[dict[str, Any]]:
        """Total value exchanged by each customer."""
        return self._fetch(CUSTOMER_TOTALS_SQL)

    def latest_rates(self) -> list[dict[str, Any]]:
        """The most recent exchange rate for each currency pair."""
        return self._fetch(LATEST_RATES_SQL)
