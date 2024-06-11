import sqlite3
import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog,
                             QVBoxLayout, QLineEdit, QComboBox, QPushButton)
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # constructed file option in menubar
        file_menu = self.menuBar().addMenu("&File")
        insert_action = QAction("Add", self)
        file_menu.addAction(insert_action)
        insert_action.triggered.connect(self.insert)

        # constructed help option in menubar
        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("about", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Constructed table to show student information
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)
        self.table.verticalHeader().setVisible(False)

    def load_data(self):
        conn = sqlite3.connect("database.db")
        result = list(conn.execute("SELECT * FROM students"))
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(result):
            self.table.insertRow(row_index)
            for column_index, column_data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))

        conn.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Info")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # create widget for student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name..")
        layout.addWidget(self.student_name)

        # create widget for student course
        self.course_select_box = QComboBox()
        course_list = ['Biology', 'Chemistry', 'Astronomy', 'Physics']
        self.course_select_box.addItems(course_list)
        layout.addWidget(self.course_select_box)

        # create widget for student number
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Phone number...")
        layout.addWidget(self.mobile)

        # create button for submitting student info
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.insert_to_database)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def insert_to_database(self):
        name = self.student_name.text()
        course = self.course_select_box.currentText()
        mobile = self.mobile.text()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, course, mobile) Values(?,?,?)",
                    (name, course, mobile))
        conn.commit()
        cur.close()
        conn.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.windowTitle("Search Bar")
        self.setFixedWidth(150)
        self.setFixedHeight(150)

        layout = QVBoxLayout()

        # Creating search widget
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter the name of student...")
        layout.addWidget(self.search_box)

        self.setLayout(layout)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

