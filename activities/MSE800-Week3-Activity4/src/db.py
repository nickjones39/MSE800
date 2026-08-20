"""Database connection management.

Wraps a single ``psycopg`` connection string and exposes a connection context
manager. The context manager commits on success and rolls back on error, which
makes the whole ``schema -> seed -> query`` flow atomic in ``main.py``.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import psycopg


class Database:
    """A thin facade over a PostgreSQL connection string."""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    @contextmanager
    def connect(self) -> Iterator[psycopg.Connection]:
        """Open a connection that commits on success and rolls back on error."""
        with psycopg.connect(self._dsn) as connection:
            yield connection
