"""MSE800 Week 3 — University enrolment & lecture-management database.

This package contains the object-oriented implementation of a PostgreSQL
project that models the ER diagram in ``er_diagram.tex``.
"""

from .cli import Cli, print_table
from .config import get_settings
from .db import Database
from .models import Enrollment, Lecturer, Lecture, Student, Subject
from .queries import QueryService
from .repositories import (
    EnrollmentRepository,
    LecturerRepository,
    LectureRepository,
    StudentRepository,
    SubjectRepository,
)
from .schema import SchemaManager
from .seeder import Seeder
from .services import StudentService

__all__ = [
    "Cli",
    "Database",
    "Enrollment",
    "EnrollmentRepository",
    "Lecturer",
    "LecturerRepository",
    "Lecture",
    "LectureRepository",
    "QueryService",
    "SchemaManager",
    "Seeder",
    "Student",
    "StudentRepository",
    "StudentService",
    "Subject",
    "SubjectRepository",
    "get_settings",
    "print_table",
]
