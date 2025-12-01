#! /usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re
import config

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

db = config.dblocal

@app.route('/', methods=['GET', 'POST'])
def base():
    if 'loggedin' not in session: #if not logged in, go to login page
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))


# Login route
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']        
        cursor = db.cursor()

        cursor.execute("SELECT * FROM accounts WHERE username = %s", [username])
        account = cursor.fetchone()
        cursor.close()

        # Check if account exists and password is correct
        if account and check_password_hash(account[2], password):

            # Basic session info from accounts table
            session['loggedin'] = True
            session['id'] = account[0] 
            session['username'] = account[1]
            session['role'] = account[4]   
            session['user_ref'] = account[5]   # student_id or instructor_id

            role = account[4]

            cursor = db.cursor()

            if role == "Student":
                cursor.execute("""
                    SELECT student_id, first_name, middle_name, last_name, enrollment_year, total_credits
                    FROM student
                    WHERE student_id = %s
                """, [session['user_ref']])  # <-- CORRECT: use user_ref, NOT username

                student = cursor.fetchone()

                if student:
                    session['student_id'] = student[0]
                    session['fname'] = student[1]
                    session['mname'] = student[2]
                    session['lname'] = student[3]
                    session['year'] = student[4]
                    session['credits'] = student[5]


            elif role == "Instructor":
                cursor.execute("""
                    SELECT instructor_id, first_name, middle_name, last_name, salary
                    FROM instructor
                    WHERE instructor_id = %s
                """, [session['user_ref']])  # <-- CORRECT: use user_ref

                instructor = cursor.fetchone()

                if instructor:
                    session['instructor_id'] = instructor[0]
                    session['fname'] = instructor[1]
                    session['mname'] = instructor[2]
                    session['lname'] = instructor[3]
                    session['salary'] = instructor[4]

            cursor.close()

            return redirect(url_for('home'))

        else:
            msg = 'Incorrect username/password!'
    
    return render_template('index.html', msg=msg)


@app.route("/pythonlogin/register", methods=["GET"])
def register():
    return render_template("registerRole.html")

# Register route
@app.route('/pythonlogin/register', methods=['POST'])
def registerRole():
    msg = ''
    role = request.form['role']
    if role == "Administrator":
        return redirect("/register/admin")
    elif role == "Instructor":
        return redirect("/register/instructor")
    elif role == "Student":
        return redirect("/register/student")
    else:
        msg = 'Please fill out the form!'
    
    return render_template('registerRole.html', msg=msg)

@app.route("/register/admin", methods=["GET", "POST"])
def register_admin():
    msg = ''
    if request.method == "POST"  and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = db.cursor()
        sql = "SELECT * FROM accounts WHERE username = %s;"
        cursor.execute(sql, [username])
        account = cursor.fetchall()
        print(account)
        cursor.close()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            role = "Administrator"
            # Hash the password before storing it
            hashed_password = generate_password_hash(password)
            print("creating account")
            print(username, hashed_password, email, role)            
            cursor = db.cursor()
            sql = "insert into accounts values (%s, %s, %s, %s, %s, %s)"  
            cursor.execute(sql, [None, username, hashed_password, email, role, None])
            data = cursor.fetchall()
            print(data)
            msg = 'You have successfully registered!'
            db.commit()
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("register/admin.html", msg=msg)


@app.route("/register/instructor", methods=["GET", "POST"])
def register_instructor():
    msg = ''
    if request.method == "POST"  and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'id' in request.form and 'fname' in request.form and 'mname' in request.form and 'lname' in request.form and 'salary' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        id = request.form['id']
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        salary = request.form['salary']
        cursor = db.cursor()
        sql = "SELECT * FROM accounts WHERE username = %s;"
        cursor.execute(sql, [username])
        account = cursor.fetchall()
        print(account)
        cursor.close()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            role = "Instructor"
            # Hash the password before storing it
            hashed_password = generate_password_hash(password)
            print("creating account")
            print(username, hashed_password, email, role)            
            cursor = db.cursor()
            sql = "insert into accounts values (%s, %s, %s, %s, %s, %s)"  
            cursor.execute(sql, [None, username, hashed_password, email, role, id])
            sql = "insert into instructor values (%s, %s, %s, %s, %s)"
            cursor.execute(sql, [id, fname, mname, lname, salary])
            data = cursor.fetchall()
            print(data)
            msg = 'You have successfully registered!'
            db.commit()
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("register/instructor.html", msg=msg)


@app.route("/register/student", methods=["GET", "POST"])
def register_student():
    msg = ''
    edited=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data = cursor.fetchall()      
        edited = []

        for i in data:
            edited.append(i[0])

        sql = "SELECT major_name from major;"
        cursor.execute(sql)
        data2 = cursor.fetchall()      
        edited2 = []

        for i in data2:
            edited2.append(i[0])

        return render_template('register/student.html', data = edited,data2=edited2, msg=msg)
    if request.method == "POST"  and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'id' in request.form and 'fname' in request.form and 'mname' in request.form and 'lname' in request.form and 'year' in request.form and 'creds' in request.form and 'dept' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        id = request.form['id']
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        year = request.form['year']
        creds = request.form['creds']
        dept = request.form['dept']
        major = request.form['major']
        cursor = db.cursor()
        sql = "SELECT * FROM accounts WHERE username = %s;"
        cursor.execute(sql, [username])
        account = cursor.fetchall()
        print(account)
        cursor.close()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            role = "Student"
            # Hash the password before storing it
            hashed_password = generate_password_hash(password)
            print("creating account")
            print(username, hashed_password, email, role)            
            cursor = db.cursor()
            sql = "insert into accounts values (%s, %s, %s, %s, %s, %s)"  
            cursor.execute(sql, [None, username, hashed_password, email, role, id])
            sql = "insert into student values (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, [id, fname, mname, lname, year, creds, dept])
            sql = 'select major_id from major where major_name = %s'
            cursor.execute(sql, [major])
            majorID = cursor.fetchone()[0]
            sql = "insert into declared values (%s, %s)"
            cursor.execute(sql, [id, majorID])
            msg = 'You have successfully registered!'
            db.commit()
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = "SELECT dept_name as dept_name from department;"
    cursor.execute(sql)
    data = cursor.fetchall()
    edited = []

    for i in data:
        edited.append(i[0])

    sql = "SELECT major_name from major;"
    cursor.execute(sql)
    data2 = cursor.fetchall()      
    edited2 = []

    for i in data2:
        edited2.append(i[0])
    return render_template("register/student.html", data = edited, data2=edited2, msg=msg)


# Logout route
@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Home route
@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        role = session['role']
        return render_template('actions.html', role=role)
    return redirect(url_for('login'))

# Profile route
@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

##########################################
#  STUDENT STUFF
##########################################

