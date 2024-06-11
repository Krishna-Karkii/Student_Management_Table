import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QTableWidget
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

    def load_table_data(self):
        pass


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())

