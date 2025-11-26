USE university_project;

-- Insert departments
INSERT INTO department (dept_id, dept_name, building, budget)
VALUES
('D01', 'Computer Science', 'Taylor', 1500000);

-- Insert majors
INSERT INTO major (major_id, major_name)
VALUES
('M01', 'Software Engineering');

-- Insert instructors
INSERT INTO instructor (instructor_id, first_name, middle_name, last_name, salary)
VALUES
('I1001', 'Son', 'Middlename', 'Goku', 95000);

-- Insert students
INSERT INTO student (student_id, first_name, middle_name, last_name, enrollment_year, total_credits)
VALUES
('S2001', 'David', 'Middlename', 'Austin', 2024, 30);

-- Insert courses
INSERT INTO course (course_id, title, credits)
VALUES
('CS101', 'Intro to Programming', 3),
('CS201', 'Super Programming', 4);

-- Insert classrooms
INSERT INTO classroom (building, room_number, capacity)
VALUES
('Taylor', '101', 40);

-- Insert sections
INSERT INTO section (sec_code, semester, year)
VALUES
('001', 'Fall', 2025);

-- Insert timeslot
INSERT INTO time_slot(time_slot_id, day, start_hr, start_min, end_hr, end_min)
VALUES
('TS001', 'Mon', 12, 30, 1, 25);

-- Assign instructors to sections
INSERT INTO teaches (instructor_id, section_id)
VALUES
('I1001', 1);

-- Enroll students
INSERT INTO enrollment (grade)
VALUES
('A');

-- Advisors
INSERT INTO advisor (student_id, instructor_id)
VALUES
('S2001', 'I1001');

-- Prerequisites
INSERT INTO prereq (course_id, prereq_id)
VALUES
('CS201', 'CS101');

-- Major in a dept
INSERT INTO under (major_id, dept_id)
VALUES
('M01', 'D01');

-- student in a major
INSERT INTO declared (student_id, major_id)
VALUES
('S2001', 'M01');

-- student in a class
INSERT INTO enrolled (student_id, enrollment_id)
VALUES
('S2001', 1);

-- teacher in a department
INSERT INTO employed (instructor_id, dept_id)
VALUES
('I1001', 'D01');

-- section in a room
INSERT INTO held_in (section_id, room_id)
VALUES
(1, 1);

-- section is available
INSERT INTO is_offered (section_id, enrollment_id)
VALUES
(1, 1);

-- section at what time
INSERT INTO held_during (section_id, time_slot_id)
VALUES
(1, 'TS001');

-- class has what sections
INSERT INTO has_sections (section_id, course_id)
VALUES
(1, 'CS101');

-- depts have what courses
INSERT INTO has_course (dept_id, course_id)
VALUES
('D01', 'CS101');