@app.route('/register_classes', methods=['GET', 'POST'])
def register_classes():
    if 'loggedin' not in session or session.get('role') != "Student":
        return redirect(url_for('login'))

    msg = ''
    cursor = db.cursor()

    # -----------------------------
    # POST: Student selects section
    # -----------------------------
    if request.method == 'POST':
        section_id = request.form.get("enrollment_id")  # THIS IS A SECTION ID
        student_id = session['student_id']

        cursor = db.cursor()

        try:
            #create a new enrollment
            cursor.execute("INSERT INTO enrollment (grade) VALUES (NULL)")
            enrollment_id = cursor.lastrowid

            #link it to the section
            cursor.execute(
                "INSERT INTO is_offered (section_id, enrollment_id) VALUES (%s, %s)",
                (section_id, enrollment_id)
            )

            #link it to the student
            cursor.execute(
                "INSERT INTO enrolled (student_id, enrollment_id) VALUES (%s, %s)",
                (student_id, enrollment_id)
            )

            db.commit()
            msg = "Successfully enrolled!"

        except Exception as e:
            db.rollback()
            msg = f"Error enrolling: {e}"

    # -----------------------------
    # GET: Load available courses
    # -----------------------------
    cursor.execute("""
    SELECT DISTINCT c.course_id, c.title
    FROM course c
    JOIN has_sections hs ON hs.course_id = c.course_id
    JOIN section s ON s.section_id = hs.section_id
    JOIN is_offered io ON io.section_id = s.section_id
    ORDER BY c.course_id
    """)

    courses = cursor.fetchall()
    cursor.close()

    return render_template(
        '/actions/student/register_classes.html',
        msg=msg,
        courses=courses
    )

#helper for register_classes
@app.route('/get_sections/<course_id>')
def get_sections(course_id):
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            s.section_id,
            s.sec_code,
            s.semester,
            s.year
        FROM has_sections hs
        JOIN section s ON s.section_id = hs.section_id
        WHERE hs.course_id = %s
        ORDER BY s.year DESC, s.semester ASC, s.sec_code
    """, (course_id,))

    rows = cursor.fetchall()
    cursor.close()

    data = []
    for r in rows:
        data.append([r[0], r[1], r[2], r[3]])

    return jsonify(data)

@app.route('/check_final_grade', methods=['GET', 'POST'])
def check_final_grade():
    if 'loggedin' not in session or session.get('role') != "Student":
        return redirect(url_for('login'))

    student_id = session['student_id']
    name = f"{session['fname']} {session['lname']}"
    selected_semester = request.args.get('semester')

    cursor = db.cursor()

    # Get all years the student has courses in (for the dropdown)
    cursor.execute("""
        SELECT DISTINCT s.semester
        FROM enrolled e
        JOIN enrollment en ON e.enrollment_id = en.enrollment_id
        JOIN is_offered io ON io.enrollment_id = en.enrollment_id
        JOIN section s ON s.section_id = io.section_id
        WHERE e.student_id = %s
        ORDER BY s.semester DESC
    """, (student_id,))
    semesters = [row[0] for row in cursor.fetchall()]

    # Query for student schedule with course title and grade
    query = """
        SELECT 
            c.course_id,
            c.title,
            s.year,
            s.semester,
            en.grade
        FROM enrolled e
        JOIN enrollment en ON e.enrollment_id = en.enrollment_id
        JOIN is_offered io ON io.enrollment_id = en.enrollment_id
        JOIN section s ON s.section_id = io.section_id
        JOIN has_sections hs ON hs.section_id = s.section_id
        JOIN course c ON c.course_id = hs.course_id
        WHERE e.student_id = %s
    """
    params = [student_id]

    if selected_semester:
        query += " AND s.semester = %s"
        params.append(selected_semester)

    query += " ORDER BY s.semester DESC, s.year"

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()

    return render_template(
        '/actions/student/check_final_grade.html',
        data=data,
        semesters=semesters,
        student_id=student_id,
        name=name
    )

@app.route('/check_courses', methods=['GET'])
def check_courses():
    if 'loggedin' not in session or session.get('role') != "Student":
        return redirect(url_for('login'))

    student_id = session['student_id']
    name = f"{session['fname']} {session['lname']}"
    selected_semester = request.args.get('semester')

    cursor = db.cursor()

    # Get all years the student has courses in (for the dropdown)
    cursor.execute("""
        SELECT DISTINCT s.semester
        FROM enrolled e
        JOIN enrollment en ON e.enrollment_id = en.enrollment_id
        JOIN is_offered io ON io.enrollment_id = en.enrollment_id
        JOIN section s ON s.section_id = io.section_id
        WHERE e.student_id = %s
        ORDER BY s.semester DESC
    """, (student_id,))
    semesters = [row[0] for row in cursor.fetchall()]

    # Query for student schedule with course title and grade
    query = """
    SELECT 
        c.course_id,
        c.title,
        s.year,
        s.semester,
        CASE
            WHEN s.year < 2025 THEN
                CASE
                    WHEN en.grade IN ('A','B','C') THEN 'passed'
                    WHEN en.grade IN ('D','F') THEN 'failed'
                    ELSE 'unknown'
                END
            WHEN s.year = 2025 AND s.semester = 'Fall' THEN 'taking'
            ELSE 'registered'
        END AS status
    FROM enrolled e
    JOIN enrollment en ON e.enrollment_id = en.enrollment_id
    JOIN is_offered io ON io.enrollment_id = en.enrollment_id
    JOIN section s ON s.section_id = io.section_id
    JOIN has_sections hs ON hs.section_id = s.section_id
    JOIN course c ON c.course_id = hs.course_id
    WHERE e.student_id = %s
    """
    params = [student_id]

    if selected_semester:
        query += " AND s.semester = %s"
        params.append(selected_semester)

    query += " ORDER BY s.semester DESC, s.year"

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()

    return render_template(
        '/actions/student/check_courses.html',
        data=data,
        semesters=semesters,
        student_id=student_id,
        name=name
    )

@app.route('/section_info', methods=['GET', 'POST'])
def section_info():
    if 'loggedin' not in session or session.get('role') != "Student":
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            c.title,
            s.sec_code,
            s.semester,
            s.year,
            CONCAT(i.first_name, ' ', i.last_name) AS instructor,
            CONCAT(cl.building, ' ', cl.room_number) AS classroom,
            CONCAT(ts.day, ' ', LPAD(ts.start_hr,2,'0'), ':', LPAD(ts.start_min,2,'0'),
                   '-', LPAD(ts.end_hr,2,'0'), ':', LPAD(ts.end_min,2,'0')) AS time_slot
        FROM enrolled e
        JOIN enrollment en ON en.enrollment_id = e.enrollment_id
        JOIN is_offered io ON io.enrollment_id = en.enrollment_id
        JOIN section s ON s.section_id = io.section_id
        JOIN has_sections hs ON hs.section_id = s.section_id
        JOIN course c ON c.course_id = hs.course_id
        LEFT JOIN teaches t ON t.section_id = s.section_id
        LEFT JOIN instructor i ON i.instructor_id = t.instructor_id
        LEFT JOIN held_in hi ON hi.section_id = s.section_id
        LEFT JOIN classroom cl ON cl.room_id = hi.room_id
        LEFT JOIN held_during hd ON hd.section_id = s.section_id
        LEFT JOIN time_slot ts ON ts.time_slot_id = hd.time_slot_id
        WHERE e.student_id = %s
        ORDER BY s.year DESC, s.semester ASC, s.sec_code
    """, (student_id,))
    data = cursor.fetchall()
    cursor.close()

    return render_template('/actions/student/section_info.html', data=data)

