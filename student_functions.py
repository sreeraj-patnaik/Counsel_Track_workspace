import sqlite3
from db import getconnection
from db_functions import add_log 


from db import getconnection

def get_student_by_id(student_id=None, email=None):
    conn = getconnection()
    cur = conn.cursor()

    if email:
        cur.execute("SELECT * FROM students WHERE email = ?", (email,))
    elif student_id:
        cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    else:
        return None

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    columns = [desc[0] for desc in cur.description]
    student = dict(zip(columns, row))
    return student


def update_student_info(student_id, data: dict):
    """
    Update multiple fields of a student.
    data = {'hobbies': 'Reading, Music', 'hours_of_study_per_day': 5, ...}
    """
    if not data:
        return

    conn = getconnection()
    cur = conn.cursor()

    for field, value in data.items():
        cur.execute(f"UPDATE students SET {field} = ? WHERE id = ?", (value, student_id))

    conn.commit()
    conn.close()

    add_log("student", student_id, "updated profile")

from db import getconnection

def get_unassigned_students():
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name FROM students
        WHERE counselor IS NULL OR counselor = ''
    """)
    students = cur.fetchall()
    conn.close()
    return students


def assign_mentee_to_teacher(student_id, teacher_id):
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students SET counselor = ? WHERE id = ?
    """, (teacher_id, student_id))
    conn.commit()
    conn.close()


