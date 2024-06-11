from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
