"""Interactive command-line interface.

A menu-driven CLI that exposes the customer and exchange operations together
with the report queries and a database reset.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Iterable, Mapping

import psycopg

from .models import Currency, Customer, ExchangeRate
from .queries import QueryService
from .schema import SchemaManager
from .seeder import Seeder
from .services import ExchangeService


def print_table(title: str, rows: Iterable[Mapping]) -> None:
    """Print a list of mappings as a simple aligned table."""
    rows = list(rows)
    print(f"\n{title}")
    if not rows:
        print("  (no rows)")
        return

    headers = list(rows[0].keys())
    widths = {header: len(str(header)) for header in headers}
    for row in rows:
        for header in headers:
            widths[header] = max(widths[header], len(str(row[header])))

    def fmt(row: Mapping) -> str:
        return "  ".join(str(row[h]).ljust(widths[h]) for h in headers)

    print(fmt(dict(zip(headers, headers))))
    print("  ".join("-" * widths[h] for h in headers))
    for row in rows:
        print(fmt(row))


class Cli:
    """Runs the interactive menu loop."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._service = ExchangeService(connection)
        self._reports = QueryService(connection)
        self._schema = SchemaManager(connection)
        self._seeder = Seeder(connection)

    def run(self) -> None:
        while True:
            self._print_menu()
            try:
                choice = input("Select an option (1-8): ").strip()
            except EOFError:
                print()
                break

            if choice == "1":
                self._add_customer()
            elif choice == "2":
                self._view_customers()
            elif choice == "3":
                self._view_rates()
            elif choice == "4":
                self._record_exchange()
            elif choice == "5":
                self._view_transactions()
            elif choice == "6":
                self._run_reports()
            elif choice == "7":
                self._reset_database()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")

    # ------------------------------------------------------------- actions
    def _add_customer(self) -> None:
        try:
            customer_id = self._prompt("Customer ID: ")
            first_name = self._prompt("First name: ")
            last_name = self._prompt("Last name: ")
            email = self._prompt("Email: ")
            phone = self._prompt("Phone: ")
            self._service.add_customer(customer_id, first_name, last_name, email, phone)
            print(" Customer added successfully.")
        except ValueError as exc:
            print(f" {exc}")

    def _view_customers(self) -> None:
        self._print_customers(self._service.list_customers())

    def _view_rates(self) -> None:
        self._print_rates(self._service.list_rates())

    def _record_exchange(self) -> None:
        try:
            customer_id = self._prompt("Customer ID: ")
            base_currency = self._prompt("Base currency code (e.g. NZD): ").upper()
            quote_currency = self._prompt("Quote currency code (e.g. USD): ").upper()
            amount_base = self._prompt_amount("Amount to exchange: ")
            transaction = self._service.record_exchange(
                customer_id, base_currency, quote_currency, amount_base, date.today()
            )
            print(
                f" Exchanged {transaction.amount_base} {transaction.base_currency} "
                f"-> {transaction.amount_quote} {transaction.quote_currency} "
                f"(rate {transaction.rate_used})."
            )
        except ValueError as exc:
            print(f" {exc}")

    def _view_transactions(self) -> None:
        print_table("Transactions", self._service.list_transactions())

    def _run_reports(self) -> None:
        print_table(
            "Q1. Total value exchanged by each customer.",
            self._reports.customer_totals(),
        )
        print_table(
            "Q2. Latest exchange rate for each currency pair.",
            self._reports.latest_rates(),
        )

    def _reset_database(self) -> None:
        self._schema.reset()
        self._seeder.seed()
        print(" Database reset and re-seeded with sample data.")

    # -------------------------------------------------------------- helpers
    @staticmethod
    def _prompt(label: str) -> str:
        value = input(label).strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value

    @staticmethod
    def _prompt_amount(label: str) -> Decimal:
        raw = input(label).strip()
        try:
            amount = Decimal(raw)
        except InvalidOperation as exc:
            raise ValueError("Invalid amount.") from exc
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        return amount

    @staticmethod
    def _print_customers(customers: list[Customer]) -> None:
        if not customers:
            print("  (no customers)")
            return
        rows = [
            {
                "ID": c.customer_id,
                "First name": c.first_name,
                "Last name": c.last_name,
                "Email": c.email,
                "Phone": c.phone,
            }
            for c in customers
        ]
        print_table("Customers", rows)

    @staticmethod
    def _print_rates(rates: list[ExchangeRate]) -> None:
        if not rates:
            print("  (no rates)")
            return
        rows = [
            {
                "Base": r.base_currency,
                "Quote": r.quote_currency,
                "Rate": r.rate,
                "Effective": r.effective_date.strftime("%d/%m/%Y"),
            }
            for r in rates
        ]
        print_table("Exchange rates", rows)

    @staticmethod
    def _print_menu() -> None:
        print("\n==== Money Exchange ====")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. View Exchange Rates")
        print("4. Record an Exchange")
        print("5. View Transactions")
        print("6. Run Report Queries")
        print("7. Reset Database")
        print("8. Exit")
