-- MSE800 Week 3 — report queries
--
-- "course" == a subject. An enrollment references a lecture, and each lecture
-- belongs to exactly one subject, so the queries join through `lecture`.

-- Q1. How many students are registered in each course?
SELECT
    sub.subject_code,
    sub.subject_unit,
    COUNT(DISTINCT e.nid) AS registered_students
FROM subject AS sub
LEFT JOIN lecture AS lec ON lec.subject_code = sub.subject_code
LEFT JOIN enrollment AS e ON e.lecture_id = lec.lecture_id
GROUP BY sub.subject_code, sub.subject_unit
ORDER BY sub.subject_code;

-- Q2. List the names and student IDs of students who have enrolled in more
--     than one course.
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
ORDER BY s.nid;
