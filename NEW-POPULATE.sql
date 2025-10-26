-- Insert departments
INSERT INTO department (dept_id, dept_name, building, budget)
VALUES
('D01', 'Computer Science', 'Taylor', 1500000);

-- Insert majors
INSERT INTO major (major_id, major_name, dept_id)
VALUES
('M01', 'Software Engineering', 'D01');

-- Insert instructors
INSERT INTO instructor (instructor_id, name, dept_id, salary)
VALUES
('I1001', 'Goku Lastname', 'D01', 95000);

-- Insert students
INSERT INTO student (student_id, name, major_id, enrollment_year, total_credits)
VALUES
('S2001', 'David Austin', 'M01', 2024, 30);
-- Insert courses
INSERT INTO course (course_id, title, dept_id, credits)
VALUES
('CS101', 'Intro to Programming', 'D01', 3);

-- Insert classrooms
INSERT INTO classroom (building, room_number, capacity)
VALUES
('Taylor', '101', 40);

-- Insert sections
INSERT INTO section (course_id, semester, year, room_id, time_slot)
VALUES
('CS101', 'Fall', 2025, 1, 'A');

-- Assign instructors to sections
INSERT INTO teaches (instructor_id, section_id)
VALUES
('I1001', 1);

-- Enroll students
INSERT INTO enrollment (student_id, section_id, grade)
VALUES
('S2001', 1, 'A');

-- Advisors
INSERT INTO advisor (student_id, instructor_id)
VALUES
('S2001', 'I1001');

-- Prerequisites
INSERT INTO prereq (course_id, prereq_id)
VALUES
('CS201', 'CS101');
