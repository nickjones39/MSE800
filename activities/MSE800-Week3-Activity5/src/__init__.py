"""MSE800 Week 3 — money exchange database.

This package contains the object-oriented implementation of a PostgreSQL
project that models the ER diagram in ``er_diagram.tex``.
"""

from .cli import Cli, print_table
from .config import get_settings
from .db import Database
from .models import Currency, Customer, ExchangeRate, Transaction
from .queries import QueryService
from .repositories import (
    CurrencyRepository,
    CustomerRepository,
    ExchangeRateRepository,
    TransactionRepository,
)
from .schema import SchemaManager
from .seeder import Seeder
from .services import ExchangeService

__all__ = [
    "Cli",
    "Currency",
    "CurrencyRepository",
    "Customer",
    "CustomerRepository",
    "Database",
    "ExchangeRate",
    "ExchangeRateRepository",
    "ExchangeService",
    "QueryService",
    "SchemaManager",
    "Seeder",
    "Transaction",
    "TransactionRepository",
    "get_settings",
    "print_table",
]
