"""Relational schema (DDL) and schema management.

The tables below are the relational mapping of the updated ER diagram
(``er_diagram.tex``). Foreign keys materialise the two relationships:

* ``enrollment.nid``        and ``enrollment.lecture_id``  -> *Enrolls*
* ``lecture.lecturer_id``   and ``lecture.subject_code``    -> *Lectures*

``SchemaManager.ensure`` creates any missing tables (non-destructive), while
``reset`` drops and recreates everything (used to re-seed a clean database).
"""

from __future__ import annotations

import psycopg

DROP_STATEMENTS: tuple[str, ...] = (
    "DROP TABLE IF EXISTS enrollment CASCADE",
    "DROP TABLE IF EXISTS lecture CASCADE",
    "DROP TABLE IF EXISTS subject CASCADE",
    "DROP TABLE IF EXISTS lecturer CASCADE",
    "DROP TABLE IF EXISTS student CASCADE",
)

CREATE_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS student (
        nid     VARCHAR(10)  PRIMARY KEY,
        f_name  VARCHAR(50)  NOT NULL,
        l_name  VARCHAR(50)  NOT NULL,
        b_date  DATE         NOT NULL,
        email   VARCHAR(120) NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lecturer (
        lecturer_id VARCHAR(10)  PRIMARY KEY,
        l_firstname VARCHAR(50)  NOT NULL,
        l_lastname  VARCHAR(50)  NOT NULL,
        l_email     VARCHAR(120) NOT NULL UNIQUE,
        l_address   VARCHAR(200)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS subject (
        subject_code VARCHAR(10)  PRIMARY KEY,
        subject_unit VARCHAR(100) NOT NULL,
        description  TEXT         NOT NULL,
        credits      SMALLINT     NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lecture (
        lecture_id   VARCHAR(10)  PRIMARY KEY,
        lecture_name VARCHAR(100) NOT NULL,
        start_time   TIME         NOT NULL,
        lecture_date DATE         NOT NULL,
        room         VARCHAR(20),
        lecturer_id  VARCHAR(10)  NOT NULL REFERENCES lecturer(lecturer_id),
        subject_code VARCHAR(10)  NOT NULL REFERENCES subject(subject_code)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS enrollment (
        enrollment_id     SERIAL      PRIMARY KEY,
        nid               VARCHAR(10) NOT NULL REFERENCES student(nid),
        lecture_id        VARCHAR(10) NOT NULL REFERENCES lecture(lecture_id),
        date_of_enrolment DATE        NOT NULL,
        grade             VARCHAR(3)
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