@app.route('/advisor_info', methods=['GET', 'POST'])
def advisor_info():
    if 'loggedin' not in session or session.get('role') != "Student":
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            CONCAT(i.first_name, ' ', i.last_name) AS advisor_name,
            d.dept_name
        FROM advisor a
        JOIN instructor i ON i.instructor_id = a.instructor_id
        JOIN employed e ON e.instructor_id = i.instructor_id
        JOIN department d ON d.dept_id = e.dept_id
        WHERE a.student_id = %s
    """, (student_id,))
    advisors = cursor.fetchall()
    cursor.close()

    return render_template('/actions/student/advisor_info.html', advisors=advisors)

@app.route('/modify_info_stud', methods=['POST', 'GET'])
def modify_info_stud():
    msg = ''
    edited=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data = cursor.fetchall()    
        edited = []

        for i in data:
            edited.append(i[0])

        sql = "SELECT major_name from major;"
        cursor.execute(sql)
        data2 = cursor.fetchall()      
        edited2 = []
        cursor.close()

        for i in data2:
            edited2.append(i[0])

        return render_template('actions/student/modify_info.html', data = edited, data2=edited2, msg=msg)
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        student_id = session['student_id']
        account_id = session['id']  # from login session

        cursor = db.cursor()

        try:
            # -----------------------------
            # 1. Update student table
            # -----------------------------
            student_data = {
                'first_name': request.form.get('fname'),
                'middle_name': request.form.get('mname'),
                'last_name': request.form.get('lname'),
                'total_credits': request.form.get('creds'),
                'enrollment_year': request.form.get('year'),
                'dept_name': request.form.get('dept')
            }
            # Filter out empty fields
            update_fields = {k: v for k, v in student_data.items() if v not in (None, '')}

            if update_fields:
                set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
                values = list(update_fields.values())
                values.append(student_id)
                cursor.execute(f"UPDATE student SET {set_clause} WHERE student_id = %s", values)

            # -----------------------------
            # 2. Update declared table
            # -----------------------------
            new_major_name = request.form.get('major')

            if new_major_name:
                # Get the major id from name
                cursor.execute("SELECT major_id FROM major WHERE major_name = %s", [new_major_name])
                result = cursor.fetchone()

                if result:
                    major_id = result[0]

                    # Update declared major
                    cursor.execute("""
                        UPDATE declared
                        SET major_id = %s
                        WHERE student_id = %s
                    """, [major_id, student_id])

                else:
                    return "Error: Major not found", 400

            # -----------------------------
            # 3. Update accounts table
            # -----------------------------
            account_data = {
                'username': request.form.get('username'),
                'password': request.form.get('password'),
                'email': request.form.get('email')
            }

            # Hash password if provided
            if account_data['password']:
                account_data['password'] = generate_password_hash(account_data['password'])

            # Filter out empty fields
            update_fields = {k: v for k, v in account_data.items() if v not in (None, '')}

            if update_fields:
                set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
                values = list(update_fields.values())
                values.append(account_id)
                cursor.execute(f"UPDATE accounts SET {set_clause} WHERE id = %s", values)

            db.commit()
            msg = "Info updated!"

        except Exception as e:
            db.rollback()
            msg = f"Error updating info: {str(e)}"

        finally:
            cursor.close()

    cursor = db.cursor()
    sql = "SELECT dept_name as dept_name from department;"
    cursor.execute(sql)
    data = cursor.fetchall()        
    edited = []

    for i in data:
        edited.append(i[0])

    sql = "SELECT major_name from major;"
    cursor.execute(sql)
    data2 = cursor.fetchall()      
    edited2 = []
    cursor.close()

    for i in data2:
        edited2.append(i[0])
    return render_template("actions/student/modify_info.html", data=edited, data2=edited2, msg=msg)

##########################################
#  INSTRUCTOR STUFF
##########################################

@app.route('/modify_info_inst', methods=['POST', 'GET'])
def modify_info_inst():
    msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        instructor_id = session['instructor_id']
        account_id = session['id']  # from login session

        cursor = db.cursor()

        try:
            # -----------------------------
            # 1. Update instructor table
            # -----------------------------
            instructor_data = {
                'first_name': request.form.get('fname'),
                'middle_name': request.form.get('mname'),
                'last_name': request.form.get('lname'),
                'salary': request.form.get('salary')
            }
            # Filter out empty fields
            update_fields = {k: v for k, v in instructor_data.items() if v not in (None, '')}

            if update_fields:
                set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
                values = list(update_fields.values())
                values.append(instructor_id)
                cursor.execute(f"UPDATE instructor SET {set_clause} WHERE instructor_id = %s", values)

            # -----------------------------
            # 2. Update accounts table
            # -----------------------------
            account_data = {
                'username': request.form.get('username'),
                'password': request.form.get('password'),
                'email': request.form.get('email')
            }

            # Hash password if provided
            if account_data['password']:
                account_data['password'] = generate_password_hash(account_data['password'])

            # Filter out empty fields
            update_fields = {k: v for k, v in account_data.items() if v not in (None, '')}

            if update_fields:
                set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
                values = list(update_fields.values())
                values.append(account_id)
                cursor.execute(f"UPDATE accounts SET {set_clause} WHERE id = %s", values)

            db.commit()
            msg = "Info updated!"

        except Exception as e:
            db.rollback()
            msg = f"Error updating info: {str(e)}"

        finally:
            cursor.close()

    return render_template("actions/instructor/modify_info.html", msg=msg)

@app.route('/submit_grades', methods=['GET', 'POST'])
def submit_grades():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    msg = ''

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        courseid   = request.form.get('courseid')     # optional if they type title instead
        coursename = request.form.get('coursename')   # optional
        section    = request.form.get('section')
        semester   = request.form.get('semester')
        year       = request.form.get('year')
        grade      = request.form.get('grade')
        instructor_id = session.get('instructor_id')

        cursor = db.cursor()

        try:
            # 1) Find the section this instructor teaches that matches course/section/term
            cursor.execute("""
                SELECT s.section_id
                FROM teaches t
                JOIN section s      ON s.section_id = t.section_id
                JOIN has_sections hs ON hs.section_id = s.section_id
                JOIN course c       ON c.course_id = hs.course_id
                WHERE t.instructor_id = %s
                  AND s.sec_code = %s
                  AND s.semester = %s
                  AND s.year = %s
                  AND (
                        (%s IS NOT NULL AND %s <> '' AND c.course_id = %s)
                     OR (%s IS NOT NULL AND %s <> '' AND c.title = %s)
                  )
            """, (
                instructor_id,
                section,
                semester,
                year,
                courseid, courseid, courseid,   # for course_id match
                coursename, coursename, coursename  # for title match
            ))
            sec_row = cursor.fetchone()

            if not sec_row:
                msg = "No matching section found that you teach for that course/term."
                cursor.close()
                return render_template('actions/instructor/submit_grades.html', msg=msg)

            section_id = sec_row[0]

            # 2) Find the enrollment record for this student in that section
            cursor.execute("""
                SELECT en.enrollment_id
                FROM enrolled e
                JOIN enrollment en    ON en.enrollment_id = e.enrollment_id
                JOIN is_offered io    ON io.enrollment_id = en.enrollment_id
                WHERE e.student_id = %s
                  AND io.section_id = %s
            """, (student_id, section_id))
            enr_row = cursor.fetchone()

            if not enr_row:
                msg = "Student is not enrolled in that section."
                cursor.close()
                return render_template('actions/instructor/submit_grades.html', msg=msg)

            enrollment_id = enr_row[0]

            # 3) Update the grade
            cursor.execute("""
                UPDATE enrollment
                SET grade = %s
                WHERE enrollment_id = %s
            """, (grade, enrollment_id))
            db.commit()

            msg = "Grade submitted successfully."

        except Exception as e:
            db.rollback()
            msg = f"Database error: {str(e)}"

        finally:
            cursor.close()

    return render_template('actions/instructor/submit_grades.html', msg=msg)

@app.route('/change_grades', methods=['GET', 'POST'])
def change_grades():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    msg = ''
    old_grade = None

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        courseid   = request.form.get('courseid')     # optional if they type title instead
        coursename = request.form.get('coursename')   # optional
        section    = request.form.get('section')
        semester   = request.form.get('semester')
        year       = request.form.get('year')
        new_grade  = request.form.get('grade')
        instructor_id = session.get('instructor_id')

        cursor = db.cursor()

        try:
            # 1) Find the section this instructor teaches that matches course/section/term
            cursor.execute("""
                SELECT s.section_id
                FROM teaches t
                JOIN section s       ON s.section_id = t.section_id
                JOIN has_sections hs ON hs.section_id = s.section_id
                JOIN course c        ON c.course_id = hs.course_id
                WHERE t.instructor_id = %s
                  AND s.sec_code = %s
                  AND s.semester = %s
                  AND s.year = %s
                  AND (
                        (%s IS NOT NULL AND %s <> '' AND c.course_id = %s)
                     OR (%s IS NOT NULL AND %s <> '' AND c.title = %s)
                  )
            """, (
                instructor_id,
                section,
                semester,
                year,
                courseid, courseid, courseid,
                coursename, coursename, coursename
            ))
            sec_row = cursor.fetchone()

            if not sec_row:
                msg = "No matching section found that you teach for that course/term."
                cursor.close()
                return render_template('actions/instructor/change_grades.html', msg=msg, old_grade=old_grade)

            section_id = sec_row[0]

            # 2) Find the enrollment record for this student in that section (and get current grade)
            cursor.execute("""
                SELECT en.enrollment_id, en.grade
                FROM enrolled e
                JOIN enrollment en ON en.enrollment_id = e.enrollment_id
                JOIN is_offered io ON io.enrollment_id = en.enrollment_id
                WHERE e.student_id = %s
                  AND io.section_id = %s
            """, (student_id, section_id))
            enr_row = cursor.fetchone()

            if not enr_row:
                msg = "Student is not enrolled in that section."
                cursor.close()
                return render_template('actions/instructor/change_grades.html', msg=msg, old_grade=old_grade)

            enrollment_id = enr_row[0]
            old_grade = enr_row[1]  # could be None / NULL

            # 3) Update the grade
            cursor.execute("""
                UPDATE enrollment
                SET grade = %s
                WHERE enrollment_id = %s
            """, (new_grade, enrollment_id))
            db.commit()

            msg = f"Grade updated successfully (was {old_grade if old_grade is not None else 'None'} → {new_grade})."

        except Exception as e:
            db.rollback()
            msg = f"Database error: {str(e)}"

        finally:
            cursor.close()

    return render_template('actions/instructor/change_grades.html', msg=msg, old_grade=old_grade)

@app.route('/add_advisor', methods=['GET', 'POST'])
def add_advisor():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    msg = ''
    instructor_id = session.get('instructor_id')

    if request.method == 'POST':
        student_id = request.form.get('student_id')

        if not student_id:
            msg = "Please enter a student ID."
            return render_template('actions/instructor/add_advisor.html', msg=msg)

        cursor = db.cursor()
        try:
            # 1) Make sure the student exists
            cursor.execute("SELECT 1 FROM student WHERE student_id = %s", (student_id,))
            row = cursor.fetchone()

            if not row:
                msg = "Student not found. Check the student ID."
                cursor.close()
                return render_template('actions/instructor/add_advisor.html', msg=msg)

            # 2) Insert or update advisor record
            cursor.execute("""
                INSERT INTO advisor (student_id, instructor_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE instructor_id = VALUES(instructor_id)
            """, (student_id, instructor_id))

            db.commit()
            msg = f"Student {student_id} is now assigned to you as an advisee."

        except Exception as e:
            db.rollback()
            msg = f"Database error: {str(e)}"

        finally:
            cursor.close()

    return render_template('actions/instructor/add_advisor.html', msg=msg)

@app.route('/remove_advisor', methods=['GET', 'POST'])
def remove_advisor():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    msg = ''
    instructor_id = session.get('instructor_id')

    if request.method == 'POST':
        student_id = request.form.get('student_id')

        if not student_id:
            msg = "Please enter a student ID."
            return render_template('actions/instructor/remove_advisor.html', msg=msg)

        cursor = db.cursor()
        try:
            # 1) Check if this student is actually advised by THIS instructor
            cursor.execute("""
                SELECT 1
                FROM advisor
                WHERE student_id = %s
                  AND instructor_id = %s
            """, (student_id, instructor_id))
            row = cursor.fetchone()

            if not row:
                msg = "That student is not currently assigned to you as an advisee."
                cursor.close()
                return render_template('actions/instructor/remove_advisor.html', msg=msg)

            # 2) Delete the advisor row
            cursor.execute("""
                DELETE FROM advisor
                WHERE student_id = %s
                  AND instructor_id = %s
            """, (student_id, instructor_id))

            db.commit()
            msg = f"Student {student_id} is no longer your advisee."

        except Exception as e:
            db.rollback()
            msg = f"Database error: {str(e)}"

        finally:
            cursor.close()

    return render_template('actions/instructor/remove_advisor.html', msg=msg)

@app.route('/modify_prereqs', methods=['GET', 'POST'])
def modify_prereqs():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    msg = ''

    if request.method == 'POST':
        action    = request.form.get('action')      # "add" or "remove"
        course_id = request.form.get('course_id')
        prereq_id = request.form.get('prereq_id')

        if not course_id or not prereq_id:
            msg = "Please enter both Course ID and Prerequisite Course ID."
            return render_template('actions/instructor/modify_prereqs.html', msg=msg)

        cursor = db.cursor()

        try:
            # 1) Make sure both courses exist
            cursor.execute("SELECT 1 FROM course WHERE course_id = %s", (course_id,))
            c1 = cursor.fetchone()
            cursor.execute("SELECT 1 FROM course WHERE course_id = %s", (prereq_id,))
            c2 = cursor.fetchone()

            if not c1 or not c2:
                msg = "One or both of the course IDs do not exist."
                cursor.close()
                return render_template('actions/instructor/modify_prereqs.html', msg=msg)

            if action == 'add':
                # 2a) Add prereq (course_id requires prereq_id)
                try:
                    cursor.execute("""
                        INSERT INTO prereq (course_id, prereq_id)
                        VALUES (%s, %s)
                    """, (course_id, prereq_id))
                    db.commit()
                    msg = f"Prerequisite {prereq_id} added for course {course_id}."
                except Exception as e:
                    db.rollback()
                    msg = f"Error adding prerequisite (it may already exist): {str(e)}"

            elif action == 'remove':
                # 2b) Remove prereq
                cursor.execute("""
                    DELETE FROM prereq
                    WHERE course_id = %s AND prereq_id = %s
                """, (course_id, prereq_id))

                if cursor.rowcount == 0:
                    msg = "No such prerequisite relationship found to remove."
                    db.rollback()  # nothing changed anyway
                else:
                    db.commit()
                    msg = f"Prerequisite {prereq_id} removed from course {course_id}."

            else:
                msg = "Invalid action."

        except Exception as e:
            db.rollback()
            msg = f"Database error: {str(e)}"

        finally:
            cursor.close()

    # GET or after POST → show page with msg
    return render_template('actions/instructor/modify_prereqs.html', msg=msg)

@app.route('/remove_from_section', methods=['GET', 'POST'])
def remove_from_section():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    msg = ''
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        courseid   = request.form.get('courseid')     # optional
        coursename = request.form.get('coursename')   # optional
        section    = request.form.get('section')
        semester   = request.form.get('semester')
        year       = request.form.get('year')
        instructor_id = session.get('instructor_id')

        cursor = db.cursor()

        try:
            # 1) Find the section this instructor teaches that matches course/section/term
            cursor.execute("""
                SELECT s.section_id
                FROM teaches t
                JOIN section s        ON s.section_id = t.section_id
                JOIN has_sections hs  ON hs.section_id = s.section_id
                JOIN course c         ON c.course_id = hs.course_id
                WHERE t.instructor_id = %s
                  AND s.sec_code = %s
                  AND s.semester = %s
                  AND s.year = %s
                  AND (
                        (%s IS NOT NULL AND %s <> '' AND c.course_id = %s)
                     OR (%s IS NOT NULL AND %s <> '' AND c.title = %s)
                  )
            """, (
                instructor_id,
                section,
                semester,
                year,
                courseid, courseid, courseid,
                coursename, coursename, coursename
            ))
            sec_row = cursor.fetchone()

            if not sec_row:
                msg = "No matching section found that you teach for that course/term."
                cursor.close()
                return render_template('actions/instructor/remove_from_section.html', msg=msg)

            section_id = sec_row[0]

            # 2) Find the enrollment for this student in that section
            cursor.execute("""
                SELECT en.enrollment_id
                FROM enrolled e
                JOIN enrollment en ON en.enrollment_id = e.enrollment_id
                JOIN is_offered io ON io.enrollment_id = en.enrollment_id
                WHERE e.student_id = %s
                  AND io.section_id = %s
            """, (student_id, section_id))
            enr_row = cursor.fetchone()

            if not enr_row:
                msg = "Student is not enrolled in that section."
                cursor.close()
                return render_template('actions/instructor/remove_from_section.html', msg=msg)

            enrollment_id = enr_row[0]

            # 3) Delete relationships in correct FK order:
            #    enrolled -> is_offered -> enrollment
            cursor.execute("""
                DELETE FROM enrolled
                WHERE enrollment_id = %s
            """, (enrollment_id,))

            cursor.execute("""
                DELETE FROM is_offered
                WHERE enrollment_id = %s
            """, (enrollment_id,))

            cursor.execute("""
                DELETE FROM enrollment
                WHERE enrollment_id = %s
            """, (enrollment_id,))

            db.commit()
            msg = f"Student {student_id} was removed from that section."

        except Exception as e:
            db.rollback()
            msg = f"Database error: {str(e)}"

        finally:
            cursor.close()

    return render_template('actions/instructor/remove_from_section.html', msg=msg)

@app.route('/section_roster', methods=['GET', 'POST'])
def section_roster():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    instructor_id = session.get('instructor_id')
    msg = ''
    roster = []
    selected_section_id = None

    cursor = db.cursor()

    # 1) Get all sections this instructor teaches (for the dropdown)
    cursor.execute("""
        SELECT 
            s.section_id,
            s.sec_code,
            s.semester,
            s.year,
            c.course_id,
            c.title
        FROM teaches t
        JOIN section s       ON s.section_id = t.section_id
        JOIN has_sections hs ON hs.section_id = s.section_id
        JOIN course c        ON c.course_id = hs.course_id
        WHERE t.instructor_id = %s
        ORDER BY s.year DESC, s.semester, c.course_id, s.sec_code
    """, (instructor_id,))
    sections = cursor.fetchall()

    if request.method == 'POST':
        selected_section_id = request.form.get('section_id')

        if not selected_section_id:
            msg = "Please select a section."
        else:
            # 2) Get roster for that section
            cursor.execute("""
                SELECT 
                    st.student_id,
                    st.first_name,
                    st.middle_name,
                    st.last_name,
                    en.grade
                FROM enrolled e
                JOIN student st     ON st.student_id = e.student_id
                JOIN enrollment en  ON en.enrollment_id = e.enrollment_id
                JOIN is_offered io  ON io.enrollment_id = en.enrollment_id
                WHERE io.section_id = %s
                ORDER BY st.last_name, st.first_name
            """, (selected_section_id,))
            roster = cursor.fetchall()
            if not roster:
                msg = "No students enrolled in this section."

    cursor.close()

    return render_template(
        'actions/instructor/section_roster.html',
        msg=msg,
        sections=sections,
        roster=roster,
        selected_section_id=selected_section_id
    )

@app.route('/teaching_sections', methods=['GET'])
def teaching_sections():
    # Must be logged in + instructor
    if 'loggedin' not in session or session.get('role') != "Instructor":
        return redirect(url_for('login'))

    instructor_id = session.get('instructor_id')
    sections = []
    msg = ''

    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT
                s.section_id,
                s.sec_code,
                s.semester,
                s.year,
                c.course_id,
                c.title,
                cl.building,
                cl.room_number,
                ts.day,
                ts.start_hr,
                ts.start_min,
                ts.end_hr,
                ts.end_min
            FROM teaches t
            JOIN section s        ON s.section_id = t.section_id
            JOIN has_sections hs  ON hs.section_id = s.section_id
            JOIN course c         ON c.course_id = hs.course_id
            LEFT JOIN held_in hi       ON hi.section_id = s.section_id
            LEFT JOIN classroom cl     ON cl.room_id = hi.room_id
            LEFT JOIN held_during hd   ON hd.section_id = s.section_id
            LEFT JOIN time_slot ts     ON ts.time_slot_id = hd.time_slot_id
            WHERE t.instructor_id = %s
            ORDER BY s.year DESC, s.semester, c.course_id, s.sec_code
        """, (instructor_id,))
        sections = cursor.fetchall()

        if not sections:
            msg = "You are not currently assigned to teach any sections."

    except Exception as e:
        msg = f"Database error: {str(e)}"

    finally:
        cursor.close()

    return render_template(
        'actions/instructor/teaching_sections.html',
        sections=sections,
        msg=msg
    )

