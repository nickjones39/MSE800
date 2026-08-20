"""Application services.

Service objects coordinate repositories and translate database errors into
friendly, user-facing messages. The CLI (:mod:`cli`) depends on these rather
than talking to repositories directly.
"""

from __future__ import annotations

from datetime import date

import psycopg

from .models import Student
from .repositories import EnrollmentRepository, StudentRepository


class StudentService:
    """Student CRUD operations."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection
        self._students = StudentRepository(connection)
        self._enrollments = EnrollmentRepository(connection)

    def add_student(
        self, nid: str, f_name: str, l_name: str, b_date: date, email: str
    ) -> None:
        """Add a student. Raises ``ValueError`` on a duplicate ID or email."""
        student = Student(
            nid=nid, f_name=f_name, l_name=l_name, b_date=b_date, email=email
        )
        try:
            # Run the insert in a savepoint so a duplicate-ID/email error does
            # not abort the enclosing (session) transaction.
            with self._connection.transaction():
                self._students.insert(student)
        except psycopg.errors.UniqueViolation as exc:
            raise ValueError(
                "A student with that ID or email already exists."
            ) from exc

    def list_students(self) -> list[Student]:
        """Return all students ordered by ID."""
        return self._students.find_all()

    def search_students(self, name: str) -> list[Student]:
        """Return students whose first or last name contains ``name``."""
        return self._students.find_by_name(name)

    def delete_student(self, nid: str) -> bool:
        """Delete a student (and their enrollments). Returns False if unknown."""
        if not self._students.exists(nid):
            return False
        self._enrollments.delete_by_nid(nid)
        self._students.delete_by_nid(nid)
        return True
