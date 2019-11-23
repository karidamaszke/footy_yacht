import sys

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

from control_window import ControlWindow
from logger_window import LoggerWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(flags=Qt.WindowFlags())
        self.logger = LoggerWindow()

    def show_logger(self):
        self.logger.switch_window.connect(self.show_controller)
        self.logger.show()

    def show_controller(self):
        self.logger.close()
        self.controller = ControlWindow(self.logger.IP, self.logger.LOGIN, self.logger.PASSWORD)
        self.controller.show()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = MainWindow()
    window.show_logger()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