##########################################
#  ADMIN STUFF
##########################################

@app.route('/crud_course', methods=['POST', 'GET'])
def crud_course():
    edited=''
    msg=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT course_id, title, credits from course;"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        return render_template('actions/admin/crud_course.html', data = data, msg=msg)
    if request.method == "POST"  and 'Cid' in request.form: #we creating out here
        id = request.form['Cid']
        title = request.form['Ctitle']
        credits = request.form['Ccredits']
        prereq = request.form['Cprereq']
        dept = request.form['Cdept']
        cursor = db.cursor()
        sql = "SELECT * FROM course WHERE title = %s;"
        cursor.execute(sql, [title])
        course = cursor.fetchall()
        print(course)
        cursor.close()
        if course:
            msg = 'Course already exists!'
        else:
            print("creating course")
            print(id, title, credits)            
            cursor = db.cursor()
            sql = "insert into course values (%s, %s, %s)"
            cursor.execute(sql, [id, title, credits])
            sql = 'insert into prereq values (%s, %s)'
            cursor.execute(sql, [id, prereq])
            sql = 'insert into has_course values (%s, %s)'
            cursor.execute(sql, [dept, id])
            data = cursor.fetchall()
            print(data)
            msg = 'Course Created!'
            db.commit()
            cursor.close()
    elif request.method == "POST" and 'update' in request.form:
        course_id = request.form.get('course')
        prereq = request.form.get('prereq')
        dept = request.form.get('dept')

        cursor = db.cursor()

        try:
            course_data = {
                'title': request.form.get('title'),
                'credits': request.form.get('credits')
            }
            # Filter out empty fields
            update_fields = {k: v for k, v in course_data.items() if v not in (None, '')}

            if update_fields:
                set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
                values = list(update_fields.values())
                values.append(course_id)
                cursor.execute(f"UPDATE course SET {set_clause} WHERE course_id = %s", values)

            if prereq:  # If user provided a prerequisite course
                # Delete old prereqs first (simplest way to replace)
                cursor.execute("DELETE FROM prereq WHERE course_id = %s", (course_id,))
                # Then insert the new one
                cursor.execute("INSERT INTO prereq (course_id, prereq_id) VALUES (%s, %s)", (course_id, prereq))

            if dept:
                # Delete old department links
                cursor.execute("DELETE FROM has_course WHERE course_id = %s", (course_id,))
                # Insert the new department
                cursor.execute("INSERT INTO has_course (dept_id, course_id) VALUES (%s, %s)", (dept, course_id))

            db.commit()
            msg = "Info updated!"

        except Exception as e:
            db.rollback()
            msg = f"Error updating info: {str(e)}"

        finally:
            cursor.close()
    elif request.method == "POST" and 'delete' in request.form:
        course_id = request.form.get('course')
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM prereq WHERE course_id = %s", (course_id,))

            cursor.execute("DELETE FROM has_course WHERE course_id = %s", (course_id,))

            cursor.execute("DELETE FROM has_sections WHERE course_id = %s", (course_id,))

            cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))

            db.commit()
            msg = "Course deleted successfully!"

        except Exception as e:
            db.rollback()
            msg = f"Error deleting course: {e}"
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = "SELECT course_id, title, credits from course;"
    cursor.execute(sql)
    data = cursor.fetchall()     
    cursor.close()
    return render_template("actions/admin/crud_course.html",data=data, msg=msg)

