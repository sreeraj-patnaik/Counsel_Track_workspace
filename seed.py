import sqlite3
from db import getconnection

def seed_students():
    conn = getconnection()
    cur = conn.cursor()

    students = [
        ("24KD1A1513", "SREERAJ DABBIRU", "24kd1a1513@lendi.edu.in", "sree"),
        ("S102", "Bob Williams", "bob@student.com", "bob123"),
        ("S103", "Charlie Lee", "charlie@student.com", "charlie123")
    ]

    for s in students:
        cur.execute("""
            INSERT OR IGNORE INTO students (id, name, email, password)
            VALUES (?, ?, ?, ?)
        """, s)
        print(f"Inserted student {s[1]}")

    conn.commit()
    conn.close()
    print("Minimal student data seeded successfully!")

def seed_teachers():
    conn = getconnection()
    cur = conn.cursor()

    teachers = [
        ("T101", "Mr. Smith", "smith@teacher.com", "smith123"),
        ("T102", "Mrs. Davis", "davis@teacher.com", "davis123")
    ]

    for t in teachers:
        cur.execute("""
            INSERT OR IGNORE INTO teachers (id, name, email, password)
            VALUES (?, ?, ?, ?)
        """, t)
        print(f"Inserted teacher {t[1]}")

    conn.commit()
    conn.close()
    print("Minimal teacher data seeded successfully!")

if __name__ == "__main__":
    seed_students()
    seed_teachers()
