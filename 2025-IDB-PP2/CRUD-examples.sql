-- instructor CRUD
-- Create
INSERT INTO instructor (instructor_id, first_name, middle_name, last_name, salary)
VALUES (..., ..., ..., ..., ...);

-- Read
SELECT ... FROM instructor;

-- Update
UPDATE instructor
SET salary = ...
WHERE instructor_id = ...;

-- Delete
DELETE FROM instructor
WHERE instructor_id = ...;

-- student CRUD
-- Create
INSERT INTO student (student_id, first_name, middle_name, last_name, enrollment_year, total_credits)
VALUES (..., ..., ..., ..., ..., ...);

-- Read
SELECT ... FROM student;

-- Update
UPDATE student
SET total_credits = ...
WHERE student_id = ...;

-- Delete
DELETE FROM student
WHERE student_id = ...;

-- section CRUD
-- Create
INSERT INTO section (sec_code, semester, year)
VALUES (..., ..., ...);

-- Read
SELECT ... FROM section;

-- Update
UPDATE section
SET semester = ..., year = ...
WHERE sec_code = ...;

-- Delete
DELETE FROM section
WHERE sec_code = ...;

-- enrolling
INSERT INTO enrollment (grade)
VALUES (...);

INSERT INTO enrolled (student_id, enrollment_id)
VALUES (..., ...);

-- assign an instructor to a section
INSERT INTO teaches (instructor_id, section_id)
VALUES (..., ...);

-- drop a class
DELETE FROM enrolled
WHERE student_id = ... AND enrollment_id = ...;

DELETE FROM enrollment
WHERE enrollment_id = ...;

-- giving a grade
UPDATE enrollment
SET grade = ...
WHERE enrollment_id = ...;

-- relationship stuff
-- assign major to student
INSERT INTO declared (student_id, major_id)
VALUES (..., ...);

-- assign instructor to department
INSERT INTO employed (instructor_id, dept_id)
VALUES (..., ...);

-- link course to section
INSERT INTO has_sections (section_id, course_id)
VALUES (..., ...);

-- link department to course
INSERT INTO has_course (dept_id, course_id)
VALUES (..., ...);

-- link major under department
INSERT INTO under (major_id, dept_id)
VALUES (..., ...);

-- link section to time slot
INSERT INTO held_during (section_id, time_slot_id)
VALUES (..., ...);

-- link section to classroom
INSERT INTO held_in (section_id, room_id)
VALUES (..., ...);

-- link section to enrollment
INSERT INTO is_offered (section_id, enrollment_id)
VALUES (..., ...);
