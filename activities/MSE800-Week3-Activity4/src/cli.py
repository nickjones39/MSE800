"""Interactive command-line interface.

A menu-driven CLI that exposes the student CRUD operations (mirroring the
``sql-sample`` example) together with the report queries and a database reset.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, Mapping

import psycopg

from .models import Student
from .queries import QueryService
from .schema import SchemaManager
from .seeder import Seeder
from .services import StudentService


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
        self._students = StudentService(connection)
        self._reports = QueryService(connection)
        self._schema = SchemaManager(connection)
        self._seeder = Seeder(connection)

    def run(self) -> None:
        while True:
            self._print_menu()
            try:
                choice = input("Select an option (1-7): ").strip()
            except EOFError:
                print()
                break

            if choice == "1":
                self._add_student()
            elif choice == "2":
                self._view_students()
            elif choice == "3":
                self._search_student()
            elif choice == "4":
                self._delete_student()
            elif choice == "5":
                self._run_reports()
            elif choice == "6":
                self._reset_database()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")

    # ------------------------------------------------------------- actions
    def _add_student(self) -> None:
        try:
            nid = self._prompt("Student ID (NID): ")
            f_name = self._prompt("First name: ")
            l_name = self._prompt("Last name: ")
            b_date = self._prompt_date("Birth date (DD/MM/YYYY): ")
            email = self._prompt("Email: ")
            self._students.add_student(nid, f_name, l_name, b_date, email)
            print(" Student added successfully.")
        except ValueError as exc:
            print(f" {exc}")

    def _view_students(self) -> None:
        self._print_students(self._students.list_students())

    def _search_student(self) -> None:
        name = self._prompt("Enter name to search: ")
        self._print_students(self._students.search_students(name))

    def _delete_student(self) -> None:
        nid = self._prompt("Enter student ID to delete: ")
        if self._students.delete_student(nid):
            print(" Student deleted.")
        else:
            print(" No student found with that ID.")

    def _run_reports(self) -> None:
        print_table(
            "Q1. How many students are registered in each course?",
            self._reports.students_per_course(),
        )
        print_table(
            "Q2. Students enrolled in more than one course (name + student ID).",
            self._reports.students_in_multiple_courses(),
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
    def _prompt_date(label: str) -> date:
        raw = input(label).strip()
        try:
            return datetime.strptime(raw, "%d/%m/%Y").date()
        except ValueError as exc:
            raise ValueError("Invalid date format; use DD/MM/YYYY.") from exc

    @staticmethod
    def _print_students(students: list[Student]) -> None:
        if not students:
            print("  (no students)")
            return
        rows = [
            {
                "NID": s.nid,
                "First name": s.f_name,
                "Last name": s.l_name,
                "Birth date": s.b_date.strftime("%d/%m/%Y"),
                "Email": s.email,
            }
            for s in students
        ]
        print_table("Students", rows)

    @staticmethod
    def _print_menu() -> None:
        print("\n==== Student Manager ====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by Name")
        print("4. Delete Student by ID")
        print("5. Run Report Queries")
        print("6. Reset Database")
        print("7. Exit")
