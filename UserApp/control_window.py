from functools import partial
from time import sleep

import paramiko
from PyQt5.QtCore import Qt, QRect, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QGraphicsView, QPushButton, QLabel, QMessageBox, QGraphicsScene

from camera_image import CameraImageReceiver
from udp_client import Client

SSH_PORT = 22


class ControlWindow(QWidget):
    START_CAMERA = 'sudo /home/pi/RPi_Cam_Web_Interface/start.sh'
    STOP_CAMERA = 'sudo /home/pi/RPi_Cam_Web_Interface/stop.sh'

    def __init__(self, ip='', login='', password=''):
        super(ControlWindow, self).__init__(flags=Qt.WindowFlags())

        self.ip = ip
        self.login = login
        self.password = password

        self.client = Client(self.ip)
        self.camera_image_receiver = CameraImageReceiver(self.ip)

        self.camera_image_frame = QGraphicsView(self)
        self.camera_image = QGraphicsScene(self)
        self.title = QLabel(self)
        self.rudder_label = QLabel(self)
        self.rudder_left_button = QPushButton(self)
        self.rudder_right_button = QPushButton(self)
        self.sail_label = QLabel(self)
        self.fall_off_button = QPushButton(self)
        self.luff_button = QPushButton(self)
        self.camera_label = QLabel(self)
        self.camera_on_button = QPushButton(self)
        self.camera_off_button = QPushButton(self)
        self.exit_button = QPushButton(self)

        self.setup()

    def setup(self):
        self.setObjectName("Dialog")
        self.resize(730, 480)

        title_font = QFont("Segoe UI", 13)
        title_font.setBold(True)

        label_font = QFont("Segoe UI", 11)
        label_font.setBold(True)

        self.title.setGeometry(QRect(15, 10, 700, 40))
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("title")

        self.rudder_label.setGeometry(QRect(555, 70, 160, 30))
        self.rudder_label.setFont(label_font)
        self.rudder_label.setAlignment(Qt.AlignCenter)
        self.rudder_label.setObjectName("rudder_label")

        self.rudder_left_button.setGeometry(QRect(555, 110, 75, 25))
        self.rudder_left_button.setObjectName("rudder_left")
        self.rudder_left_button.clicked.connect(partial(self.send_message, message="RUDDER_DOWN"))

        self.rudder_right_button.setGeometry(QRect(640, 110, 75, 25))
        self.rudder_right_button.setObjectName("rudder_right")
        self.rudder_right_button.clicked.connect(partial(self.send_message, message="RUDDER_UP"))

        self.sail_label.setGeometry(QRect(555, 170, 160, 30))
        self.sail_label.setFont(label_font)
        self.sail_label.setAlignment(Qt.AlignCenter)
        self.sail_label.setObjectName("sail_label")

        self.luff_button.setGeometry(QRect(555, 210, 75, 25))
        self.luff_button.setObjectName("luff_button")
        self.luff_button.clicked.connect(partial(self.send_message, message="SAIL_DOWN"))

        self.fall_off_button.setGeometry(QRect(640, 210, 75, 25))
        self.fall_off_button.setObjectName("fall_off_button")
        self.fall_off_button.clicked.connect(partial(self.send_message, message="SAIL_UP"))

        self.camera_label.setGeometry(QRect(555, 270, 160, 30))
        self.camera_label.setFont(label_font)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setObjectName("camera_label")

        self.camera_on_button.setGeometry(QRect(555, 310, 75, 25))
        self.camera_on_button.setObjectName("camera_on_button")
        self.camera_on_button.clicked.connect(partial(self.start_stop_camera, command=self.START_CAMERA))

        self.camera_off_button.setGeometry(QRect(640, 310, 75, 25))
        self.camera_off_button.setObjectName("camera_off_button")
        self.camera_off_button.clicked.connect(partial(self.start_stop_camera, command=self.STOP_CAMERA))

        self.exit_button.setGeometry(QRect(555, 410, 160, 30))
        self.exit_button.setObjectName("exit_button")
        self.exit_button.clicked.connect(partial(self.send_message, message="END"))

        self.camera_image_frame.setGeometry(QRect(26, 70, 514, 386))
        self.camera_image_frame.setScene(self.camera_image)
        self.displayed_camera_image = self.camera_image.addPixmap(QPixmap(QImage()))

        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle("Footy Control")
        self.title.setText("FOOTY YACHT CONTROLLER: " + self.ip)

        self.rudder_label.setText("Rudder angle:")
        self.rudder_right_button.setText("RIGHT")
        self.rudder_left_button.setText("LEFT")

        self.sail_label.setText("Sail position:")
        self.fall_off_button.setText("FALL OFF")
        self.luff_button.setText("LUFF")

        self.camera_label.setText("Camera:")
        self.camera_on_button.setText("START")
        self.camera_off_button.setText("STOP")

        self.exit_button.setText("EXIT")

    def start_stop_camera(self, command):
        try:
            client = paramiko.SSHClient()

            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.ip, port=SSH_PORT,
                           username=self.login, password=self.password)
            client.exec_command(command)
            sleep(4)

            client.close()

            if "start" in command:
                self.init_camera_receiver()

        except Exception as err:
            self.error_message("Authentication failed!", str(err))

    def send_message(self, message):
        try:
            self.client.send_order(message)
        except Exception as err:
            self.error_message("Connection failed!", str(err))

        if message is "END":
            self.start_stop_camera(self.STOP_CAMERA)
            self.close()

    def init_camera_receiver(self):
        self.camera_image_receiver.image_received.connect(self.camera_image_update)
        self.camera_image_receiver.start()

    @pyqtSlot(QPixmap)
    def camera_image_update(self, current_image):
        self.displayed_camera_image.setPixmap(current_image)

    @staticmethod
    def error_message(error_title, error_message):
        error = QMessageBox()
        error.setIcon(QMessageBox.Critical)
        error.setWindowTitle("Error")
        error.setText(error_title)
        error.setInformativeText(error_message)
        error.exec_()
