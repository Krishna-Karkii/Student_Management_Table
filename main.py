import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        insert_action = QAction("Add")
        file_menu.addAction(insert_action)

        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("about")
        help_menu.addAction(about_action)



