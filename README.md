# 2025-IDB-PP1
2025 Intro to database design Project, phase 1.

Every main table now has its own short id, like dept_id, major_id, and section_id. 
Students and instructors are linked to departments through these ids instead of department names. 
Students now also have a major, which connects to a department.
Each table includes check constraints for valid data, such as salary limits, credit ranges, and year ranges.
Sections and classrooms now use numeric ids instead of combining building and room numbers.
The takes table from the old version was replaced with a new enrollment table that uses its own id and prevents duplicate enrollments.
