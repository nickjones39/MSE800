"""Analytical queries that answer the two questions in the brief.

Both queries join through ``lecture`` because an enrollment references a
lecture, and a lecture belongs to exactly one ``subject`` (a "course").
"""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row

STUDENTS_PER_COURSE_SQL = """
    SELECT
        sub.subject_code,
        sub.subject_unit,
        COUNT(DISTINCT e.nid) AS registered_students
    FROM subject AS sub
    LEFT JOIN lecture AS lec ON lec.subject_code = sub.subject_code
    LEFT JOIN enrollment AS e ON e.lecture_id = lec.lecture_id
    GROUP BY sub.subject_code, sub.subject_unit
    ORDER BY sub.subject_code
"""

STUDENTS_IN_MULTIPLE_COURSES_SQL = """
    SELECT
        s.nid,
        s.f_name,
        s.l_name,
        COUNT(DISTINCT lec.subject_code) AS courses_enrolled
    FROM student AS s
    JOIN enrollment AS e ON e.nid = s.nid
    JOIN lecture AS lec ON lec.lecture_id = e.lecture_id
    GROUP BY s.nid, s.f_name, s.l_name
    HAVING COUNT(DISTINCT lec.subject_code) > 1
    ORDER BY s.nid
"""


class QueryService:
    """Runs the report queries and returns rows as lists of dictionaries."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection

    def _fetch(self, sql: str) -> list[dict[str, Any]]:
        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def students_per_course(self) -> list[dict[str, Any]]:
        """How many students are registered in each course?"""
        return self._fetch(STUDENTS_PER_COURSE_SQL)

    def students_in_multiple_courses(self) -> list[dict[str, Any]]:
        """Names and student IDs of students enrolled in more than one course."""
        return self._fetch(STUDENTS_IN_MULTIPLE_COURSES_SQL)
