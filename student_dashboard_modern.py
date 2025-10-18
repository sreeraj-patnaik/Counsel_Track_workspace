from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTabWidget, QScrollArea, QFormLayout, QFrame, QGroupBox
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
        self.setGeometry(150, 50, 900, 700)
        self.fields = {}
        self.student_data = {}
        self.init_ui()
        self.load_student_data()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QFrame()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(25)

        # Header Section
        header_layout = QHBoxLayout()
        title = QLabel("CounselTrack - Student Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #2E3440; margin-bottom: 10px;")
        header_layout.addWidget(title)

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.setMinimumHeight(45)
        self.logout_btn.setStyleSheet("""
            QPushButton { background-color: #BF616A; color: white; border-radius: 10px; font-weight: bold; font-size: 14px; padding: 12px 20px; }
            QPushButton:hover { background-color: #D08770; }
            QPushButton:pressed { background-color: #A94442; }
        """)
        header_layout.addWidget(self.logout_btn, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(header_layout)

        # Tabs with improved styling
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 2px solid #D8DEE9; border-radius: 12px; background-color: #FFFFFF; }
            QTabBar::tab { background-color: #ECEFF4; color: #2E3440; padding: 15px 25px; margin-right: 5px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 14px; }
            QTabBar::tab:selected { background-color: #5E81AC; color: white; }
            QTabBar::tab:hover { background-color: #81A1C1; color: white; }
        """)
        main_layout.addWidget(self.tabs)

        # Profile Tab
        self.profile_tab = QWidget()
        self.profile_layout = QVBoxLayout()
        self.profile_form = QFormLayout()
        self.profile_form.setSpacing(20)
        self.profile_layout.addLayout(self.profile_form)
        self.profile_tab.setLayout(self.profile_layout)

        # Attendance Tab
        self.attendance_tab = QWidget()
        self.attendance_layout = QVBoxLayout()
        self.attendance_form = QFormLayout()
        self.attendance_form.setSpacing(20)
        self.attendance_layout.addLayout(self.attendance_form)
        self.attendance_tab.setLayout(self.attendance_layout)

        # Remarks Tab
        self.remarks_tab = QWidget()
        self.remarks_layout = QVBoxLayout()
        self.remarks_form = QFormLayout()
        self.remarks_form.setSpacing(20)
        self.remarks_layout.addLayout(self.remarks_form)
        self.remarks_tab.setLayout(self.remarks_layout)

        self.tabs.addTab(self.profile_tab, "Profile")
        self.tabs.addTab(self.attendance_tab, "Attendance/SGPA")
        self.tabs.addTab(self.remarks_tab, "Remarks")

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

        # Profile Fields
        for field in profile_fields:
            lbl = QLabel(field.replace("_", " ").title())
            lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #4C566A;")
            edit = QLineEdit()
            edit.setPlaceholderText(f"Enter {field.replace('_',' ')}")
            edit.setMinimumHeight(45)
            edit.setStyleSheet("""
                QLineEdit { padding: 12px; border-radius: 10px; border: 2px solid #D8DEE9; font-size: 14px; background-color: #FFFFFF; }
                QLineEdit:focus { border-color: #5E81AC; background-color: #F8F9FA; }
            """)
            self.fields[field] = edit
            self.profile_form.addRow(lbl, edit)

        # Attendance Fields
        for field in attendance_fields:
            lbl = QLabel(field.replace("_", " ").title())
            lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #4C566A;")
            edit = QLineEdit()
            edit.setMinimumHeight(45)
            edit.setStyleSheet("""
                QLineEdit { padding: 12px; border-radius: 10px; border: 2px solid #D8DEE9; font-size: 14px; background-color: #FFFFFF; }
                QLineEdit:focus { border-color: #5E81AC; background-color: #F8F9FA; }
            """)
            self.fields[field] = edit
            self.attendance_form.addRow(lbl, edit)

        # Remarks Fields
        for field in remarks_fields:
            lbl = QLabel(field.replace("_", " ").title())
            lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #4C566A;")
            edit = QLineEdit()
            edit.setReadOnly(True)
            edit.setMinimumHeight(45)
            edit.setStyleSheet("""
                QLineEdit { padding: 12px; border-radius: 10px; border: 2px solid #D8DEE9; background-color: #ECEFF4; font-size: 14px; color: #8FBCBB; }
            """)
            self.fields[field] = edit
            self.remarks_form.addRow(lbl, edit)

        # Buttons Section
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setToolTip("Save your updated information")
        self.accept_btn = QPushButton("Accept Remarks")
        self.accept_btn.setToolTip("Accept the counselor's remarks")
        for btn in [self.save_btn, self.accept_btn]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #A3BE8C, stop:1 #88C0D0); color: white; border-radius: 12px; font-weight: bold; font-size: 15px; padding: 15px; }
                QPushButton:hover { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8FBCBB, stop:1 #81A1C1); }
                QPushButton:pressed { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5E81AC, stop:1 #4C566A); }
            """)
            btn_layout.addWidget(btn)
        self.save_btn.clicked.connect(self.save_changes)
        self.accept_btn.clicked.connect(self.accept_remarks)
        main_layout.addLayout(btn_layout)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(scroll)

        self.setStyleSheet("""
            QWidget { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F8F9FA, stop:1 #ECEFF4); font-family: 'Segoe UI', Arial, sans-serif; color: #2E3440; }
            QLabel { font-size: 15px; }
            QScrollArea { border: none; }
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
