import paramiko

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMessageBox

SSH_PORT = 22


class LoggerWindow(QWidget):
    switch_window = pyqtSignal()

    IP = ""
    LOGIN = ""
    PASSWORD = ""

    def __init__(self):
        super(LoggerWindow, self).__init__(flags=Qt.WindowFlags())

        self.title = QLabel(self)
        self.ip_label = QLabel(self)
        self.ip = QLineEdit(self)
        self.login_label = QLabel(self)
        self.login = QLineEdit(self)
        self.password_label = QLabel(self)
        self.password = QLineEdit(self)
        self.connect_button = QPushButton(self)

        self.setup()

    def setup(self):
        self.setObjectName("LoggerWindow")
        self.resize(300, 200)

        title_font = QtGui.QFont("Segoe UI", 13)
        title_font.setBold(True)

        self.title.setGeometry(QRect(50, 10, 200, 30))
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("title")

        self.ip.setGeometry(QRect(130, 50, 110, 25))
        self.ip.setObjectName("title")

        self.login.setGeometry(QRect(130, 80, 110, 25))
        self.login.setObjectName("login")

        self.password.setGeometry(QRect(130, 110, 110, 25))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setObjectName("password")

        self.ip_label.setGeometry(QRect(10, 50, 100, 25))
        self.ip_label.setAlignment(Qt.AlignCenter)
        self.ip_label.setObjectName("ip_label")

        self.login_label.setGeometry(QRect(10, 80, 100, 25))
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_label.setObjectName("login_label")

        self.password_label.setGeometry(QRect(10, 110, 100, 25))
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_label.setObjectName("password_label")

        self.connect_button.setGeometry(QRect(140, 150, 90, 23))
        self.connect_button.clicked.connect(self.connect)
        self.connect_button.setObjectName("connect_button")

        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle("Logger")

        self.title.setText("Connect to Footy:")
        self.ip_label.setText("IP")
        self.login_label.setText("login")
        self.password_label.setText("password")
        self.connect_button.setText("Connect")

    def connect(self):
        try:
            client = paramiko.SSHClient()

            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.ip.text(), port=SSH_PORT,
                           username=self.login.text(), password=self.password.text())
            client.exec_command('sudo python3 /home/pi/footy_control/server.py')

            client.close()

            LoggerWindow.IP = self.ip.text()
            LoggerWindow.LOGIN = self.login.text()
            LoggerWindow.PASSWORD = self.password.text()

            self.switch_window.emit()

        except Exception as err:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setWindowTitle("Error")
            error.setText("Authentication failed!")
            error.setInformativeText(str(err))
            error.exec_()
