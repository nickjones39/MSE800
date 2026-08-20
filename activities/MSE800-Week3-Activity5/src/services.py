"""Application services.

Service objects coordinate repositories and translate database errors into
friendly, user-facing messages. The CLI (:mod:`cli`) depends on these rather
than talking to repositories directly.

``ExchangeService.record_exchange`` is the core business operation: it looks up
the latest exchange rate for a currency pair and records a transaction using
that rate.
"""

from __future__ import annotations

from datetime import date
from decimal import ROUND_HALF_UP, Decimal

import psycopg

from .models import Currency, Customer, ExchangeRate, Transaction
from .repositories import (
    CurrencyRepository,
    CustomerRepository,
    ExchangeRateRepository,
    TransactionRepository,
)

TWO_DP = Decimal("0.01")


class ExchangeService:
    """Customer and currency-exchange operations."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection
        self._customers = CustomerRepository(connection)
        self._currencies = CurrencyRepository(connection)
        self._rates = ExchangeRateRepository(connection)
        self._transactions = TransactionRepository(connection)

    # ------------------------------------------------------------ customers
    def add_customer(
        self, customer_id: str, first_name: str, last_name: str, email: str, phone: str
    ) -> None:
        """Add a customer. Raises ``ValueError`` on a duplicate ID or email."""
        customer = Customer(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        try:
            # Run the insert in a savepoint so a duplicate-ID/email error does
            # not abort the enclosing (session) transaction.
            with self._connection.transaction():
                self._customers.insert(customer)
        except psycopg.errors.UniqueViolation as exc:
            raise ValueError("A customer with that ID or email already exists.") from exc

    def list_customers(self) -> list[Customer]:
        return self._customers.find_all()

    # ----------------------------------------------------------- currencies
    def list_currencies(self) -> list[Currency]:
        return self._currencies.find_all()

    # ------------------------------------------------------ exchange rates
    def list_rates(self) -> list[ExchangeRate]:
        return self._rates.find_all()

    # -------------------------------------------------------- transactions
    def list_transactions(self) -> list[dict]:
        return self._transactions.find_all()

    def record_exchange(
        self,
        customer_id: str,
        base_currency: str,
        quote_currency: str,
        amount_base: Decimal,
        transaction_date: date,
    ) -> Transaction:
        """Record a currency exchange using the latest available rate.

        Raises ``ValueError`` for an unknown customer/currency, an invalid pair,
        or when no rate is quoted for the requested pair.
        """
        if not self._customers.exists(customer_id):
            raise ValueError("Unknown customer ID.")
        if not self._currencies.exists(base_currency):
            raise ValueError("Unknown base currency.")
        if not self._currencies.exists(quote_currency):
            raise ValueError("Unknown quote currency.")
        if base_currency == quote_currency:
            raise ValueError("Base and quote currency must be different.")
        if amount_base <= 0:
            raise ValueError("Amount must be greater than zero.")

        rate = self._rates.find_latest(base_currency, quote_currency)
        if rate is None:
            raise ValueError(
                f"No exchange rate is quoted for {base_currency} -> {quote_currency}."
            )

        amount_quote = (amount_base * rate.rate).quantize(TWO_DP, rounding=ROUND_HALF_UP)

        transaction = Transaction(
            customer_id=customer_id,
            base_currency=base_currency,
            quote_currency=quote_currency,
            amount_base=amount_base,
            amount_quote=amount_quote,
            rate_used=rate.rate,
            transaction_date=transaction_date,
        )
        self._transactions.insert(transaction)
        return transaction
