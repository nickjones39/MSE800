# MSE800 — Week 3, Activity 4: PostgreSQL Project (University Enrolment & Lecture Management)

Yoobee MSE800, Week 3, Activity 4. A database project developed from the
`starting-ER.png` ER diagram, implemented in **PostgreSQL** and driven by an
**object-oriented Python** application.

The task was to review and update the ER diagram, re-draw it in TikZ/LaTeX,
implement the database, populate it with sample data, and answer two SQL
questions.

---

## 1. Updated ER diagram

The updated diagram is `docs/er_diagram.tex` (Chen notation, drawn with TikZ).
It is also pre-compiled to `docs/er_diagram.pdf`.

To re-compile it (from the `docs/` directory):

```bash
cd docs
pdflatex er_diagram.tex
```

### Changes made in the review

| Change | Detail |
|---|---|
| **Added** `Email` | to the `Student` entity |
| **Added** `Credits` | to the `Subjects` entity |
| **Added** `Description` | to the `Subjects` entity (renamed from `Subject_udsc`) |
| **Added** `Room` | to the `Lecture` entity |
| **Added** `Grade` | to the `Enrollment` entity |
| **Corrected** `Lecturer` key | `Lecture_id` → `Lecturer_id` (a lecturer is identified by their own id) |
| **Corrected** `Enrollment` key | `Student_code` alone cannot identify an enrollment (a student may enrol in several courses), so a surrogate `Enrollment_id` primary key was added |
| **Resolved** course attributes | the overlapping `CC#` / `Subject` / `Subject_code` fields were merged into a single foreign key to `Subjects` |

### Relationship types

The model has two relationships:

* **Enrolls** — a *many-to-many* relationship between `Student` and `Lecture`,
  resolved by the associative entity `Enrollment`. One student may have many
  enrollments (M), one lecture may be taken by many students (M), and each
  enrollment links exactly one student to one lecture (1).

* **Lectures** — a ternary relationship between `Lecturer`, `Lecture` and
  `Subjects`, which decomposes into two *one-to-many* relationships that meet at
  `Lecture`: one lecturer delivers many lectures (1:N), one subject has many
  lectures (1:N), and each lecture is delivered by exactly one lecturer and
  belongs to exactly one subject.

---

## 2. Relational schema

Five tables (one per entity), with the relationships materialised as foreign
keys:

| Table | Columns | Notes |
|---|---|---|
| `student` | `nid` (PK), `f_name`, `l_name`, `b_date`, `email` | `email` added |
| `lecturer` | `lecturer_id` (PK), `l_firstname`, `l_lastname`, `l_email`, `l_address` | key corrected |
| `subject` | `subject_code` (PK), `subject_unit`, `description`, `credits` | "course" in the queries; `credits` + `description` added |
| `lecture` | `lecture_id` (PK), `lecture_name`, `start_time`, `lecture_date`, `room`, `lecturer_id` (FK), `subject_code` (FK) | `room` added |
| `enrollment` | `enrollment_id` (PK, serial), `nid` (FK), `lecture_id` (FK), `date_of_enrolment`, `grade` | `grade` added |

* `enrollment.nid` and `enrollment.lecture_id` implement **Enrolls**.
* `lecture.lecturer_id` and `lecture.subject_code` implement **Lectures**.

---

## 3. Sample data

| Table | Records |
|---|---|
| `subject` (courses) | **8** — the real programme courses (MSE800–MSE806 and MSE907), each with `credits` and a `description` |
| `lecturer` | **2** — Jane Smith, John Doe |
| `student` | **5** — Alice, Bob, Carol, David, Eve |
| `lecture` | 8 lecture sessions (one per course) |
| `enrollment` | 9 enrolment records (several students are enrolled in more than one course) |

The seed data is defined in `src/seeder.py`.

---

## 4. SQL queries

The two questions from the brief, implemented in `src/queries.py` (and also
available standalone in `sql/queries.sql`):

**Q1 — How many students are registered in each course?**

```sql
SELECT sub.subject_code, sub.subject_unit,
       COUNT(DISTINCT e.nid) AS registered_students
FROM subject AS sub
LEFT JOIN lecture AS lec ON lec.subject_code = sub.subject_code
LEFT JOIN enrollment AS e ON e.lecture_id = lec.lecture_id
GROUP BY sub.subject_code, sub.subject_unit
ORDER BY sub.subject_code;
```

