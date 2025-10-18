import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QRadioButton, QMessageBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from db_functions import check_student_password, check_teacher_password, add_log
from student_functions import get_student_by_id
from teacher_functions import get_teacher_by_id
from signup import SignupWindow
from student_dashboard_modern import StudentDashboard
from teacher_dashboard_modern import TeacherDashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CounselTrack Login")
        self.setGeometry(400, 200, 650, 700)
        self.setMinimumSize(650, 700) 
        self.init_ui()
        self.center_window()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

    def init_ui(self):
      
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QFrame()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(70, 50, 70, 50)
        main_layout.setSpacing(25)

        title = QLabel("CounselTrack Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #2E3440; margin-bottom: 10px;")
        main_layout.addWidget(title)

        user_type_label = QLabel("Select User Type:")
        user_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_type_label.setStyleSheet("font-weight: bold; font-size: 18px; color: #4C566A;")
        main_layout.addWidget(user_type_label)

        self.student_radio = QRadioButton("Student")
        self.teacher_radio = QRadioButton("Teacher")
        self.student_radio.setChecked(True)

        radio_layout = QHBoxLayout()
        radio_layout.addStretch(1)
        radio_layout.addWidget(self.student_radio)
        radio_layout.addSpacing(30)
        radio_layout.addWidget(self.teacher_radio)
        radio_layout.addStretch(1)
        main_layout.addLayout(radio_layout)

        email_label = QLabel("Email:")
        email_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #4C566A;")
        main_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumHeight(50)
        main_layout.addWidget(self.email_input)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #4C566A;")
        main_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setMinimumHeight(50)
        main_layout.addWidget(self.password_input)

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(20)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setMinimumHeight(55)
        self.login_btn.setToolTip("Log in to your account")
        btn_layout.addWidget(self.login_btn)

        self.signup_btn = QPushButton("New user? Create an account")
        self.signup_btn.clicked.connect(self.open_signup)
        self.signup_btn.setMinimumHeight(55)
        self.signup_btn.setToolTip("Sign up for a new account")
        btn_layout.addWidget(self.signup_btn)

        btn_wrapper = QHBoxLayout()
        btn_wrapper.addStretch(1)
        btn_wrapper.addLayout(btn_layout)
        btn_wrapper.addStretch(1)
        main_layout.addLayout(btn_wrapper)

        main_layout.addStretch(2) 

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(scroll)

        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F8F9FA, stop:1 #ECEFF4);
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #2E3440;
            }
            QRadioButton {
                font-size: 16px;
                spacing: 12px;
                color: #4C566A;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #D8DEE9;
                background-color: #FFFFFF;
            }
            QRadioButton::indicator:checked {
                background-color: #5E81AC;
                border: 2px solid #5E81AC;
            }
            QLineEdit {
                padding: 12px;
                border-radius: 10px;
                border: 2px solid #D8DEE9;
                font-size: 15px;
                background-color: #FFFFFF;
            }
            QLineEdit:focus {
                border-color: #5E81AC;
                background-color: #F8F9FA;
            }
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #A3BE8C, stop:1 #88C0D0);
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8FBCBB, stop:1 #81A1C1);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5E81AC, stop:1 #4C566A);
            }
            QPushButton#signup {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D08770, stop:1 #BF616A);
            }
            QPushButton#signup:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #BF616A, stop:1 #A94442);
            }
            QPushButton#signup:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #A94442, stop:1 #8B0000);
            }
            QScrollArea { border: none; }
        """)
        self.signup_btn.setObjectName("signup")

    def open_signup(self):
        self.signup_window = SignupWindow(login_window=self)
        self.signup_window.show()
        self.hide()

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        user_type = "student" if self.student_radio.isChecked() else "teacher"

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter both email and password.")
            return

        if user_type == "student":
            if check_student_password(email, password):
                student = get_student_by_id(email=email)
                if not student:
                    QMessageBox.warning(self, "Error", "Student not found.")
                    return
                add_log("student", student["id"], "login")
                QMessageBox.information(self, "Success", f"Welcome {student['name']}!")
                self.open_student_dashboard(student["id"])
            else:
                QMessageBox.warning(self, "Error", "Invalid student email or password")
        else:
            if check_teacher_password(email, password):
                teacher = get_teacher_by_id(email=email)
                if not teacher:
                    QMessageBox.warning(self, "Error", "Teacher not found.")
                    return
                add_log("teacher", teacher["id"], "login")
                QMessageBox.information(self, "Success", f"Welcome {teacher['name']}!")
                self.open_teacher_dashboard(teacher["id"])
            else:
                QMessageBox.warning(self, "Error", "Invalid teacher email or password")

    def open_student_dashboard(self, student_id):
        self.dashboard = StudentDashboard(student_id, login_window=self)
        self.dashboard.show()
        self.hide()

    def open_teacher_dashboard(self, teacher_id):
        self.dashboard = TeacherDashboard(teacher_id, login_window=self)
        self.dashboard.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
