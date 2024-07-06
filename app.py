from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'students.db'

def init_sqlite_db():
    conn = sqlite3.connect(DATABASE)
    print("Opened database successfully")

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Student_info (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            date_of_birth DATE
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Students_subject (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Student_marks (
            mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            marks INTEGER,
            FOREIGN KEY (student_id) REFERENCES Student_info(student_id),
            FOREIGN KEY (subject_id) REFERENCES Students_subject(subject_id)
        )
    ''')
    print("Tables created successfully")
    
    conn.execute('''
        INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin')
    ''')
    conn.commit()
    conn.close()

init_sqlite_db()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and user['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        subject_names = request.form.getlist('subject_name[]')
        marks = request.form.getlist('marks[]')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Student_info (student_id, first_name, last_name, date_of_birth) VALUES (?, ?, ?, ?)', 
                         (student_id, first_name, last_name, date_of_birth))
            
            for subject_name, mark in zip(subject_names, marks):
                conn.execute('INSERT OR IGNORE INTO Students_subject (subject_name) VALUES (?)', (subject_name,))
                subject_id = conn.execute('SELECT subject_id FROM Students_subject WHERE subject_name = ?', (subject_name,)).fetchone()['subject_id']
                conn.execute('INSERT INTO Student_marks (student_id, subject_id, marks) VALUES (?, ?, ?)', 
                             (student_id, subject_id, mark))
            
            conn.commit()
            flash('Student added successfully!')
        except sqlite3.IntegrityError:
            flash('Student ID already exists. Please choose a different one.')
        finally:
            conn.close()
        
        return redirect(url_for('add_student'))

    return render_template('add_student.html')

@app.route('/view-students')
def view_students():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('''
        SELECT si.student_id, si.first_name, si.last_name, si.date_of_birth,
               group_concat(ss.subject_name) as subjects,
               group_concat(sm.marks) as marks
        FROM Student_info si
        LEFT JOIN Student_marks sm ON si.student_id = sm.student_id
        LEFT JOIN Students_subject ss ON sm.subject_id = ss.subject_id
        GROUP BY si.student_id
    ''').fetchall()
    conn.close()
    return render_template('view_students.html', students=students)

@app.route('/search')
def search():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('search.html')

@app.route('/search-student', methods=['GET', 'POST'])
def search_student():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        roll_number = request.form['roll_number']
        conn = get_db_connection()

        student_info = conn.execute('SELECT * FROM Student_info WHERE student_id = ?', (roll_number,)).fetchone()
        
        if student_info:
            subjects = conn.execute('''
                SELECT ss.subject_name, sm.marks 
                FROM Student_marks sm
                JOIN Students_subject ss ON sm.subject_id = ss.subject_id
                WHERE sm.student_id = ?
            ''', (roll_number,)).fetchall()

            student = {
                'student_id': student_info['student_id'],
                'first_name': student_info['first_name'],
                'last_name': student_info['last_name'],
                'date_of_birth': student_info['date_of_birth'],
                'subjects': [{'subject_name': subject['subject_name'], 'marks': subject['marks']} for subject in subjects]
            }

            conn.close()
            return render_template('student_details.html', student=student)
        else:
            conn.close()
            flash(f"No student found with Roll Number: {roll_number}")
            return render_template('search.html')

    return redirect(url_for('search'))

@app.route('/delete-student/<int:id>')
def delete_student(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM Student_info WHERE student_id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Student deleted successfully!')
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(debug=True)
