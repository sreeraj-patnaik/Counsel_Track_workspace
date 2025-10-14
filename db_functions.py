import sqlite3
from db import getconnection





def get_student_by_email(email):
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE email = ?", (email,))
    student = cur.fetchone()
    conn.close()
    return student

def check_student_password(email, password):
    student = get_student_by_email(email)
    if student and student[3] == password:  
        return True
    return False

def update_student_field(student_id, field, value):
    conn = getconnection()
    cur = conn.cursor()
    cur.execute(f"UPDATE students SET {field} = ? WHERE id = ?", (value, student_id))
    conn.commit()
    conn.close()



def get_teacher_by_email(email):
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teachers WHERE email = ?", (email,))
    teacher = cur.fetchone()
    conn.close()
    return teacher

def check_teacher_password(email, password):
    teacher = get_teacher_by_email(email)
    if teacher and teacher[7] == password:  
        return True
    return False

def get_teacher_mentees(teacher_id):
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teachers WHERE id = ?", (teacher_id,))
    teacher = cur.fetchone()
    conn.close()
    if teacher:
        mentees = [m for m in teacher[9:25] if m]  
        return mentees
    return []


def add_log(user_type, user_id, action="login"):
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO login_logs (user_type, user_id, action) VALUES (?, ?, ?)",
                (user_type, str(user_id), action))
    conn.commit()
    conn.close()

def get_logs(user_type=None):
    conn = getconnection()
    cur = conn.cursor()
    if user_type:
        cur.execute("SELECT * FROM login_logs WHERE user_type = ?", (user_type,))
    else:
        cur.execute("SELECT * FROM login_logs")
    logs = cur.fetchall()
    conn.close()
    return logs