@app.route('/crud_section', methods=['POST', 'GET'])
def crud_section():
    edited=''
    msg=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = """
        SELECT 
            s.section_id,
            s.sec_code, 
            s.semester, 
            s.year, 
            h.course_id, 
            c.title
        FROM section s
        JOIN has_sections h ON s.section_id = h.section_id
        JOIN course c ON h.course_id = c.course_id
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        return render_template('actions/admin/crud_section.html', data = data, msg=msg)
    if request.method == "POST"  and 'Cid' in request.form: #we creating out here
        id = request.form['Cid']
        code = request.form['Ccode']
        semester = request.form['Csem']
        year = request.form['Cyear']
        course = request.form['CcourseID']
        room = request.form['Croom']
        cursor = db.cursor()
        sql ="""
        SELECT s.section_id
        FROM section s
        JOIN has_sections h ON s.section_id = h.section_id
        WHERE s.sec_code = %s
        AND s.semester = %s
        AND s.year = %s
        AND h.course_id = %s
        """
        cursor.execute(sql, [code, semester, year, course])
        result = cursor.fetchall()
        print(result)
        cursor.close()
        if result:
            msg = 'Section already exists!'
        else:
            print("creating section")
            print(id, code, semester, year)            
            cursor = db.cursor()
            sql = "insert into section values (%s, %s, %s, %s)"
            cursor.execute(sql, [id, code, semester, year])
            data = cursor.fetchall()
            print(data)
            sql = "insert into has_sections values (%s, %s)"
            cursor.execute(sql, [id, course])
            sql = "insert into held_in values (%s, %s)"
            cursor.execute(sql, [id, room])
            msg = 'Section Created!'
            db.commit()
            cursor.close()
    elif request.method == "POST" and 'update' in request.form:
        section_id = request.form.get('section')
        course = request.form.get('course')
        room = request.form.get('room')

        cursor = db.cursor()

        try:
            section_data = {
                'sec_code': request.form.get('code'),
                'semester': request.form.get('sem'),
                'year': request.form.get('year')
            }
            # Filter out empty fields
            update_fields = {k: v for k, v in section_data.items() if v not in (None, '')}

            if update_fields:
                set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
                values = list(update_fields.values())
                values.append(section_id)
                cursor.execute(f"UPDATE section SET {set_clause} WHERE section_id = %s", values)

            if course:  # If user provided a prerequisite course
                # Delete old prereqs first (simplest way to replace)
                cursor.execute("DELETE FROM has_sections WHERE section_id = %s", (section_id,))
                # Then insert the new one
                cursor.execute("INSERT INTO has_sections (section_id, course_id) VALUES (%s, %s)", (section_id, course))

            if room:
                # Delete old department links
                cursor.execute("DELETE FROM held_in WHERE section_id = %s", (section_id,))
                # Insert the new department
                cursor.execute("INSERT INTO held_in (section_id, room_id) VALUES (%s, %s)", (section_id, room))

            db.commit()
            msg = "Info updated!"

        except Exception as e:
            db.rollback()
            msg = f"Error updating info: {str(e)}"

        finally:
            cursor.close()
    elif request.method == "POST" and 'delete' in request.form:
        section_id = request.form.get('section')
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM held_in WHERE section_id = %s", (section_id,))

            cursor.execute("DELETE FROM held_during WHERE section_id = %s", (section_id,))

            cursor.execute("DELETE FROM has_sections WHERE section_id = %s", (section_id,))

            cursor.execute("DELETE FROM is_offered WHERE section_id = %s", (section_id,))
            
            cursor.execute("DELETE FROM teaches WHERE section_id = %s", (section_id,))
            
            cursor.execute("DELETE FROM section WHERE section_id = %s", (section_id,))

            db.commit()
            msg = "Section deleted successfully!"

        except Exception as e:
            db.rollback()
            msg = f"Error deleting section: {e}"
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = """
    SELECT 
            s.section_id,
            s.sec_code, 
            s.semester, 
            s.year, 
            h.course_id, 
            c.title
        FROM section s
        JOIN has_sections h ON s.section_id = h.section_id
        JOIN course c ON h.course_id = c.course_id
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    return render_template("actions/admin/crud_section.html",data=data, msg=msg)

