from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTabWidget, QScrollArea, QFormLayout, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtCore import Qt
from teacher_functions import get_teacher_by_id, get_mentees_list, update_mentee_info
from student_functions import get_unassigned_students, assign_mentee_to_teacher, get_student_by_id
from db import getconnection
from db_functions import add_log

class TeacherDashboard(QWidget):
    def __init__(self, teacher_id, login_window=None):
        super().__init__()
        self.teacher_id = teacher_id
        self.login_window = login_window
        self.setWindowTitle("CounselTrack Teacher Dashboard")
        self.setGeometry(100, 50, 900, 650)
        self.fields = {}
        self.current_mentee_id = None
        self.init_ui()
        self.load_mentees()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QFrame()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        title = QLabel("Teacher Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:24px; font-weight:bold; color:#007BFF;")
        main_layout.addWidget(title)

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.setMinimumHeight(40)
        self.logout_btn.setStyleSheet("""
            QPushButton { background-color: #f44336; color: white; border-radius: 6px; font-weight:bold; }
            QPushButton:hover { background-color: #da190b; }
        """)
        main_layout.addWidget(self.logout_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.mentees_tab = QWidget()
        self.mentees_layout = QVBoxLayout()
        self.mentee_list_widget = QListWidget()
        self.mentee_list_widget.itemClicked.connect(self.load_mentee_data)
        self.mentees_layout.addWidget(self.mentee_list_widget)
        self.mentees_tab.setLayout(self.mentees_layout)
        self.tabs.addTab(self.mentees_tab, "Mentees")

        self.details_tab = QWidget()
        self.details_layout = QVBoxLayout()
        details_scroll = QScrollArea()
        details_scroll.setWidgetResizable(True)
        container_details = QFrame()
        self.form_layout = QFormLayout()
        container_details.setLayout(self.form_layout)
        details_scroll.setWidget(container_details)
        self.details_layout.addWidget(details_scroll)
        self.details_tab.setLayout(self.details_layout)
        self.tabs.addTab(self.details_tab, "Mentee Details")

        self.assign_tab = QWidget()
        assign_layout = QVBoxLayout()
        assign_layout.setSpacing(15)

        self.unassigned_list = QListWidget()
        assign_layout.addWidget(QLabel("Unassigned Students:"))
        assign_layout.addWidget(self.unassigned_list)

        self.assign_btn = QPushButton("Assign Selected to Me")
        self.assign_btn.setMinimumHeight(40)
        self.assign_btn.setStyleSheet("""
            QPushButton { background-color:#007BFF; color:white; border-radius:6px; font-weight:bold; }
            QPushButton:hover { background-color:#0056b3; }
        """)
        self.assign_btn.clicked.connect(self.assign_selected)
        assign_layout.addWidget(self.assign_btn)

        self.assign_tab.setLayout(assign_layout)
        self.tabs.addTab(self.assign_tab, "Assign Mentees")
        self.load_unassigned_students()

        self.editable_fields = ["suggestions_by_counselor", "HoD_remarks"]
        self.readonly_fields = [
            "name", "email", "age", "semester", "mode_of_transport",
            "subject1","subject2","subject3","subject4","subject5","subject6",
            "presentcgpa",
            "sem1sgpa","sem2sgpa","sem3sgpa","sem4sgpa",
            "sem5sgpa","sem6sgpa","sem7sgpa","sem8sgpa",
            "midsem1marks","midsem2marks",
            "favourite_subject","least_favourite_subject",
            "hobbies","extracurricular_activities",
            "hours_of_study_per_day",
            "attendancem1","attendancem2","attendancem3",
            "attendancem4","attendancem5"
        ]

        for field in self.readonly_fields:
            lbl = QLabel(field.replace("_"," ").title())
            edit = QLineEdit()
            edit.setReadOnly(True)
            edit.setMinimumHeight(35)
            edit.setStyleSheet("""
                QLineEdit { padding:8px; border-radius:6px; border:1px solid #ccc; background:#eee; font-size:14px; }
            """)
            self.fields[field] = edit
            self.form_layout.addRow(lbl, edit)

        for field in self.editable_fields:
            lbl = QLabel(field.replace("_"," ").title())
            edit = QLineEdit()
            edit.setMinimumHeight(35)
            edit.setStyleSheet("""
                QLineEdit { padding:8px; border-radius:6px; border:1px solid #ccc; font-size:14px; }
                QLineEdit:focus { border-color:#007BFF; }
            """)
            self.fields[field] = edit
            self.form_layout.addRow(lbl, edit)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setStyleSheet("""
            QPushButton { background-color:#007BFF; color:white; border-radius:6px; font-weight:bold; }
            QPushButton:hover { background-color:#0056b3; }
        """)
        self.save_btn.clicked.connect(self.save_changes)
        self.form_layout.addRow(self.save_btn)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(scroll)

        self.setStyleSheet("""
            QWidget { background-color:#fff; font-family: Arial, sans-serif; color:#333; }
            QLabel { font-size:14px; }
        """)

    def load_mentees(self):
        self.mentee_list_widget.clear()
        for mentee_id in get_mentees_list(self.teacher_id):
            student = get_student_by_id(student_id=mentee_id)
            if student:
                item = QListWidgetItem(f"{student['id']} - {student['name']}")
                self.mentee_list_widget.addItem(item)

    def load_mentee_data(self, item):
        mentee_id = item.text().split(" - ")[0]
        self.current_mentee_id = mentee_id

        conn = getconnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = ?", (mentee_id,))
        row = cur.fetchone()
        if not row:
            QMessageBox.critical(self, "Error", f"Mentee {mentee_id} not found!")
            return

        columns = [desc[0] for desc in cur.description]
        data = dict(zip(columns, row))
        conn.close()

        for field, widget in self.fields.items():
            widget.setText(str(data.get(field, "")))

        self.tabs.setCurrentWidget(self.details_tab)

    def save_changes(self):
        if not self.current_mentee_id:
            QMessageBox.warning(self, "Error", "No mentee selected!")
            return
        new_data = {field:self.fields[field].text() for field in self.editable_fields}
        update_mentee_info(self.current_mentee_id, new_data)
        add_log("teacher", self.teacher_id, f"updated mentee {self.current_mentee_id}")
        QMessageBox.information(self, "Success", "Mentee data updated successfully!")

    def load_unassigned_students(self):
        students = get_unassigned_students()
        self.unassigned_list.clear()
        for sid, name in students:
            self.unassigned_list.addItem(f"{sid} - {name}")

    def assign_selected(self):
        selected = self.unassigned_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Select a student to assign!")
            return
        sid = selected.text().split(" - ")[0]
        assign_mentee_to_teacher(sid, self.teacher_id)
        add_log("teacher", self.teacher_id, f"assigned mentee {sid}")
        QMessageBox.information(self, "Assigned", f"Student {sid} successfully assigned!")
        self.load_unassigned_students()
        self.load_mentees()

    def logout(self):
        self.close()
        if self.login_window:
            self.login_window.show()

