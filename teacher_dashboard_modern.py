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
        self.setGeometry(100, 50, 950, 700)
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
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(25)

        # Header Section
        header_layout = QHBoxLayout()
        title = QLabel("Teacher Dashboard")
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

        # Mentees Tab
        self.mentees_tab = QWidget()
        self.mentees_layout = QVBoxLayout()
        self.mentee_list_widget = QListWidget()
        self.mentee_list_widget.itemClicked.connect(self.load_mentee_data)
        self.mentee_list_widget.setStyleSheet("""
            QListWidget { border: 2px solid #D8DEE9; border-radius: 10px; background-color: #FFFFFF; font-size: 14px; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #ECEFF4; }
            QListWidget::item:selected { background-color: #81A1C1; color: white; }
            QListWidget::item:hover { background-color: #D8DEE9; }
        """)
        self.mentees_layout.addWidget(self.mentee_list_widget)
        self.mentees_tab.setLayout(self.mentees_layout)
        self.tabs.addTab(self.mentees_tab, "Mentees")

        # Details Tab
        self.details_tab = QWidget()
        self.details_layout = QVBoxLayout()
        details_scroll = QScrollArea()
        details_scroll.setWidgetResizable(True)
        container_details = QFrame()
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)
        container_details.setLayout(self.form_layout)
        details_scroll.setWidget(container_details)
        self.details_layout.addWidget(details_scroll)
        self.details_tab.setLayout(self.details_layout)
        self.tabs.addTab(self.details_tab, "Mentee Details")

        # Assign Tab
        self.assign_tab = QWidget()
        assign_layout = QVBoxLayout()
        assign_layout.setSpacing(20)

        assign_label = QLabel("Unassigned Students:")
        assign_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4C566A;")
        assign_layout.addWidget(assign_label)

        self.unassigned_list = QListWidget()
        self.unassigned_list.setStyleSheet("""
            QListWidget { border: 2px solid #D8DEE9; border-radius: 10px; background-color: #FFFFFF; font-size: 14px; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #ECEFF4; }
            QListWidget::item:selected { background-color: #81A1C1; color: white; }
            QListWidget::item:hover { background-color: #D8DEE9; }
        """)
        assign_layout.addWidget(self.unassigned_list)

        self.assign_btn = QPushButton("Assign Selected to Me")
        self.assign_btn.setMinimumHeight(50)
        self.assign_btn.setToolTip("Assign the selected student as your mentee")
        self.assign_btn.setStyleSheet("""
            QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #A3BE8C, stop:1 #88C0D0); color: white; border-radius: 12px; font-weight: bold; font-size: 15px; padding: 15px; }
            QPushButton:hover { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8FBCBB, stop:1 #81A1C1); }
            QPushButton:pressed { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5E81AC, stop:1 #4C566A); }
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
            lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #4C566A;")
            edit = QLineEdit()
            edit.setReadOnly(True)
            edit.setMinimumHeight(45)
            edit.setStyleSheet("""
                QLineEdit { padding: 12px; border-radius: 10px; border: 2px solid #D8DEE9; background-color: #ECEFF4; font-size: 14px; color: #8FBCBB; }
            """)
            self.fields[field] = edit
            self.form_layout.addRow(lbl, edit)

        for field in self.editable_fields:
            lbl = QLabel(field.replace("_"," ").title())
            lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #4C566A;")
            edit = QLineEdit()
            edit.setMinimumHeight(45)
            edit.setStyleSheet("""
                QLineEdit { padding: 12px; border-radius: 10px; border: 2px solid #D8DEE9; font-size: 14px; background-color: #FFFFFF; }
                QLineEdit:focus { border-color: #5E81AC; background-color: #F8F9FA; }
            """)
            self.fields[field] = edit
            self.form_layout.addRow(lbl, edit)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setMinimumHeight(50)
        self.save_btn.setToolTip("Save the updated mentee information")
        self.save_btn.setStyleSheet("""
            QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #A3BE8C, stop:1 #88C0D0); color: white; border-radius: 12px; font-weight: bold; font-size: 15px; padding: 15px; }
            QPushButton:hover { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8FBCBB, stop:1 #81A1C1); }
            QPushButton:pressed { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5E81AC, stop:1 #4C566A); }
        """)
        self.save_btn.clicked.connect(self.save_changes)
        self.form_layout.addRow(self.save_btn)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(scroll)

        self.setStyleSheet("""
            QWidget { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F8F9FA, stop:1 #ECEFF4); font-family: 'Segoe UI', Arial, sans-serif; color: #2E3440; }
            QLabel { font-size: 15px; }
            QScrollArea { border: none; }
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