@app.route('/crud_classroom', methods=['POST', 'GET'])
def crud_classroom():
    edited=''
    msg=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT building, room_number FROM classroom;"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        edited = []

        for building, room in data:
            edited.append(f"{building}-{room}")

        return render_template('actions/admin/crud_classroom.html', data = edited, msg=msg)
    if request.method == "POST"  and 'Cid' in request.form: #we creating out here
        id = request.form['Cid']
        building = request.form['Cbuilding']
        number = request.form['Cnumber']
        cap = request.form['Ccap']
        cursor = db.cursor()
        sql = "SELECT * FROM classroom WHERE building = %s AND room_number = %s"
        cursor.execute(sql, (building, number))
        room = cursor.fetchall()
        print(room)
        cursor.close()
        if room:
            msg = 'Classroom already exists!'
        else:
            print("creating Classroom")
            print(id, building, number, cap)            
            cursor = db.cursor()
            sql = "insert into classroom values (%s, %s, %s, %s)"
            cursor.execute(sql, [id, building, number, cap])
            data = cursor.fetchall()
            print(data)
            msg = 'Classroom Created!'
            db.commit()
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = "SELECT building, room_number FROM classroom;"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    edited = []

    for building, room in data:
        edited.append(f"{building}-{room}")
    return render_template("actions/admin/crud_classroom.html",data=edited, msg=msg)

