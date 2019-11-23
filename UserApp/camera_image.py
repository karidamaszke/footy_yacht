from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from urllib import request


class CameraImageReceiver(QThread):
    image_received = pyqtSignal(QPixmap)

    def __init__(self, ip):
        super(CameraImageReceiver, self).__init__()
        self.image_url = 'http://' + ip + '/html/cam_pic.php'

    def run(self):
        image = QImage()
        while True:
            image_data_buffer = request.urlopen(self.image_url).read()
            image.loadFromData(image_data_buffer)
            self.image_received.emit(QPixmap(image))
