import sqlite3
import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        insert_action = QAction("Add", self)
        file_menu.addAction(insert_action)

        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("about", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

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


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