@app.route('/crud_department', methods=['POST', 'GET'])
def crud_department():
    edited=''
    msg=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data = cursor.fetchall()        
        cursor.close()
        edited = []

        for i in data:
            edited.append(i[0])

        return render_template('actions/admin/crud_department.html', data = edited, msg=msg)
    if request.method == "POST"  and 'Cid' in request.form: #we creating out here
        id = request.form['Cid']
        name = request.form['Cname']
        building = request.form['Cbuilding']
        budget = request.form['Cbudget']
        cursor = db.cursor()
        sql = "SELECT * FROM department WHERE dept_name = %s;"
        cursor.execute(sql, [name])
        dept = cursor.fetchall()
        print(dept)
        cursor.close()
        if dept:
            msg = 'Department already exists!'
        else:
            # Hash the password before storing it
            print("creating department")
            print(id, name, building, budget)            
            cursor = db.cursor()
            sql = "insert into department values (%s, %s, %s, %s)"
            cursor.execute(sql, [id, name, building, budget])
            data = cursor.fetchall()
            print(data)
            msg = 'Department Created!'
            db.commit()
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = "SELECT dept_name as dept_name from department;"
    cursor.execute(sql)
    data = cursor.fetchall()        
    cursor.close()
    edited = []

    for i in data:
        edited.append(i[0])
    return render_template("actions/admin/crud_department.html",data=edited, msg=msg)

@app.route('/crud_timeslot', methods=['POST', 'GET'])
def crud_timeslot():
    edited=''
    msg=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT day, start_hr, start_min, end_hr, end_min from time_slot;"
        cursor.execute(sql)
        data = cursor.fetchall()        
        cursor.close()
        edited = []

        for day, start_hr, start_min, end_hr, end_min in data:
            edited.append(f"{day}, {start_hr}:{start_min}-{end_hr}:{end_min}")

        return render_template('actions/admin/crud_timeslot.html', data = edited, msg=msg)
    if request.method == "POST"  and 'Cid' in request.form: #we creating out here
        id = request.form['Cid']
        day = request.form['Cday']
        start_hr = request.form['Csh']
        start_min = request.form['Csm']
        end_hr = request.form['Ceh']
        end_min = request.form['Cem']
        sectionID = request.form['CsectionID']
        cursor = db.cursor()
        sql = """
        SELECT * FROM time_slot WHERE day = %s
        AND start_hr = %s
        AND start_min = %s
        AND end_hr = %s
        AND end_min = %s;
        """
        cursor.execute(sql, [day, start_hr, start_min, end_hr, end_min])
        result = cursor.fetchall()
        print(result)
        cursor.close()
        if result:
            msg = 'Time slot already exists!'
        else:
            # Hash the password before storing it
            print("creating time slot")
            print(id, day, start_hr, start_min, end_hr, end_min)            
            cursor = db.cursor()
            sql = "insert into time_slot values (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, [id, day, start_hr, start_min, end_hr, end_min])
            sql = "insert into held_during values (%s, %s)"
            cursor.execute(sql, [sectionID, id])
            data = cursor.fetchall()
            print(data)
            msg = 'Time Slot Created!'
            db.commit()
            cursor.close()
    
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = "SELECT day, start_hr, start_min, end_hr, end_min from time_slot;"
    cursor.execute(sql)
    data = cursor.fetchall()        
    cursor.close()
    edited = []

    for i in data:
        edited.append(f"{day}, {start_hr}:{start_min}-{end_hr}:{end_min}")
    return render_template("actions/admin/crud_timeslot.html",data=edited, msg=msg)

@app.route('/crud_instructor', methods=['POST', 'GET'])
def crud_instructor():
    edited=''
    msg=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT first_name, middle_name, last_name from instructor;"
        cursor.execute(sql)
        data = cursor.fetchall()        
        cursor.close()
        edited = []

        for fname, mname, lname in data:
            edited.append(f"{lname}, {fname} {mname}")

        return render_template('actions/admin/crud_instructor.html', data = edited, msg=msg)
    if request.method == "POST"  and 'Cid' in request.form: #we creating out here
        id = request.form['Cid']
        fname = request.form['Cfname']
        mname = request.form['Cmname']
        lname = request.form['Clname']
        salary = request.form['Csalary']
        dept = request.form['Cdept']
        section = request.form['Csection']
        student = request.form['Cstudent']
        cursor = db.cursor()
        sql = """
        SELECT * FROM instructor WHERE first_name = %s
        AND middle_name = %s
        AND last_name = %s;
        """
        cursor.execute(sql, [fname, mname, lname])
        result = cursor.fetchall()
        print(result)
        cursor.close()
        if result:
            msg = 'Instructor already exists!'
        else:
            # Hash the password before storing it
            print("creating instructor")
            print(id, fname, mname, lname, salary)            
            cursor = db.cursor()
            sql = "insert into instructor values (%s, %s, %s, %s, %s)"
            cursor.execute(sql, [id, fname, mname, lname, salary])
            sql = "insert into employed values (%s, %s)"
            cursor.execute(sql, [id, dept])
            sql = "insert into teaches values (%s, %s)"
            cursor.execute(sql, [id, section])
            sql = "insert into advisor values (%s, %s)"
            cursor.execute(sql, [student, id])
            data = cursor.fetchall()
            print(data)
            msg = 'Instructor Created!'
            db.commit()
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = "SELECT first_name, middle_name, last_name from instructor;"
    cursor.execute(sql)
    data = cursor.fetchall()        
    cursor.close()
    edited = []

    for fname, mname, lname in data:
            edited.append(f"{lname}, {fname} {mname}")
    return render_template("actions/admin/crud_instructor.html",data=edited, msg=msg)

