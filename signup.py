from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QRadioButton, QMessageBox
)
from db import getconnection

class SignupWindow(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("CounselTrack Signup")
        self.setGeometry(400, 200, 400, 400) 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        self.student_radio = QRadioButton("Student")
        self.teacher_radio = QRadioButton("Teacher")
        self.student_radio.setChecked(True)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.student_radio)
        radio_layout.addWidget(self.teacher_radio)
        layout.addLayout(radio_layout)

        layout.addWidget(QLabel("ID:"))
        self.id_input = QLineEdit()
        layout.addWidget(self.id_input)

        layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Password:"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pass_input)

        self.signup_btn = QPushButton("Create Account")
        self.signup_btn.clicked.connect(self.handle_signup)
        layout.addWidget(self.signup_btn)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QLabel {
                color: #495057;
                font-weight: bold;
            }
            QRadioButton {
                font-size: 15px;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #CCCCCC;
                border-radius: 9px;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #007BFF;
                border: 2px solid #007BFF;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #CCCCCC;
                background-color: #FAFAFA;
            }
            QLineEdit:focus {
                border: 1.5px solid #007BFF;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

    def handle_signup(self):
        id_ = self.id_input.text().strip()
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.pass_input.text().strip()
        user_type = "student" if self.student_radio.isChecked() else "teacher"

        if not id_ or not name or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        conn = getconnection()
        cur = conn.cursor()

        try:
            if user_type == "student":
                cur.execute("INSERT INTO students (id, name, email, password) VALUES (?, ?, ?, ?)", 
                            (id_, name, email, password))
            else:
                cur.execute("""
                    INSERT INTO teachers (id, name, email, department, designation, experience, subjects_handled, password, phone)
                    VALUES (?, ?, ?, '', '', 0, '', ?, '')
                """, (id_, name, email, password))

            conn.commit()
            QMessageBox.information(self, "Success", f"{user_type.title()} account created successfully!")
            self.close()
            if self.login_window:
                self.login_window.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Signup failed: {str(e)}")
        finally:
            conn.close()

