#! /usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session
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
            sql = "insert into accounts values (%s, %s, %s, %s, %s)"  
            cursor.execute(sql, [None, username, hashed_password, email, role])
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
        cursor.close()
        edited = []

        for i in data:
            edited.append(i[0])

        return render_template('register/student.html', data = edited, msg=msg)
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
            data = cursor.fetchall()
            print(data)
            msg = 'You have successfully registered!'
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
    return render_template("register/student.html", data = edited, msg=msg)


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

@app.route('/modify_info_stud', methods=['POST', 'GET'])
def modify_info_stud():
    msg = ''
    edited=''
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data = cursor.fetchall()        
        cursor.close()
        edited = []

        for i in data:
            edited.append(i[0])

        return render_template('actions/student/modify_info.html', data = edited, msg=msg)
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

    cursor = db.cursor()
    sql = "SELECT dept_name as dept_name from department;"
    cursor.execute(sql)
    data = cursor.fetchall()        
    cursor.close()
    edited = []

    for i in data:
        edited.append(i[0])
    return render_template("actions/student/modify_info.html", data=edited, msg=msg)

@app.route('/register_classes', methods=['GET', 'POST'])
def register_classes():
    if 'loggedin' not in session or session.get('role') != "Student":
        return redirect(url_for('login'))

    msg = ''

    if request.method == 'POST':
        coursename   = request.form['coursename']
        courseid     = request.form['courseid']
        section_code = request.form['section']
        semester     = request.form['semester']
        year         = request.form['year']
        student_id   = session['student_id']

        cursor = db.cursor()

        try:
            # -----------------------------------------
            # STEP 1: Insert enrollment only if valid
            # -----------------------------------------
            cursor.execute("""
                INSERT INTO enrollment (grade)
                SELECT NULL
                WHERE EXISTS (
                    SELECT 1
                    FROM course c
                    JOIN has_sections hs ON hs.course_id = c.course_id
                    JOIN section s ON s.section_id = hs.section_id
                    WHERE (c.course_id = %s OR c.title = %s)
                      AND s.sec_code = %s
                      AND s.semester = %s
                      AND s.year = %s
                );
            """, (courseid, coursename, section_code, semester, year))

            if cursor.rowcount == 0:
                msg = "Invalid course/section or not offered in that term."
                return render_template('/actions/student/register_classes.html', msg=msg)

            enrollment_id = cursor.lastrowid

            # -----------------------------------------
            # STEP 2: Link enrollment → section
            # -----------------------------------------
            cursor.execute("""
                INSERT INTO is_offered (section_id, enrollment_id)
                SELECT s.section_id, %s
                FROM course c
                JOIN has_sections hs ON hs.course_id = c.course_id
                JOIN section s ON s.section_id = hs.section_id
                WHERE (c.course_id = %s OR c.title = %s)
                  AND s.sec_code = %s
                  AND s.semester = %s
                  AND s.year = %s
            """, (enrollment_id, courseid, coursename, section_code, semester, year))

            if cursor.rowcount == 0:
                msg = "Unexpected error: no section matched."
                db.rollback()
                return render_template('/actions/student/register_classes.html', msg=msg)

            # -----------------------------------------
            # STEP 3: Link enrollment → student
            # -----------------------------------------
            cursor.execute("""
                INSERT INTO enrolled (student_id, enrollment_id)
                VALUES (%s, %s)
            """, (student_id, enrollment_id))

            db.commit()
            msg = "Successfully enrolled!"

        except Exception as e:
            db.rollback()
            msg = f"Database error: {str(e)}"

        finally:
            cursor.close()

        return render_template('/actions/student/register_classes.html', msg=msg)

    # GET request → show form
    return render_template('/actions/student/register_classes.html', msg=msg)

@app.route('/check_courses', methods=['GET'])
def check_courses():
    if 'loggedin' not in session or session.get('role') != "Student":
        return redirect(url_for('login'))

    student_id = session['student_id']
    name = f"{session['fname']} {session['lname']}"
    selected_year = request.args.get('year')

    cursor = db.cursor()

    # Get all years the student has courses in (for the dropdown)
    cursor.execute("""
        SELECT DISTINCT s.year
        FROM enrolled e
        JOIN enrollment en ON e.enrollment_id = en.enrollment_id
        JOIN is_offered io ON io.enrollment_id = en.enrollment_id
        JOIN section s ON s.section_id = io.section_id
        WHERE e.student_id = %s
        ORDER BY s.year DESC
    """, (student_id,))
    years = [row[0] for row in cursor.fetchall()]

    # Query for student schedule with course title and grade
    query = """
        SELECT 
            c.course_id,
            c.title,
            s.semester,
            s.year,
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

    if selected_year:
        query += " AND s.year = %s"
        params.append(selected_year)

    query += " ORDER BY s.year DESC, s.semester"

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()

    return render_template(
        '/actions/student/check_courses.html',
        data=data,
        years=years,
        student_id=student_id,
        name=name
    )

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
