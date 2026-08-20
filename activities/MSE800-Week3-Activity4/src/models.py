"""Domain models.

One dataclass per entity in the ER diagram. Field order is significant: it
matches the column order used by the repositories, so
``dataclasses.astuple(record)`` lines up with the ``INSERT`` statement.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time


@dataclass
class Student:
    nid: str
    f_name: str
    l_name: str
    b_date: date
    email: str


@dataclass
class Lecturer:
    lecturer_id: str
    l_firstname: str
    l_lastname: str
    l_email: str
    l_address: str


@dataclass
class Subject:
    subject_code: str
    subject_unit: str
    description: str
    credits: int


@dataclass
class Lecture:
    lecture_id: str
    lecture_name: str
    start_time: time
    lecture_date: date
    room: str
    lecturer_id: str
    subject_code: str


@dataclass
class Enrollment:
    nid: str
    lecture_id: str
    date_of_enrolment: date
    grade: str
