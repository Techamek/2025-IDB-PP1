# 2025-IDB-PP1
2025 Intro to database design Project, phase 1.

every main table now has its own short id, like dept_id, major_id, and section_id. 
students and instructors are linked to departments through these ids instead of department names. 
students now also have a major, which connects to a department.
each table includes check constraints for valid data, such as salary limits, credit ranges, and year ranges.
sections and classrooms now use numeric ids instead of combining building and room numbers.
the takes table from the old version was replaced with a new enrollment table that uses its own id and prevents duplicate enrollments.
