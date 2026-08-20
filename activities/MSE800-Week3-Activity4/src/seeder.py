"""Sample data and database seeding.

The sample data satisfies the brief:

* 8 courses from the programme specification (the ``subject`` table),
* 2 lecturers,
* 5 students,
* appropriate enrollment records (9 records, so several students are enrolled
  in more than one course), and
* the lecture sessions those records reference.
"""

from __future__ import annotations

from datetime import date, time

import psycopg

from .models import Enrollment, Lecturer, Lecture, Student, Subject
from .repositories import (
    EnrollmentRepository,
    LecturerRepository,
    LectureRepository,
    StudentRepository,
    SubjectRepository,
)

SUBJECTS = [
    Subject("MSE800", "Professional Software Engineering", "This course will expose students to concepts, techniques, and frameworks for designing single and n-tier applications using modern software engineering tools. Students will be introduced to the software design process, software life cycle models, requirements engineering, formal specification, and validation.", 30),
    Subject("MSE801", "Research Methods", "Introduces advanced design thinking skills, and research and writing methods, required for this level of learning and application in the software industry; these skills will particularly be applied to the latter stage of the programme.", 15),
    Subject("MSE802", "Quantum Computing", "This course introduces quantum computation, a model of computation based on the physical laws of quantum mechanics.", 15),
    Subject("MSE803", "Data Analytics", "This course will provide students with a thorough practical understanding of applied data analytics and working knowledge of how to apply the most prevalent types of data processing tools and techniques to gain insight into organisation business data.", 15),
    Subject("MSE804", "Blockchain and Decentralised Digital Identity", "The course is designed to provide students with in-depth knowledge of blockchain technology and applications, digital currency, and decentralised identity and the ability to apply how the opportunities presented by these innovations can be leveraged across different sectors including, for example, agriculture, finance, information security and health.", 15),
    Subject("MSE805", "Cloud Security", "The aim of this course is to provide a developed understanding of what is required to secure a cloud ecosystem. The concepts and principles discussed will help bridge the gaps between traditional and cloud architectures while accounting for the shifting thought patterns involving enterprise risk management.", 15),
    Subject("MSE806", "Intelligent Transportation Systems", "This course focuses on how artificial intelligence and machine learning can be deployed in developing the intelligent transportation systems (ITS) by focusing on systems and technological aspects to provide a sustainable society.", 15),
    Subject("MSE907", "Industry-Based Capstone Research Project", "This course is designed to provide students with an opportunity to engage in high-level inquiry, through undertaking a practice-centred industry focused capstone project that advances knowledge within the software engineering domain and meets industry needs.", 60),
]

LECTURERS = [
    Lecturer("L001", "Jane", "Smith", "jane.smith@university.ac.nz", "12 Victoria St, Wellington"),
    Lecturer("L002", "John", "Doe", "john.doe@university.ac.nz", "34 Lambton Quay, Wellington"),
]

STUDENTS = [
    Student("S1001", "Alice", "Johnson", date(2001, 3, 14), "alice.johnson@student.ac.nz"),
    Student("S1002", "Bob", "Brown", date(2000, 7, 22), "bob.brown@student.ac.nz"),
    Student("S1003", "Carol", "Davis", date(2002, 11, 2), "carol.davis@student.ac.nz"),
    Student("S1004", "David", "Wilson", date(2001, 1, 30), "david.wilson@student.ac.nz"),
    Student("S1005", "Eve", "Martinez", date(2000, 9, 18), "eve.martinez@student.ac.nz"),
]

LECTURES = [
    Lecture("LEC001", "MSE800 Lecture", time(9, 0), date(2026, 2, 9), "R101", "L001", "MSE800"),
    Lecture("LEC002", "MSE801 Lecture", time(10, 0), date(2026, 2, 9), "R102", "L002", "MSE801"),
    Lecture("LEC003", "MSE802 Lecture", time(11, 0), date(2026, 2, 10), "R103", "L001", "MSE802"),
    Lecture("LEC004", "MSE803 Lecture", time(9, 0), date(2026, 2, 10), "R104", "L002", "MSE803"),
    Lecture("LEC005", "MSE804 Lecture", time(10, 0), date(2026, 2, 11), "R105", "L001", "MSE804"),
    Lecture("LEC006", "MSE805 Lecture", time(11, 0), date(2026, 2, 11), "R106", "L002", "MSE805"),
    Lecture("LEC007", "MSE806 Lecture", time(9, 0), date(2026, 2, 12), "R107", "L001", "MSE806"),
    Lecture("LEC008", "MSE907 Lecture", time(10, 0), date(2026, 2, 12), "R108", "L002", "MSE907"),
]

# (nid, lecture_id, date_of_enrolment, grade)
ENROLLMENTS = [
    Enrollment("S1001", "LEC001", date(2026, 2, 9), "A"),
    Enrollment("S1001", "LEC002", date(2026, 2, 9), "A-"),
    Enrollment("S1002", "LEC001", date(2026, 2, 9), "B"),
    Enrollment("S1002", "LEC003", date(2026, 2, 10), "B+"),
    Enrollment("S1003", "LEC004", date(2026, 2, 10), "B+"),
    Enrollment("S1003", "LEC005", date(2026, 2, 11), "B"),
    Enrollment("S1004", "LEC006", date(2026, 2, 11), "A-"),
    Enrollment("S1005", "LEC007", date(2026, 2, 12), "A-"),
    Enrollment("S1005", "LEC008", date(2026, 2, 12), "B+"),
]


class Seeder:
    """Populates the database with the sample data."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._subjects = SubjectRepository(connection)
        self._lecturers = LecturerRepository(connection)
        self._students = StudentRepository(connection)
        self._lectures = LectureRepository(connection)
        self._enrollments = EnrollmentRepository(connection)

    def seed(self) -> dict[str, int]:
        """Insert sample data in foreign-key-safe order and return row counts."""
        self._subjects.insert_many(SUBJECTS)
        self._lecturers.insert_many(LECTURERS)
        self._students.insert_many(STUDENTS)
        self._lectures.insert_many(LECTURES)
        self._enrollments.insert_many(ENROLLMENTS)

        return {
            "subjects": len(SUBJECTS),
            "lecturers": len(LECTURERS),
            "students": len(STUDENTS),
            "lectures": len(LECTURES),
            "enrollments": len(ENROLLMENTS),
        }

    def seed_if_empty(self) -> dict[str, int] | None:
        """Seed only when the database has no students yet, else do nothing."""
        if self._students.count() > 0:
            return None
        return self.seed()
