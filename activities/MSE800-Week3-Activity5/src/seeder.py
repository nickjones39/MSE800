"""Sample data and database seeding.

The sample data covers the four entities in the brief (customers, currencies,
exchange rates and transactions):

* 5 currencies,
* 4 customers,
* 10 exchange rates (five pairs, each quoted in both directions), and
* 5 transactions, several made by the same customer — this exercises the
  one-to-many relationship between ``customer`` and ``exchange_transaction``.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import psycopg

from .models import Currency, Customer, ExchangeRate, Transaction
from .repositories import (
    CurrencyRepository,
    CustomerRepository,
    ExchangeRateRepository,
    TransactionRepository,
)

CURRENCIES = [
    Currency("NZD", "New Zealand Dollar", "NZ$"),
    Currency("USD", "United States Dollar", "US$"),
    Currency("EUR", "Euro", "€"),
    Currency("GBP", "British Pound", "£"),
    Currency("AUD", "Australian Dollar", "A$"),
]

CUSTOMERS = [
    Customer("C001", "Alice", "Johnson", "alice.johnson@example.com", "+64 21 123 4567"),
    Customer("C002", "Bob", "Brown", "bob.brown@example.com", "+64 22 765 4321"),
    Customer("C003", "Carol", "Davis", "carol.davis@example.com", "+64 27 111 2222"),
    Customer("C004", "David", "Wilson", "david.wilson@example.com", "+64 29 333 4444"),
]

# Rates effective 19 August 2026 (how many quote units per 1 base unit).
EXCHANGE_RATES = [
    ExchangeRate("NZD", "USD", Decimal("0.610000"), date(2026, 8, 19)),
    ExchangeRate("USD", "NZD", Decimal("1.640000"), date(2026, 8, 19)),
    ExchangeRate("NZD", "EUR", Decimal("0.550000"), date(2026, 8, 19)),
    ExchangeRate("EUR", "NZD", Decimal("1.820000"), date(2026, 8, 19)),
    ExchangeRate("NZD", "GBP", Decimal("0.470000"), date(2026, 8, 19)),
    ExchangeRate("GBP", "NZD", Decimal("2.130000"), date(2026, 8, 19)),
    ExchangeRate("USD", "EUR", Decimal("0.900000"), date(2026, 8, 19)),
    ExchangeRate("EUR", "USD", Decimal("1.110000"), date(2026, 8, 19)),
    ExchangeRate("NZD", "AUD", Decimal("0.920000"), date(2026, 8, 19)),
    ExchangeRate("AUD", "NZD", Decimal("1.090000"), date(2026, 8, 19)),
]

TRANSACTIONS = [
    Transaction("C001", "NZD", "USD", Decimal("1000.00"), Decimal("610.00"), Decimal("0.610000"), date(2026, 8, 19)),
    Transaction("C002", "USD", "NZD", Decimal("500.00"), Decimal("820.00"), Decimal("1.640000"), date(2026, 8, 19)),
    Transaction("C003", "EUR", "NZD", Decimal("200.00"), Decimal("364.00"), Decimal("1.820000"), date(2026, 8, 19)),
    Transaction("C001", "NZD", "EUR", Decimal("300.00"), Decimal("165.00"), Decimal("0.550000"), date(2026, 8, 20)),
    Transaction("C004", "GBP", "NZD", Decimal("100.00"), Decimal("213.00"), Decimal("2.130000"), date(2026, 8, 20)),
]


class Seeder:
    """Populates the database with the sample data."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._currencies = CurrencyRepository(connection)
        self._customers = CustomerRepository(connection)
        self._rates = ExchangeRateRepository(connection)
        self._transactions = TransactionRepository(connection)

    def seed(self) -> dict[str, int]:
        """Insert sample data in foreign-key-safe order and return row counts."""
        self._currencies.insert_many(CURRENCIES)
        self._customers.insert_many(CUSTOMERS)
        self._rates.insert_many(EXCHANGE_RATES)
        self._transactions.insert_many(TRANSACTIONS)

        return {
            "currencies": len(CURRENCIES),
            "customers": len(CUSTOMERS),
            "exchange_rates": len(EXCHANGE_RATES),
            "transactions": len(TRANSACTIONS),
        }

    def seed_if_empty(self) -> dict[str, int] | None:
        """Seed only when the database has no customers yet, else do nothing."""
        if self._customers.count() > 0:
            return None
        return self.seed()
