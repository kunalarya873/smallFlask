from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search_student.html')
    else:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        student_name = request.form.get('studentname')
        c.execute(f"SELECT * FROM info WHERE name LIKE '%{student_name}%'")
        results = c.fetchall()
        column_names = ['Name', 'StudentId', 'Address', 'Gender', 'Date of birth']
        conn.close()
        return render_template('search_results.html', headings=column_names, mylist=results)


@app.route('/add_student', methods=['GET', 'POST'])
def add_students():
    if request.method == 'GET':
        return render_template('add_student.html')
    else:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()

        studentname = request.form.get('studentname') 
        sid = request.form.get('id') 
        address = request.form.get('address') 
        gender = request.form.get('gender') 
        dob = request.form.get('dob')

        if not studentname or not sid:
            return "Name and StudentID are required"
        else:
            sid = int(sid)

        # Fix the SQL query and use parameterized query
        sql_query = "INSERT INTO info VALUES (?, ?, ?, ?, ?)"
        c.execute(sql_query, (studentname, sid, address, gender, dob))
        conn.commit()

        scores = {
            'CHEM101': request.form.get('chem101'),
            'MATH101': request.form.get('math101'),
            'PHYS101': request.form.get('phys101')
        }

        for code, score in scores.items():
            if score is not None:
                sql_query = "INSERT INTO scores VALUES (?, ?, ?)"
                c.execute(sql_query, (sid, code, float(score)))
                conn.commit()

        conn.close()
        return f"the student {studentname} was created ....OK"


def extract_data(request):
    data_dict = {}
    scores_dict = {}
    data_dict['name'] = request.form.get('studentname')
    data_dict['studentid'] = request.form.get('id')
    data_dict['address'] = request.form.get('address')
    data_dict['gender'] = request.form.get('gender')
    data_dict['dob'] = request.form.get('dob')
    scores_dict['CHEM101'] = float(request.form.get('chem101')) if request.form.get('chem101') else None
    scores_dict['PHYS101'] = float(request.form.get('chem101')) if request.form.get('phys101') else None
    scores_dict['MATH101'] = float(request.form.get('chem101'))if request.form.get('math101') else None
    return data_dict, scores_dict


@app.route('/edit_student/<int:sid>', methods=['GET', 'POST'])
def edit_student(sid):
    if request.method == 'GET':
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM info WHERE studentid={sid}")
        info_results = c.fetchall()[0]
        c.execute(f"SELECT * FROM scores WHERE studentid={sid}")
        scores_results = c.fetchall()
        scores_dict = {'CHEM101': '', 'MATH101': '', 'PHYS101': ''}
        for each_score in scores_results:
            scores_dict[each_score[1]] = each_score[2]
        conn.close()  # Close the connection after fetching data
        return render_template('edit_student.html', info_results=info_results, scores_dict=scores_dict)
    else:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        student_dict, student_scores_dict = extract_data(request)
        if not student_dict['name']:
            conn.close()  # Close the connection before returning
            return "Name is a required field"
        sql_query = f"""
                    UPDATE info SET
                    name='{student_dict['name']}',
                    address= '{student_dict['address']}', 
                    gender = '{student_dict['gender']}',
                    dob = '{student_dict['dob']}'
                    WHERE studentid = {student_dict['studentid']}"""
        c.execute(sql_query)
        conn.commit()
        sql_query = f"DELETE FROM scores WHERE studentid={student_dict['studentid']}"
        c.execute(sql_query)
        conn.commit()
        for k, v in student_scores_dict.items():
            if v is not None:
                v = float(v)
                sql_query = f"""
                    INSERT INTO Scores VALUES(
                        {student_dict['studentid']},
                        '{k}',
                        {v})"""
                c.execute(sql_query)
                conn.commit()
        conn.close()  # Close the connection after all database operations
        return f"Records for the studentID {student_dict['studentid']} have been updated"


@app.route('/courses')
def courses():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM scores")
    scores_list = c.fetchall()
    course_codes = ['CHEM101', 'PHYS101', 'MATH101']
    course_details = []
    for each_course in course_codes:
        course_dict = {'name': each_course,
                       'average': 0.0,
                       'num_students': 0,
                       'passed': 0}

        for each_score in scores_list:
            if each_course == each_score[1]:
                course_dict['num_students'] += 1
                course_dict['average'] += each_score[2]
                if each_score[2] >= 50.0:
                    course_dict['passed'] += 1
        course_dict['average'] /= course_dict['num_students']
        course_dict['average'] = round(course_dict['average'], 2)
        course_details.append(course_dict)
    conn.close()
    return render_template('course_info.html', course_details=course_details)
