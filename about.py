#encoding:utf-8
import json
import sys

import requests
from threading import Thread
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget


class UI_About(QWidget):
    def __init__(self, ver_idx = 20, ver_name="v1.20.0", url="https://github.wuyanzheshui.workers.dev/Wind2009-Louse/DuelEditor/raw/master/version.json", parent=None):
        self.last_version_idx = ver_idx
        self.parent = parent
        self.url = url

        super(UI_About, self).__init__()
        self.setWindowTitle("About")
        self.setFixedSize(313, 100)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(10, 10, 211, 21))
        self.label.setText('Duel Editor %s'%ver_name)
        self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(10, 30, 211, 21))
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setText('作者：虱子（<a href="https://github.com/Wind2009-Louse/DuelEditor/">项目地址</a>）')
        self.label_2.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(10, 60, 93, 28))
        self.pushButton.setText("检查更新")
        self.pushButton.clicked.connect(self.check_update)
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(110, 65, 211, 16))

    def check_update(self):
        self.label_3.setText("检查更新中……")
        QApplication.processEvents()
        self.update_thread = Update_Thread(self)
        self.update_thread.setDaemon(True)
        self.update_thread.start()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

class Update_Thread(Thread):
    def __init__(self, windows):
        self.windows = windows
        super().__init__()
    def run(self):
        try:
            json_result = json.loads(requests.get(self.windows.url, timeout=5).content.decode("utf-8", errors="ignore"))
            if json_result["version"] > self.windows.last_version_idx:
                self.windows.label_3.setText("当前有最新版本：%s"%json_result["name"])
                if self.windows.parent != None:
                    self.windows.parent.update_signal.emit(json_result["name"])
            elif json_result["version"] == self.windows.last_version_idx:
                self.windows.label_3.setText("当前已是最新版本")
            else:
                self.windows.label_3.setText("当前正在使用抢先版本")
        except Exception as e:
            print(e)
            self.windows.label_3.setText("检查更新失败")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = UI_About()

    m_window.show()
    sys.exit(app.exec_())
