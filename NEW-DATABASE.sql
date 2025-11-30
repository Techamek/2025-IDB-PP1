CREATE DATABASE university_project;
USE university_project;

CREATE TABLE department (
    dept_id       CHAR(5) PRIMARY KEY,
    dept_name     VARCHAR(50) UNIQUE NOT NULL,
    building      VARCHAR(20),
    budget        DECIMAL(12,2) CHECK (budget >= 0)
);

CREATE TABLE major (
    major_id      CHAR(5) PRIMARY KEY,
    major_name    VARCHAR(50) NOT NULL
);

CREATE TABLE student (
    student_id     CHAR(5) PRIMARY KEY,
    first_name     VARCHAR(30) NOT NULL,
    middle_name    VARCHAR(30) NOT NULL,
    last_name      VARCHAR(30) NOT NULL,
    enrollment_year INT CHECK (enrollment_year BETWEEN 2000 AND 2099),
    total_credits   INT DEFAULT 0 CHECK (total_credits >= 0),
    dept_name      VARCHAR(50) NOT NULL
);

CREATE TABLE instructor (
    instructor_id  CHAR(5) PRIMARY KEY,
    first_name     VARCHAR(30) NOT NULL,
    middle_name    VARCHAR(30) NOT NULL,
    last_name      VARCHAR(30) NOT NULL,
    salary         DECIMAL(10,2) CHECK (salary >= 30000)
);

CREATE TABLE course (
    course_id     CHAR(7) PRIMARY KEY,
    title         VARCHAR(50) NOT NULL,
    credits       INT CHECK (credits BETWEEN 1 AND 5)
);

CREATE TABLE classroom (
    room_id       INT AUTO_INCREMENT PRIMARY KEY,
    building      VARCHAR(20),
    room_number   VARCHAR(10),
    capacity      INT CHECK (capacity > 0),
    UNIQUE (building, room_number)
);

CREATE TABLE time_slot (
    time_slot_id VARCHAR(5) PRIMARY KEY,
    day          VARCHAR(3) CHECK (day IN ('Mon','Tue','Wed','Thu','Fri','Sat')),
    start_hr     INT CHECK (start_hr >= 0 AND start_hr < 24),
    start_min    INT CHECK (start_min >= 0 AND start_min < 60),
    end_hr       INT CHECK (end_hr >= 0 AND end_hr < 24),
    end_min      INT CHECK (end_min >= 0 AND end_min < 60)
);

CREATE TABLE section (
    section_id   INT AUTO_INCREMENT PRIMARY KEY,
    sec_code     VARCHAR(5),
    semester     VARCHAR(10) CHECK (semester IN ('Spring','Summer','Fall','Winter')),
    year         INT CHECK (year BETWEEN 2000 AND 2099),
    UNIQUE (semester, year, sec_code)
);

CREATE TABLE enrollment (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    grade         CHAR(2) CHECK (grade IN ('A','B','C','D','F','I','W') OR grade IS NULL)
);

CREATE TABLE teaches (
    instructor_id CHAR(5),
    section_id    INT,
    PRIMARY KEY (instructor_id, section_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id)
        ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES section(section_id)
        ON DELETE CASCADE
);

CREATE TABLE advisor (
    student_id    CHAR(5) PRIMARY KEY,
    instructor_id CHAR(5),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id)
        ON DELETE SET NULL
);

CREATE TABLE prereq (
    course_id  CHAR(7),
    prereq_id  CHAR(7),
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
        ON DELETE CASCADE,
    FOREIGN KEY (prereq_id) REFERENCES course(course_id)
        ON DELETE CASCADE
);

CREATE TABLE under (
    major_id CHAR(5),
    dept_id CHAR(5),
    PRIMARY KEY (major_id, dept_id),
    FOREIGN KEY (major_id) REFERENCES major(major_id),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE declared (
    student_id CHAR(5),
    major_id CHAR(5),
    PRIMARY KEY (student_id, major_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (major_id) REFERENCES major(major_id)
);

CREATE TABLE enrolled (
    student_id CHAR(5),
    enrollment_id INT,
    PRIMARY KEY (student_id, enrollment_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (enrollment_id) REFERENCES enrollment(enrollment_id)
);

CREATE TABLE employed (
    instructor_id CHAR(5),
    dept_id CHAR(5),
    PRIMARY KEY (instructor_id, dept_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE held_in (
    section_id INT,
    room_id INT,
    PRIMARY KEY (section_id, room_id),
    FOREIGN KEY (section_id) REFERENCES section(section_id),
    FOREIGN KEY (room_id) REFERENCES classroom(room_id)
);

CREATE TABLE is_offered (
    section_id INT,
    enrollment_id INT,
    PRIMARY KEY (section_id, enrollment_id),
    FOREIGN KEY (section_id) REFERENCES section(section_id),
    FOREIGN KEY (enrollment_id) REFERENCES enrollment(enrollment_id)
);

CREATE TABLE held_during (
    section_id INT,
    time_slot_id varchar(5),
    PRIMARY KEY (section_id, time_slot_id),
    FOREIGN KEY (section_id) REFERENCES section(section_id),
    FOREIGN KEY (time_slot_id) REFERENCES time_slot(time_slot_id)
);

CREATE TABLE has_sections (
    section_id INT,
    course_id char(7),
    PRIMARY KEY (section_id, course_id),
    FOREIGN KEY (section_id) REFERENCES section(section_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE has_course (
    dept_id       CHAR(5),
    course_id     char(7),
    PRIMARY KEY (dept_id, course_id),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);
