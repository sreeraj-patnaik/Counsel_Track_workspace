import sqlite3
import os
import sys
import shutil

APP_NAME = "MyApp"  

def get_user_data_dir():
    """Return a folder path to store the writable DB."""
    if sys.platform == "win32":
        base_dir = os.getenv('APPDATA')  
    else:
        base_dir = os.path.expanduser("~")  

    app_dir = os.path.join(base_dir, APP_NAME)
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

def get_database_path():
    """
    Returns the path to a writable database.
    If running as .exe, copies bundled DB once to AppData for read/write.
    """
    user_dir = get_user_data_dir()
    db_path = os.path.join(user_dir, "database.db")

    if not os.path.exists(db_path):
        if getattr(sys, 'frozen', False):
            bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            bundled_db = os.path.join(bundle_dir, "database.db")
        else:
            bundled_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

        if os.path.exists(bundled_db):
            shutil.copy2(bundled_db, db_path)
            print(f" Copied bundled DB to user folder: {db_path}")
        else:
            raise FileNotFoundError(f"Bundled DB not found at {bundled_db}")

    return db_path

def getconnection():
    """Connect to the writable database."""
    return sqlite3.connect(get_database_path())

def init_db():
    """Initialize database tables if not existing."""
    conn = getconnection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER,
            semester INTEGER,
            mode_of_transport TEXT,
            counselor TEXT,
            subject1 TEXT,
            subject2 TEXT,
            subject3 TEXT,
            subject4 TEXT,
            subject5 TEXT,
            subject6 TEXT,
            presentcgpa REAL,
            sem1sgpa REAL,
            sem2sgpa REAL,
            sem3sgpa REAL,
            sem4sgpa REAL,
            sem5sgpa REAL,
            sem6sgpa REAL,
            sem7sgpa REAL,
            sem8sgpa REAL,
            midsem1marks TEXT,
            midsem2marks TEXT,
            favourite_subject TEXT,
            least_favourite_subject TEXT,
            hobbies TEXT,
            extracurricular_activities TEXT,
            hours_of_study_per_day INTEGER,
            attendancem1 INTEGER,
            attendancem2 INTEGER,
            attendancem3 INTEGER,
            attendancem4 INTEGER,
            attendancem5 INTEGER,
            suggestions_by_counselor TEXT,
            HoD_remarks TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            department TEXT,
            designation TEXT,
            experience INTEGER,
            subjects_handled TEXT,
            password TEXT,
            phone TEXT,
            mentee1 TEXT,
            mentee2 TEXT,
            mentee3 TEXT,
            mentee4 TEXT,
            mentee5 TEXT,
            mentee6 TEXT,
            mentee7 TEXT,
            mentee8 TEXT,
            mentee9 TEXT,
            mentee10 TEXT,
            mentee11 TEXT,
            mentee12 TEXT,
            mentee13 TEXT,
            mentee14 TEXT,
            mentee15 TEXT,
            mentee16 TEXT,
            remarks TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            action TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database initialized and ready at: {get_database_path()}")

if __name__ == "__main__":
    init_db()