**Q2 — List the names and student IDs of students who have enrolled in more than one course.**

```sql
SELECT s.nid, s.f_name, s.l_name,
       COUNT(DISTINCT lec.subject_code) AS courses_enrolled
FROM student AS s
JOIN enrollment AS e ON e.nid = s.nid
JOIN lecture AS lec ON lec.lecture_id = e.lecture_id
GROUP BY s.nid, s.f_name, s.l_name
HAVING COUNT(DISTINCT lec.subject_code) > 1
ORDER BY s.nid;
```

---

## 5. Project structure

```
MSE800-Week3-Activity4/
├── main.py            # entry point: CLI menu / --setup / --report
├── requirements.txt   # Python dependencies
├── .env.example       # connection-string template
├── .env               # your real connection string (git-ignored)
├── docs/
│   ├── er_diagram.tex # updated ER diagram (TikZ/LaTeX)
│   └── er_diagram.pdf # compiled diagram
├── sql/
│   └── queries.sql    # the two report queries
└── src/
    ├── config.py      # settings / env loading
    ├── db.py          # connection management
    ├── models.py      # entity dataclasses
    ├── repositories.py# repository layer (insert + CRUD queries)
    ├── services.py    # application services (StudentService)
    ├── schema.py      # DDL + schema manager
    ├── seeder.py      # sample data
    ├── queries.py     # report queries
    └── cli.py         # interactive student-manager menu
```

The code uses **object-oriented design** (dataclass models, repository pattern,
service layer, a connection facade and a CLI controller), keeping concerns
separate.

---

## 6. Setup

### Prerequisites

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
* A PostgreSQL database — the course uses a **Neon** serverless instance.

### 1. Create the conda environment

```bash
conda create -n MSE800-week3 -c conda-forge python=3.12
conda activate MSE800-week3
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

* `psycopg[binary]` — the PostgreSQL driver
* `python-dotenv` — loads `.env`

### 3. Configure the database connection

Copy `.env.example` to `.env` (a `.env` placeholder already exists) and set your
real connection string, e.g. your Neon URL:

```
DATABASE_URL=postgresql://neondb_owner:YOUR_PASSWORD@your-host/neondb?sslmode=require
```

> The password is read from `.env` (which is git-ignored) and never committed.

---

## 7. Running

### Interactive Student Manager (default)

```bash
python main.py
```

This ensures the schema exists, seeds the sample data the first time it runs
(without wiping anything afterwards), and opens a menu:

```
==== Student Manager ====
1. Add Student
2. View All Students
3. Search Student by Name
4. Delete Student by ID
5. Run Report Queries
6. Reset Database
7. Exit
```

* **Add Student** — prompts for student ID, first name, last name, birth date
  (`DD/MM/YYYY`) and email; rejects duplicate IDs/emails.
* **View All Students** — lists every student.
* **Search Student by Name** — case-insensitive match on first or last name.
* **Delete Student by ID** — removes the student (and their enrollments).
* **Run Report Queries** — prints the two questions below.
* **Reset Database** — drops, recreates and re-seeds the sample data.

### One-shot modes

```bash
python main.py --setup      # drop + recreate + seed, then exit
python main.py --report     # print the two report queries, then exit
```

`--report` prints the answers to the two questions:

```
Q1. How many students are registered in each course?
subject_code  subject_unit                                   registered_students
------------  ---------------------------------------------  -------------------
MSE800        Professional Software Engineering              2
MSE801        Research Methods                               1
MSE802        Quantum Computing                              1
MSE803        Data Analytics                                 1
MSE804        Blockchain and Decentralised Digital Identity  1
MSE805        Cloud Security                                 1
MSE806        Intelligent Transportation Systems             1
MSE907        Industry-Based Capstone Research Project       1

Q2. Students enrolled in more than one course (name + student ID).
nid    f_name  l_name    courses_enrolled
-----  ------  --------  ----------------
S1001  Alice   Johnson   2
S1002  Bob     Brown     2
S1003  Carol   Davis     2
S1005  Eve     Martinez  2
```

---

## Author

Nick Jones