@app.route('/crud_student', methods=['POST', 'GET'])
def crud_student():
    msg=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT student_id, first_name, middle_name, last_name from student;"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        sql = """
        SELECT 
            s.student_id, 
            s.first_name, 
            s.middle_name, 
            s.last_name, 
            s.enrollment_year, 
            s.total_credits, 
            m.major_name, 
            d.dept_name
        FROM student s
        LEFT JOIN declared dc ON dc.student_id = s.student_id
        LEFT JOIN major m ON m.major_id = dc.major_id
        LEFT JOIN under u ON u.major_id = m.major_id
        LEFT JOIN department d ON d.dept_id = u.dept_id
        """
        cursor.execute(sql)
        data2 = cursor.fetchall()  
        edited2 = []

        for row in data2:
            sid, fname, mname, lname, enyear, tcreds, major, dept = row
            full_name = f"{lname}, {fname} {mname}"
            edited2.append([sid, full_name, enyear, tcreds, major or "N/A", dept or "N/A"])

        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data3 = cursor.fetchall()        
        edited3 = []

        for i in data3:
            edited3.append(i[0])

        sql = "SELECT major_name from major;"
        cursor.execute(sql)
        data4 = cursor.fetchall()      
        edited4 = []
        cursor.close()

        for i in data4:
            edited4.append(i[0])

        return render_template('actions/admin/crud_student.html', data = data, data2=edited2, data3=edited3, data4=edited4, msg=msg)
    if request.method == "POST"  and 'Cid' in request.form: #we creating out here
        id = request.form['Cid']
        fname = request.form['Cfname']
        mname = request.form['Cmname']
        lname = request.form['Clname']
        year = request.form['Cyear']
        creds = request.form['Ccreds']
        major = request.form['Cmajor']
        dept = request.form['Cdept']
        cursor = db.cursor()
        sql = """
        SELECT * FROM student WHERE first_name = %s
        AND middle_name = %s
        AND last_name = %s;
        """
        cursor.execute(sql, [fname, mname, lname])
        result = cursor.fetchall()
        print(result)
        cursor.close()
        if result:
            msg = 'Student already exists!'
        else:
            # Hash the password before storing it
            print("creating student")
            print(id, fname, mname, lname, year, creds, dept)            
            cursor = db.cursor()
            sql = "insert into student values (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, [id, fname, mname, lname, year, creds, dept])
            sql = "insert into declared values (%s, %s)"
            cursor.execute(sql, [id, major])
            data = cursor.fetchall()
            print(data)
            msg = 'Student Created!'
            db.commit()
            cursor.close()
    elif request.method == 'POST' and 'update' in request.form:
        student_id = request.form.get('student')

        cursor = db.cursor()

        try:
            # -----------------------------
            # 1. Update student table
            # -----------------------------
            student_data = {
                'first_name': request.form.get('fname'),
                'middle_name': request.form.get('mname'),
                'last_name': request.form.get('lname'),
                'total_credits': request.form.get('creds'),
                'enrollment_year': request.form.get('year'),
                'dept_name': request.form.get('dept')
            }
            # Filter out empty fields
            update_fields = {k: v for k, v in student_data.items() if v not in (None, '')}

            if update_fields:
                set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
                values = list(update_fields.values())
                values.append(student_id)
                cursor.execute(f"UPDATE student SET {set_clause} WHERE student_id = %s", values)

            # -----------------------------
            # 2. Update declared table
            # -----------------------------
            new_major_name = request.form.get('major')

            if new_major_name:
                # Get the major id from name
                cursor.execute("SELECT major_id FROM major WHERE major_name = %s", [new_major_name])
                result = cursor.fetchone()

                if result:
                    major_id = result[0]

                    # Update declared major
                    cursor.execute("""
                        UPDATE declared
                        SET major_id = %s
                        WHERE student_id = %s
                    """, [major_id, student_id])

                else:
                    return "Error: Major not found", 400

            db.commit()
            msg = "Info updated!"

        except Exception as e:
            db.rollback()
            msg = f"Error updating info: {str(e)}"

        finally:
            cursor.close()
    elif request.method == "POST" and 'delete' in request.form:
        student_id = request.form.get('student')
        cursor = db.cursor()
        try:
            #delete from declared table
            cursor.execute("DELETE FROM declared WHERE student_id = %s", (student_id,))

            #delete from advisor table
            cursor.execute("DELETE FROM advisor WHERE student_id = %s", (student_id,))

            #delete from enrolled table
            cursor.execute("DELETE FROM enrolled WHERE student_id = %s", (student_id,))

            #delete from student table
            cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))

            db.commit()
            msg = "Student deleted successfully!"

        except Exception as e:
            db.rollback()
            msg = f"Error deleting student: {e}"

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    cursor = db.cursor()
    sql = "SELECT student_id, first_name, middle_name, last_name from student;"
    cursor.execute(sql)
    data = cursor.fetchall()

    sql = """
        SELECT 
            s.student_id, 
            s.first_name, 
            s.middle_name, 
            s.last_name, 
            s.enrollment_year, 
            s.total_credits, 
            m.major_name, 
            d.dept_name
        FROM student s
        LEFT JOIN declared dc ON dc.student_id = s.student_id
        LEFT JOIN major m ON m.major_id = dc.major_id
        LEFT JOIN under u ON u.major_id = m.major_id
        LEFT JOIN department d ON d.dept_id = u.dept_id
    """
    cursor.execute(sql)
    data2 = cursor.fetchall()  
    edited2 = []

    for row in data2:
        sid, fname, mname, lname, enyear, tcreds, major, dept = row
        full_name = f"{lname}, {fname} {mname}"
        edited2.append([sid, full_name, enyear, tcreds, major or "N/A", dept or "N/A"])

    sql = "SELECT dept_name as dept_name from department;"
    cursor.execute(sql)
    data3 = cursor.fetchall()        
    edited3 = []

    for i in data3:
        edited3.append(i[0])

    sql = "SELECT major_name from major;"
    cursor.execute(sql)
    data4 = cursor.fetchall()      
    edited4 = []
    cursor.close()

    for i in data4:
        edited4.append(i[0])
    return render_template("actions/admin/crud_student.html",data=data, data2=edited2, data3=edited3, data4=edited4, msg=msg)

@app.route('/assign_teacher', methods=['POST', 'GET'])

######################################################

# Search form route
@app.route('/searchform')
def searchform():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('form.html', username=session['username'])

# Search route
@app.route('/search', methods=['POST', 'GET'])
def search():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return "Fill out the Search Form"
     
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        data = []
        if(id != '' or name != ''):
            cursor = db.cursor()        
            if name:
                cursor.execute("SELECT * from instructor where name = %s", [name])
            if id:
                cursor.execute("SELECT * from instructor where ID = %s", [id])
                    
            data = cursor.fetchall()        
            cursor.close()
            print("Found: ", data)
        return render_template('results.html', data=data)

# Run the application
app.run(host='localhost', port=4500)
