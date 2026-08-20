"""Entry point for the MSE800 Week 3 Money Exchange project.

Usage:
    python main.py              start the interactive Money Exchange menu
    python main.py --setup      drop, recreate and seed the database, then exit
    python main.py --report     print the two report queries and exit
"""

from __future__ import annotations

import argparse

import psycopg

from src.cli import Cli, print_table
from src.config import get_settings
from src.db import Database
from src.queries import QueryService
from src.schema import SchemaManager
from src.seeder import Seeder


def _run_reports(connection: psycopg.Connection) -> None:
    reports = QueryService(connection)
    print_table(
        "Q1. Total value exchanged by each customer.",
        reports.customer_totals(),
    )
    print_table(
        "Q2. Latest exchange rate for each currency pair.",
        reports.latest_rates(),
    )


def _print_seed_summary(counts: dict[str, int]) -> None:
    print("Database schema created and populated.")
    for table, count in counts.items():
        print(f"  {table:<16} {count} rows")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MSE800 Week 3 — money exchange database (PostgreSQL)."
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="drop, recreate and seed the database, then exit",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="print the two report queries and exit",
    )
    args = parser.parse_args()

    settings = get_settings()
    database = Database(settings.database_url)

    with database.connect() as connection:
        if args.setup:
            SchemaManager(connection).reset()
            _print_seed_summary(Seeder(connection).seed())
            return

        SchemaManager(connection).ensure()
        Seeder(connection).seed_if_empty()

        if args.report:
            _run_reports(connection)
            return

        Cli(connection).run()


if __name__ == "__main__":
    main()
