CREATE DATABASE university_project;
USE university_project;

CREATE TABLE department (
    dept_id       CHAR(5)      PRIMARY KEY,
    dept_name     VARCHAR(50)  UNIQUE NOT NULL,
    building      VARCHAR(20),
    budget        DECIMAL(12,2) CHECK (budget >= 0)
);

CREATE TABLE major (
    major_id      CHAR(5)      PRIMARY KEY,
    major_name    VARCHAR(50)  NOT NULL,
    dept_id       CHAR(5)      REFERENCES department(dept_id)
);

CREATE TABLE student (
    student_id    CHAR(5)      PRIMARY KEY,
    name          VARCHAR(30)  NOT NULL,
    major_id      CHAR(5)      REFERENCES major(major_id),
    enrollment_year INT        CHECK (enrollment_year BETWEEN 2000 AND 2099),
    total_credits  INT         DEFAULT 0 CHECK (total_credits >= 0)
);

CREATE TABLE instructor (
    instructor_id  CHAR(5)      PRIMARY KEY,
    name           VARCHAR(30)  NOT NULL,
    dept_id        CHAR(5)      REFERENCES department(dept_id),
    salary         DECIMAL(10,2) CHECK (salary >= 30000)
);

CREATE TABLE course (
    course_id     CHAR(7)      PRIMARY KEY,
    title         VARCHAR(50)  NOT NULL,
    dept_id       CHAR(5)      REFERENCES department(dept_id),
    credits       INT          CHECK (credits BETWEEN 1 AND 5)
);

CREATE TABLE classroom (
    room_id       SERIAL       PRIMARY KEY,
    building      VARCHAR(20),
    room_number   VARCHAR(10),
    capacity      INT CHECK (capacity > 0)
);

CREATE TABLE section (
    section_id    SERIAL       PRIMARY KEY,
    course_id     CHAR(7)      REFERENCES course(course_id),
    semester      VARCHAR(10)  CHECK (semester IN ('Spring','Summer','Fall','Winter')),
    year          INT CHECK (year BETWEEN 2000 AND 2099),
    room_id       INT          REFERENCES classroom(room_id),
    time_slot     VARCHAR(5)
);

CREATE TABLE enrollment (
    enrollment_id SERIAL       PRIMARY KEY,
    student_id    CHAR(5)      REFERENCES student(student_id),
    section_id    INT          REFERENCES section(section_id),
    grade         CHAR(2) CHECK (grade IN ('A','B','C','D','F','I','W') OR grade IS NULL),
    UNIQUE(student_id, section_id)
);

CREATE TABLE teaches (
    instructor_id CHAR(5)      REFERENCES instructor(instructor_id),
    section_id    INT          REFERENCES section(section_id),
    PRIMARY KEY(instructor_id, section_id)
);

CREATE TABLE advisor (
    student_id    CHAR(5) PRIMARY KEY REFERENCES student(student_id),
    instructor_id CHAR(5) REFERENCES instructor(instructor_id)
);

CREATE TABLE prereq (
    course_id     CHAR(7) REFERENCES course(course_id),
    prereq_id     CHAR(7) REFERENCES course(course_id),
    PRIMARY KEY(course_id, prereq_id)
);
