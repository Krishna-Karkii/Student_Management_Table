import sqlite3
import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog,
                             QVBoxLayout, QLineEdit, QComboBox, QPushButton, QGridLayout, QToolBar,
                             QStatusBar)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(700, 500)

        # construct file option in menubar
        file_menu = self.menuBar().addMenu("&File")
        insert_action = QAction(QIcon("icons/add.png"), "Add", self)
        file_menu.addAction(insert_action)
        insert_action.triggered.connect(self.insert)

        # construct help option in menubar
        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("about", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Construct Edit option in menubar
        search_menu = self.menuBar().addMenu("&Edit")
        search_action = QAction(QIcon("icons/search.png"), "search", self)
        search_menu.addAction(search_action)
        search_menu.triggered.connect(self.search)

        # Construct a toolbar
        toolbar = QToolBar()
        toolbar.addAction(insert_action)
        toolbar.addAction(search_action)
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Construct table to show student information
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)
        self.table.verticalHeader().setVisible(False)

        # Construct a Statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

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

    def search(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def cell_clicked(self):
        edit_button = QPushButton("Edit Cell")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Cell")
        delete_button.clicked.connect(self.delete)

        children = self.statusbar.findChildren(QPushButton)

        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()


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
        self.setWindowTitle("Search Bar")
        layout = QGridLayout()

        # Creating search widget
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter the name of student...")

        # Creating search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)

        layout.addWidget(self.search_box, 0, 0)
        layout.addWidget(button, 0, 1)
        self.setLayout(layout)

    def search(self):
        name = self.search_box.text().title()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM students WHERE name=?", (name,))
        result = list(result)
        print(result)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cur.close()
        conn.close()


class EditDialog(QDialog):
    pass


class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
