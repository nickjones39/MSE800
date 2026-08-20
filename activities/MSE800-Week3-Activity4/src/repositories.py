"""Repository layer.

Each entity gets a small repository that knows how to persist and query it. A
shared base class provides the generic ``INSERT`` logic, and each subclass
declares its table name and column order (which must match the corresponding
dataclass field order in :mod:`models`).
"""

from __future__ import annotations

from dataclasses import astuple
from typing import Sequence, TypeVar

import psycopg
from psycopg.rows import dict_row

from .models import Enrollment, Lecturer, Lecture, Student, Subject

T = TypeVar("T")


class Repository:
    """Generic repository: inserts one dataclass row into a table."""

    table: str = ""
    columns: tuple[str, ...] = ()

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection

    def insert(self, record: T) -> None:
        values = astuple(record)
        placeholders = ", ".join(["%s"] * len(self.columns))
        sql = (
            f"INSERT INTO {self.table} ({', '.join(self.columns)}) "
            f"VALUES ({placeholders})"
        )
        self._connection.execute(sql, values)

    def insert_many(self, records: Sequence[T]) -> None:
        for record in records:
            self.insert(record)


class StudentRepository(Repository):
    table = "student"
    columns = ("nid", "f_name", "l_name", "b_date", "email")

    def find_all(self) -> list[Student]:
        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "SELECT nid, f_name, l_name, b_date, email "
                "FROM student ORDER BY nid"
            )
            return [Student(**row) for row in cursor.fetchall()]

    def find_by_name(self, name: str) -> list[Student]:
        pattern = f"%{name}%"
        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "SELECT nid, f_name, l_name, b_date, email FROM student "
                "WHERE f_name ILIKE %s OR l_name ILIKE %s ORDER BY nid",
                (pattern, pattern),
            )
            return [Student(**row) for row in cursor.fetchall()]

    def exists(self, nid: str) -> bool:
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM student WHERE nid = %s", (nid,))
            return cursor.fetchone() is not None

    def delete_by_nid(self, nid: str) -> bool:
        with self._connection.cursor() as cursor:
            cursor.execute("DELETE FROM student WHERE nid = %s", (nid,))
            return cursor.rowcount > 0

    def count(self) -> int:
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM student")
            return cursor.fetchone()[0]


class EnrollmentRepository(Repository):
    table = "enrollment"
    columns = ("nid", "lecture_id", "date_of_enrolment", "grade")

    def delete_by_nid(self, nid: str) -> None:
        """Remove every enrollment belonging to a student (cascade for delete)."""
        with self._connection.cursor() as cursor:
            cursor.execute("DELETE FROM enrollment WHERE nid = %s", (nid,))


class LecturerRepository(Repository):
    table = "lecturer"
    columns = ("lecturer_id", "l_firstname", "l_lastname", "l_email", "l_address")


class SubjectRepository(Repository):
    table = "subject"
    columns = ("subject_code", "subject_unit", "description", "credits")


class LectureRepository(Repository):
    table = "lecture"
    columns = (
        "lecture_id",
        "lecture_name",
        "start_time",
        "lecture_date",
        "room",
        "lecturer_id",
        "subject_code",
    )
