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
