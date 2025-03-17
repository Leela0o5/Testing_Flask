from flask import Flask, redirect, render_template, request, url_for
import sqlite3 as sql
app = Flask(__name__)

def initdb():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON") 
    cur.execute("CREATE TABLE IF NOT EXISTS students (student_id INTEGER PRIMARY KEY AUTOINCREMENT,roll_number TEXT UNIQUE NOT NULL,first_name TEXT NOT NULL,last_name TEXT)")
    cur.execute(" CREATE TABLE IF NOT EXISTS course ( course_id INTEGER PRIMARY KEY AUTOINCREMENT,course_code TEXT UNIQUE NOT NULL,course_name TEXT NOT NULL,course_description TEXT NOT NULL )")
    cur.execute("CREATE TABLE IF NOT EXISTS enrollments (enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,student_id INTEGER NOT NULL,course_id INTEGER NOT NULL,FOREIGN KEY (student_id) REFERENCES student(student_id)  ON DELETE CASCADE,FOREIGN KEY (course_id) REFERENCES course(course_id))")
    cur.execute("DELETE FROM course") 
    cur.execute("INSERT INTO course (course_code, course_name, course_description) VALUES ('CSE01', 'MAD I', 'Modern Application Development - I')")
    cur.execute("INSERT INTO course (course_code, course_name, course_description) VALUES ('CSE02', 'DBMS', 'Database Management Systems')")
    cur.execute("INSERT INTO course (course_code, course_name, course_description) VALUES ('CSE03', 'PDSA', 'Programming, Data Structures and Algorithms using Python')")
    cur.execute("INSERT INTO course (course_code, course_name, course_description) VALUES ('BST13', 'BDM', 'Business Data Management')")
    conn.commit()
    conn.close()

initdb()

@app.route('/')
def home():
     with sql.connect("database.db") as conn:
             cur = conn.cursor()
             cur.execute("select * from students")
             rows = cur.fetchall()
             return render_template('home.html',rows=rows)

@app.route('/enternewstudent')
def new_student():
    return render_template('student.html')

@app.route('/addrecord',methods = ['POST', 'GET'])
def addrec():
    msg = ""
    conn=None
    if request.method == 'POST':
        try:
            roll = request.form['roll']
            f_name = request.form['f_name']
            l_name = request.form['l_name']
            courses = request.form.getlist('courses')
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("Insert into students (roll_number,first_name,last_name) values (?,?,?)",(roll,f_name,l_name))
                student_id = cur.lastrowid
                for course_id in courses:
                    cur.execute("INSERT INTO enrollments (student_id,course_id) values(?,?)",(student_id,course_id))
                conn.commit()
        except sql.IntegrityError:
                msg = "Student already exists. Please use different Roll Number!"
                redirect(url_for('alreadyExits',msg=msg))
        return redirect(url_for('home'))
    

@app.route('/delete/<int:student_id>')
def delete(student_id):
      with sql.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
      return redirect(url_for('home'))

@app.route('/update/<int:student_id>')
def update(student_id):
    roll = request.form['roll']
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    courses = request.form.getlist('courses')
    with sql.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE students SET roll_number = ?, first_name = ?, last_name = ? WHERE student_id = ?", (roll, f_name, l_name, student_id))
        conn.commit()
    return redirect(url_for('home'))



@app.route('/student/<int:student_id>')
def details(student_id):
        if request.method == 'POST':
            with sql.connect("database.db") as conn:
             cur = conn.cursor()
             cur.execute("select * from students where student_id=?",(student_id))
             rows = cur.fetchone()
             cur.execute("select * from enrollments where student_id=?",(student_id))
             rows2= cur.fetchall()
             return render_template('studentDetailsPage.html',rows=rows,rows2=rows2)
            


if __name__ == "__main__":
     app.run(debug=True)


