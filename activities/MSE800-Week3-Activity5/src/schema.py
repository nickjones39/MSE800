"""Relational schema (DDL) and schema management.

The tables below are the relational mapping of the ER diagram
(``er_diagram.tex``). Foreign keys materialise the three relationships:

* ``exchange_transaction.customer_id``          -> *Makes*
* ``exchange_transaction.base_currency`` and
  ``exchange_transaction.quote_currency``        -> *Involves*
* ``exchange_rate.base_currency`` and
  ``exchange_rate.quote_currency``               -> *Quotes*

``SchemaManager.ensure`` creates any missing tables (non-destructive), while
``reset`` drops and recreates everything (used to re-seed a clean database).

The transaction table is named ``exchange_transaction`` rather than
``transaction`` because ``transaction`` is a reserved SQL keyword.
"""

from __future__ import annotations

import psycopg

DROP_STATEMENTS: tuple[str, ...] = (
    "DROP TABLE IF EXISTS exchange_transaction CASCADE",
    "DROP TABLE IF EXISTS exchange_rate CASCADE",
    "DROP TABLE IF EXISTS currency CASCADE",
    "DROP TABLE IF EXISTS customer CASCADE",
)

CREATE_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS customer (
        customer_id VARCHAR(10)  PRIMARY KEY,
        first_name  VARCHAR(50)  NOT NULL,
        last_name   VARCHAR(50)  NOT NULL,
        email       VARCHAR(120) NOT NULL UNIQUE,
        phone       VARCHAR(30)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS currency (
        currency_code VARCHAR(3)   PRIMARY KEY,
        currency_name VARCHAR(100) NOT NULL,
        symbol        VARCHAR(5)   NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS exchange_rate (
        rate_id        SERIAL        PRIMARY KEY,
        base_currency  VARCHAR(3)    NOT NULL REFERENCES currency(currency_code),
        quote_currency VARCHAR(3)    NOT NULL REFERENCES currency(currency_code),
        rate           NUMERIC(12,6) NOT NULL,
        effective_date DATE          NOT NULL,
        CONSTRAINT uq_rate UNIQUE (base_currency, quote_currency, effective_date),
        CONSTRAINT chk_rate_positive CHECK (rate > 0),
        CONSTRAINT chk_rate_distinct CHECK (base_currency <> quote_currency)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS exchange_transaction (
        transaction_id   SERIAL        PRIMARY KEY,
        customer_id      VARCHAR(10)   NOT NULL REFERENCES customer(customer_id),
        base_currency    VARCHAR(3)    NOT NULL REFERENCES currency(currency_code),
        quote_currency   VARCHAR(3)    NOT NULL REFERENCES currency(currency_code),
        amount_base      NUMERIC(14,2) NOT NULL,
        amount_quote     NUMERIC(14,2) NOT NULL,
        rate_used        NUMERIC(12,6) NOT NULL,
        transaction_date DATE          NOT NULL,
        CONSTRAINT chk_txn_distinct CHECK (base_currency <> quote_currency),
        CONSTRAINT chk_txn_positive CHECK (amount_base > 0 AND amount_quote > 0)
    )
    """,
)


class SchemaManager:
    """Creates and (optionally) resets the relational schema."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection

    def ensure(self) -> None:
        """Create any missing tables (non-destructive)."""
        for statement in CREATE_STATEMENTS:
            self._connection.execute(statement)

    def reset(self) -> None:
        """Drop and re-create every table in dependency-safe order."""
        for statement in DROP_STATEMENTS:
            self._connection.execute(statement)
        self.ensure()
