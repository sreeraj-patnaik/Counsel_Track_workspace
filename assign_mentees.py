from PyQt6.QtWidgets import (
    QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout, QMessageBox
)
from db import getconnection

class MenteeAssignmentWindow(QWidget):
    def __init__(self, teacher_id):
        super().__init__()
        self.teacher_id = teacher_id
        self.setWindowTitle("Assign Mentees")
        self.setGeometry(400, 200, 400, 500)
        self.init_ui()
        self.load_students()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Select students to assign:")
        layout.addWidget(self.label)

        self.student_list = QListWidget()
        self.student_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.student_list)

        self.assign_btn = QPushButton("Assign Selected")
        self.assign_btn.clicked.connect(self.assign_selected)
        layout.addWidget(self.assign_btn)

        self.setLayout(layout)

    def load_students(self):
        conn = getconnection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM students")
        students = cur.fetchall()
        conn.close()

        self.student_list.clear()
        for sid, name in students:
            self.student_list.addItem(f"{sid} - {name}")

    def assign_selected(self):
        selected = self.student_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Select at least one student.")
            return

        student_ids = [s.text().split(" - ")[0] for s in selected]

        conn = getconnection()
        cur = conn.cursor()
        for sid in student_ids:
            cur.execute("UPDATE students SET counselor = ? WHERE id = ?", (self.teacher_id, sid))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Mentees assigned successfully!")
