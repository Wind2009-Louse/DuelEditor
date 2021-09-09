#encoding:utf-8
import sys
import os

import requests
import time
from threading import Thread
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap


class UI_PIC(QWidget):
    download_signal = pyqtSignal(bool)
    def __init__(self, parent=None, pic_id=0, pic_name = ""):
        self.parent = parent
        self.pic_id = pic_id

        super(UI_PIC, self).__init__()
        self.setWindowTitle(pic_name)
        self.download_signal.connect(self.download_connect)

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.resize(300, 300)

        file_name = os.path.join(os.path.abspath('.'), "pics", "%d.png"%pic_id)
        if not os.path.exists(file_name):
            file_name = os.path.join(os.path.abspath('.'), "pics", "%d.jpg"%pic_id)
            if not os.path.exists(file_name):
                self.download_thread = Download_Thread(self, pic_id)
                self.download_thread.setDaemon(True)
                self.download_thread.start()
                return
        self.show_pic()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def download_connect(self, sig):
        if sig:
            self.show_pic()
        else:
            self.close()

    def close_connect(self, args=None):
        self.close()
    
    def resizeEvent(self, event):
        self.label.resize(self.width(), self.height())

    def closeEvent(self, event):
        if self.parent is not None:
            self.parent.clear_img_signal.emit("close")

    def show_pic(self):
        file_name = os.path.join(os.path.abspath('.'), "pics", "%d.png"%self.pic_id)
        if not os.path.exists(file_name):
            file_name = os.path.join(os.path.abspath('.'), "pics", "%d.jpg"%self.pic_id)
            if not os.path.exists(file_name):
                self.close()
                return
        png = QPixmap(file_name)
        width = png.width()
        height = png.height()
        png = png.scaled(width, height)
        self.old_width = width
        self.old_height = height
        self.label.setPixmap(png)
        self.resize(width, height)

class Download_Thread(Thread):
    def __init__(self, window, pic_id=0):
        self.window = window
        self.pic_id = pic_id
        super().__init__()
    def run(self):
        if not os.path.exists("pics"):
            os.makedirs("pics")
        url = "https://cdn01.moecube.com/images/ygopro-images-zh-CN/%d.jpg"%self.pic_id
        filename = os.path.join("pics", "%d.jpg"%self.pic_id)
        try:
            with requests.get(url, stream=True) as req:
                if 'Content-length' in req.headers:
                    length = float(req.headers['Content-length'])
                    count = 0
                    with open(filename, 'wb') as f:
                        for chunk in req.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                count += len(chunk)
                                self.window.label.setText("下载中（%.2f%%）"%(count * 100 / length))
                else:
                    with open(filename, 'wb') as f:
                        f.write(req.content)
            self.window.download_signal.emit(True)
        except Exception as e:
            print(e)
            self.window.label.setText("下载失败！")
            time.sleep(3)
            self.window.download_signal.emit(False)

        self.window.label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = UI_PIC(None,  80254726, "80254726")

    m_window.show()
    sys.exit(app.exec_())
