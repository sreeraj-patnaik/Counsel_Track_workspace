import sqlite3
from db import getconnection
from db_functions import add_log  # for logging actions


from db import getconnection

def get_teacher_by_id(teacher_id=None, email=None):
    conn = getconnection()
    cur = conn.cursor()

    if email:
        cur.execute("SELECT * FROM teachers WHERE email = ?", (email,))
    elif teacher_id:
        cur.execute("SELECT * FROM teachers WHERE id = ?", (teacher_id,))
    else:
        return None

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    columns = [desc[0] for desc in cur.description]
    teacher = dict(zip(columns, row))
    return teacher

def get_mentees_list(teacher_id):
    """
    Returns a list of student IDs assigned to this teacher (using counselor field)
    """
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM students WHERE counselor = ?", (teacher_id,))
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]



def get_mentee_details(student_id):
    """
    Returns full student record as a dict
    """
    conn = getconnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None

    columns = [desc[0] for desc in cur.description]
    student = dict(zip(columns, row))
    conn.close()
    return student


def update_mentee_info(mentee_id, data: dict):
    """
    Teacher can update mentee fields like:
    suggestions_by_counselor, HoD_remarks, verified_status, etc.
    """
    if not data:
        return
    
    conn = getconnection()
    cur = conn.cursor()
    
    for field, value in data.items():
        cur.execute(f"UPDATE students SET {field} = ? WHERE id = ?", (value, mentee_id))
    
    conn.commit()
    conn.close()
    
    # Log teacher action
    add_log("teacher", mentee_id, "updated mentee profile")


def update_teacher_info(teacher_id, data: dict):
    """
    Update teacher fields like remarks, phone, or subjects_handled
    """
    if not data:
        return
    
    conn = getconnection()
    cur = conn.cursor()
    
    for field, value in data.items():
        cur.execute(f"UPDATE teachers SET {field} = ? WHERE id = ?", (value, teacher_id))
    
    conn.commit()
    conn.close()
    
    add_log("teacher", teacher_id, "updated own profile")
