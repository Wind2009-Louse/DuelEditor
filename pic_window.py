#encoding:utf-8
import sys
import os

import requests
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap


class UI_PIC(QWidget):
    def __init__(self, parent=None, pic_id=0, pic_name = ""):
        self.parent = parent

        super(UI_PIC, self).__init__()
        self.setWindowTitle(pic_name)

        file_name = os.path.join(os.path.abspath('.'), "pics", "%d.png"%pic_id)
        if not os.path.exists(file_name):
            file_name = os.path.join(os.path.abspath('.'), "pics", "%d.jpg"%pic_id)
            if not os.path.exists(file_name):
                self.close()
                return
        png = QPixmap(file_name)
        width = png.width()
        height = png.height()
        self.setFixedSize(width, height)
        self.label = QLabel(self)
        self.label.setPixmap(png)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def closeEvent(self, event):
        if self.parent is not None:
            self.parent.clear_img_signal.emit("close")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = UI_PIC()

    m_window.show()
    sys.exit(app.exec_())
