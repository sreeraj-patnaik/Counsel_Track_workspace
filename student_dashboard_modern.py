from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTabWidget, QScrollArea, QFormLayout, QFrame
)
from PyQt6.QtCore import Qt
from student_functions import get_student_by_id, update_student_info
from db_functions import add_log

class StudentDashboard(QWidget):
    def __init__(self, student_id, login_window=None):
        super().__init__()
        self.student_id = student_id
        self.login_window = login_window
        self.setWindowTitle("CounselTrack Student Dashboard")
        self.setGeometry(150, 50, 850, 650)
        self.fields = {}
        self.student_data = {}
        self.init_ui()
        self.load_student_data()

    def init_ui(self):
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QFrame()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Student Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #007BFF;")
        main_layout.addWidget(title)

        # Logout Button at top-right
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.setMinimumHeight(40)
        self.logout_btn.setStyleSheet("""
            QPushButton { background-color: #f44336; color: white; border-radius: 6px; font-weight:bold; }
            QPushButton:hover { background-color: #da190b; }
        """)
        main_layout.addWidget(self.logout_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Profile Tab
        self.profile_tab = QWidget()
        self.profile_layout = QVBoxLayout()
        self.profile_form = QFormLayout()
        self.profile_layout.addLayout(self.profile_form)
        self.profile_tab.setLayout(self.profile_layout)

        # Attendance/SGPA Tab
        self.attendance_tab = QWidget()
        self.attendance_layout = QVBoxLayout()
        self.attendance_form = QFormLayout()
        self.attendance_layout.addLayout(self.attendance_form)
        self.attendance_tab.setLayout(self.attendance_layout)

        # Remarks Tab
        self.remarks_tab = QWidget()
        self.remarks_layout = QVBoxLayout()
        self.remarks_form = QFormLayout()
        self.remarks_layout.addLayout(self.remarks_form)
        self.remarks_tab.setLayout(self.remarks_layout)

        self.tabs.addTab(self.profile_tab, "Profile")
        self.tabs.addTab(self.attendance_tab, "Attendance/SGPA")
        self.tabs.addTab(self.remarks_tab, "Remarks")

        # Editable and readonly fields
        self.editable_fields = [
            "name", "email", "password", "age", "semester", "mode_of_transport",
            "subject1", "subject2", "subject3", "subject4", "subject5", "subject6",
            "presentcgpa",
            "sem1sgpa", "sem2sgpa", "sem3sgpa", "sem4sgpa",
            "sem5sgpa", "sem6sgpa", "sem7sgpa", "sem8sgpa",
            "midsem1marks", "midsem2marks",
            "favourite_subject", "least_favourite_subject",
            "hobbies", "extracurricular_activities",
            "hours_of_study_per_day",
            "attendancem1", "attendancem2", "attendancem3",
            "attendancem4", "attendancem5"
        ]
        self.readonly_fields = ["suggestions_by_counselor", "HoD_remarks"]

        # Field categories
        profile_fields = [
            "name", "email", "password", "age", "semester", "mode_of_transport",
            "subject1", "subject2", "subject3", "subject4", "subject5", "subject6",
            "favourite_subject", "least_favourite_subject",
            "hobbies", "extracurricular_activities"
        ]
        attendance_fields = [
            "presentcgpa",
            "sem1sgpa", "sem2sgpa", "sem3sgpa", "sem4sgpa",
            "sem5sgpa", "sem6sgpa", "sem7sgpa", "sem8sgpa",
            "midsem1marks", "midsem2marks",
            "hours_of_study_per_day",
            "attendancem1", "attendancem2", "attendancem3",
            "attendancem4", "attendancem5"
        ]
        remarks_fields = self.readonly_fields

        # Create inputs
        for field in profile_fields:
            lbl = QLabel(field.replace("_", " ").title())
            edit = QLineEdit()
            edit.setPlaceholderText(f"Enter {field.replace('_',' ')}")
            edit.setMinimumHeight(35)
            edit.setStyleSheet("""
                QLineEdit { padding: 8px; border-radius: 6px; border:1px solid #ccc; font-size:14px; }
                QLineEdit:focus { border-color: #007BFF; }
            """)
            self.fields[field] = edit
            self.profile_form.addRow(lbl, edit)

        for field in attendance_fields:
            lbl = QLabel(field.replace("_", " ").title())
            edit = QLineEdit()
            edit.setMinimumHeight(35)
            edit.setStyleSheet("""
                QLineEdit { padding: 8px; border-radius: 6px; border:1px solid #ccc; font-size:14px; }
                QLineEdit:focus { border-color: #007BFF; }
            """)
            self.fields[field] = edit
            self.attendance_form.addRow(lbl, edit)

        for field in remarks_fields:
            lbl = QLabel(field.replace("_", " ").title())
            edit = QLineEdit()
            edit.setReadOnly(True)
            edit.setMinimumHeight(35)
            edit.setStyleSheet("""
                QLineEdit { padding: 8px; border-radius: 6px; border:1px solid #ccc; background:#eee; font-size:14px; }
            """)
            self.fields[field] = edit
            self.remarks_form.addRow(lbl, edit)

        # Save & Accept Remarks buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Changes")
        self.accept_btn = QPushButton("Accept Remarks")
        for btn in [self.save_btn, self.accept_btn]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton { background-color: #007BFF; color:white; border-radius:6px; font-weight:bold; }
                QPushButton:hover { background-color: #0056b3; }
            """)
            btn_layout.addWidget(btn)
        self.save_btn.clicked.connect(self.save_changes)
        self.accept_btn.clicked.connect(self.accept_remarks)
        main_layout.addLayout(btn_layout)

        # Set scroll as main layout
        window_layout = QVBoxLayout(self)
        window_layout.addWidget(scroll)

        # Global stylesheet
        self.setStyleSheet("""
            QWidget { background-color: #FFFFFF; font-family: Arial, sans-serif; color:#333; }
            QLabel { font-size:14px; }
        """)

    def load_student_data(self):
        data = get_student_by_id(self.student_id)
        if not data:
            QMessageBox.critical(self, "Error", "Student data not found!")
            self.close()
            return
        self.student_data = data
        for field, widget in self.fields.items():
            widget.setText(str(data.get(field, "")))

    def save_changes(self):
        new_data = {field: self.fields[field].text() for field in self.editable_fields}
        update_student_info(self.student_id, new_data)
        add_log("student", self.student_id, "updated profile")
        QMessageBox.information(self, "Success", "Profile updated successfully!")

    def accept_remarks(self):
        update_student_info(self.student_id, {"remarks_accepted": 1})
        add_log("student", self.student_id, "accepted remarks")
        QMessageBox.information(self, "Success", "Remarks accepted!")

    def logout(self):
        self.close()
        if self.login_window:
            self.login_window.show()
