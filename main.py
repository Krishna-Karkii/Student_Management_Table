import sqlite3
import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog,
                             QVBoxLayout, QLineEdit, QComboBox, QPushButton, QGridLayout, QToolBar,
                             QStatusBar, QLabel, QMessageBox)
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
        about_action.triggered.connect(self.about)
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

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Message")
        content = """
        This app was build for fun through learning process
        where i encountered various different apps"""
        self.setText(content)


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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Info")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        index = main_window.table.currentRow()
        self.student_id = main_window.table.item(index, 0)

        # Create student name widget with current name
        name = main_window.table.item(index, 1).text()
        self.student_name = QLineEdit(name)
        self.student_name.setPlaceholderText("name")
        layout.addWidget(self.student_name)

        # create course name widget with current course name
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        course_list = ['Biology', 'Chemistry', 'Astronomy', 'Physics']
        self.course_name.addItems(course_list)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Create mobile widget with current mobile number
        phone_number = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(phone_number)
        layout.addWidget(self.mobile)

        # Create button to register updated info
        button = QPushButton("Register")
        button.clicked.connect(self.update_student_info)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student_info(self):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?",
                    (self.student_name.text(),
                     self.course_name.currentText(),
                     self.mobile.text(),
                     self.student_id.text()))
        conn.commit()
        cur.close()
        conn.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Info")

        layout = QGridLayout()

        conformation_label = QLabel("Are you sure you want to delete selected data?")
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete_data)
        no_button = QPushButton("No")

        layout.addWidget(conformation_label, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0, 1, 1)
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)

    def delete_data(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0)

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("DELETE from students WHERE id = ?",
                    (student_id.text(),))
        conn.commit()
        cur.close()
        conn.close()
        main_window.load_data()

        self.close()

        # Conformation message of deletion to the user
        conformation_message = QMessageBox()
        conformation_message.setWindowTitle("About Message")
        conformation_message.setText("Student data has been successfully deleted!")
        conformation_message.exec()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
