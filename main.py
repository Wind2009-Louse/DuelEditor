#encoding:utf-8
import os
import sys
import webbrowser
import zipfile
from copy import deepcopy
from functools import partial
from json import dumps, loads
from re import sub
from sqlite3 import connect
from threading import Thread
from tempfile import mkdtemp
from shutil import rmtree

from PyQt5.QtCore import QRect, QRegExp, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QRegExpValidator, QFont
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QLabel, QLineEdit, QListWidget, QMainWindow,
                             QMenuBar, QMessageBox, QPushButton, QTextBrowser,
                             QWidget, QAbstractItemView)

import about
import calculator
import pic_window

idx_represent_str = ["己方手卡", "己方魔陷_1", "己方魔陷_2", "己方魔陷_3", "己方魔陷_4", "己方魔陷_5", "己方场地", "己方灵摆_1", "己方灵摆_2", "己方怪兽_1", "己方怪兽_2", "己方怪兽_3", "己方怪兽_4", "己方怪兽_5", "己方墓地", "己方除外", "己方额外", "对方手卡", "对方魔陷_1", "对方魔陷_2", "对方魔陷_3", "对方魔陷_4", "对方魔陷_5", "对方场地", "对方灵摆_1", "对方灵摆_2", "对方怪兽_1", "对方怪兽_2", "对方怪兽_3", "对方怪兽_4", "对方怪兽_5", "对方墓地", "对方除外", "对方额外", "额外怪兽区_1", "额外怪兽区_2"]
idx_represent_controller = {"己方": 1, "对方": -1, "额外怪兽区": 0}
cardcolors_dict = {0x2: QColor(10,128,0), 0x4: QColor(235,30,128), 0x10: QColor(168,168,0), 0x40: QColor(108,34,108), 0x80: QColor(16,128,235), 0x2000: QColor(168,168,168), 0x800000: QColor(0,0,0), 0x4000: QColor(98,98,98), 0x4000000: QColor(3,62,116), 0xffffffff: QColor(178,68,0)}
init_field = {"locations":{}, "desp":{}, "LP":[8000,8000], "fields":[]}
for t in range(len(idx_represent_str)):
    init_field["fields"].append([])
version_idx = 210
version_name = "v1.21.0"

default_mirror = "Github"
mirror_setting = {
    "Github":{
        "version": "https://github.com/Wind2009-Louse/DuelEditor/raw/master/version.json",
        "release": "https://github.com/Wind2009-Louse/DuelEditor/releases/download/"
    },
    "wuyanzheshui":{
        "version": "https://github.wuyanzheshui.workers.dev/Wind2009-Louse/DuelEditor/raw/master/version.json",
        "release": "https://github.wuyanzheshui.workers.dev/Wind2009-Louse/DuelEditor/releases/download/"
    },
    "cnpmjs": {
        "version": "https://github.com.cnpmjs.org/Wind2009-Louse/DuelEditor/raw/master/version.json",
        "release": "https://github.com.cnpmjs.org/Wind2009-Louse/DuelEditor/releases/download/"
    },
    "fastGit": {
        "version": "https://hub.fastgit.org/Wind2009-Louse/DuelEditor/raw/master/version.json",
        "release": "https://hub.fastgit.org/Wind2009-Louse/DuelEditor/releases/download/"
    },
    "ghproxy": {
        "version": "https://cdn.jsdelivr.net/gh/Wind2009-Louse/DuelEditor@master/version.json",
        "release": "https://mirror.ghproxy.com/https://github.com/Wind2009-Louse/DuelEditor/releases/download/"
    }
}

class Update_Thread(Thread):
    def __init__(self, window, url):
        self.window = window
        self.url = url
        super().__init__()
    def run(self):
        try:
            json_result = loads(about.requests.get(self.url, timeout=5).content.decode("utf-8", errors="ignore"))
            if json_result["version"] > version_idx:
                self.window.update_signal.emit(json_result["name"])
        except Exception as e:
            print(e)

class Download_Thread(Thread):
    def __init__(self, window, release_url, version_name=None):
        self.window = window
        self.url = release_url
        self.version_name = version_name
        super().__init__()
    def run(self):
        if self.version_name == None:
            return
        url = ""
        filename = ""
        if os.name == "nt":
            url = "%s%s/DuelEditor.exe"%(self.url, self.version_name)
            filename = "DuelEditor %s.exe"%self.version_name
        elif os.name == "posix":
            url = "%s%s/DuelEditor.out"%(self.url, self.version_name)
            filename = "DuelEditor %s.out"%self.version_name
        else:
            self.window.download_signal.emit("下载失败，找不到对应系统的版本！")
            return

        try:
            length = 0
            count = 0
            with about.requests.get(url, stream=True) as req:
                length = float(req.headers['Content-length'])
                with open(filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            count += len(chunk)
                            self.window.process_signal.emit("%.2f%%"%(count * 100 / length))
            self.window.process_signal.emit("")
            if count < length:
                self.window.download_signal.emit("下载失败，请重试！")
                os.remove(filename)
            else:
                self.window.download_signal.emit("下载成功！")
        except Exception as e:
            print(e)
            self.window.process_signal.emit("")
            self.window.download_signal.emit("下载失败！")
        finally:
            self.version_name = None

class Ui_MainWindow(QMainWindow):
    update_signal = pyqtSignal(str)
    download_signal = pyqtSignal(str)
    process_signal = pyqtSignal(str)
    clear_img_signal = pyqtSignal(str)
    normal_font = QFont()
    bold_font = QFont()
    bold_font.setBold(True)
    italic_font = QFont()
    italic_font.setItalic(True)
    bold_italic_font = QFont()
    bold_italic_font.setBold(True)
    bold_italic_font.setItalic(True)

    def placeframe(self):
        menu_height = self.menuBar().height()
        width = self.width()
        height = self.height() - menu_height
        # print(width, height)

        width_1_1 = 191 * width // self.origin_width
        height_1_1 = 143 * height // self.origin_height
        if height < self.origin_height:
            height_1_1 = 143 - (self.origin_height - height) // 2
        xline_1_1 = 10
        xline_1_2 = 10 + 200 * width // self.origin_width
        xline_1_3 = 10 + 400 * width // self.origin_width
        xline_1_4 = 10 + 600 * width // self.origin_width
        yline_1_1 = menu_height + 8
        yline_1_2 = menu_height + (self.origin_height - 10) * height // self.origin_height - height_1_1
        if height < self.origin_height:
            yline_1_2 = menu_height + (self.origin_height - 153) - (self.origin_height - height) // 2

        # enemy/self place
        self.label_enemy_ex.setGeometry(
            QRect(xline_1_1, yline_1_1, width_1_1, 20))
        self.Enemy_Ex.setGeometry(
            QRect(xline_1_1, yline_1_1+22, width_1_1, height_1_1 - 22))
        self.label_enemy_hand.setGeometry(
            QRect(xline_1_2, yline_1_1, width_1_1, 20))
        self.Enemy_Hand.setGeometry(
            QRect(xline_1_2, yline_1_1+22, width_1_1, height_1_1 - 22))
        self.label_enemy_grave.setGeometry(
            QRect(xline_1_3, yline_1_1, width_1_1, 20))
        self.Enemy_Grave.setGeometry(
            QRect(xline_1_3, yline_1_1+22, width_1_1, height_1_1 - 22))
        self.label_enemy_banish.setGeometry(
            QRect(xline_1_4, yline_1_1, width_1_1, 20))
        self.Enemy_Banish.setGeometry(
            QRect(xline_1_4, yline_1_1+22, width_1_1, height_1_1 - 22))
        self.label_self_ex.setGeometry(
            QRect(xline_1_1, yline_1_2, width_1_1, 20))
        self.Self_Ex.setGeometry(
            QRect(xline_1_1, yline_1_2+22, width_1_1, height_1_1 - 22))
        self.label_self_hand.setGeometry(
            QRect(xline_1_2, yline_1_2, width_1_1, 20))
        self.Self_Hand.setGeometry(
            QRect(xline_1_2, yline_1_2+22, width_1_1, height_1_1 - 22))
        self.label_self_grave.setGeometry(
            QRect(xline_1_3, yline_1_2, width_1_1, 20))
        self.Self_Grave.setGeometry(
            QRect(xline_1_3, yline_1_2+22, width_1_1, height_1_1 - 22))
        self.label_self_banish.setGeometry(
            QRect(xline_1_4, yline_1_2, width_1_1, 20))
        self.Self_Banish.setGeometry(
            QRect(xline_1_4, yline_1_2+22, width_1_1, height_1_1 - 22))

        # field
        width_2_0 = 110 * width // self.origin_width
        width_2_1 = width_2_0 + 1
        height_2_0 = (yline_1_2 - yline_1_1 - height_1_1 - 38) // 5
        height_2_1 = height_2_0 + 1
        xline_2_1 = 10
        xline_2_2 = 10 + 120 * width // self.origin_width
        xline_2_3 = 10 + 120 * width // self.origin_width + width_2_0
        xline_2_4 = 10 + 120 * width // self.origin_width + width_2_0 * 2
        xline_2_5 = 10 + 120 * width // self.origin_width + width_2_0 * 3
        xline_2_6 = 10 + 120 * width // self.origin_width + width_2_0 * 4
        xline_2_7 = 10 + 680 * width // self.origin_width
        yline_2_1 = yline_1_1 + height_1_1 + 30
        yline_2_2 = yline_2_1 + height_2_0
        yline_2_3 = yline_2_1 + height_2_0 * 2 # 280 * height / self.origin_height
        yline_2_4 = yline_2_1 + height_2_0 * 3 # 330 * height / self.origin_height
        yline_2_5 = yline_2_1 + height_2_0 * 4 # 380 * height / self.origin_height
        yline_2_6 = yline_2_1 + height_2_0 + 25 # 255 * height / self.origin_height
        yline_2_7 = yline_2_5 - height_2_0 - 25 # 305 * height / self.origin_height
        yline_2_8 = yline_2_5 - 45 # 335 * height / self.origin_height
        if height < self.origin_height:
            diff = (self.origin_height - height) // 2
            height_2_1 = 51
            yline_2_0 = 180 + menu_height
            yline_2_1 = yline_2_0 - diff
            yline_2_2 = yline_2_0 + 50 - diff
            yline_2_3 = yline_2_0 + 100 - diff
            yline_2_4 = yline_2_0 + 150 - diff
            yline_2_5 = yline_2_0 + 200 - diff
            yline_2_6 = yline_2_0 + 75 - diff
            yline_2_7 = yline_2_0 + 125 - diff
            yline_2_8 = yline_2_0 + 155 - diff
        self.Enemy_S1.setGeometry(QRect(xline_2_6, yline_2_1, width_2_1, height_2_1))
        self.Enemy_S2.setGeometry(QRect(xline_2_5, yline_2_1, width_2_1, height_2_1))
        self.Enemy_S3.setGeometry(QRect(xline_2_4, yline_2_1, width_2_1, height_2_1))
        self.Enemy_S4.setGeometry(QRect(xline_2_3, yline_2_1, width_2_1, height_2_1))
        self.Enemy_S5.setGeometry(QRect(xline_2_2, yline_2_1, width_2_1, height_2_1))
        self.Enemy_M1.setGeometry(QRect(xline_2_6, yline_2_2, width_2_1, height_2_1))
        self.Enemy_M2.setGeometry(QRect(xline_2_5, yline_2_2, width_2_1, height_2_1))
        self.Enemy_M3.setGeometry(QRect(xline_2_4, yline_2_2, width_2_1, height_2_1))
        self.Enemy_M4.setGeometry(QRect(xline_2_3, yline_2_2, width_2_1, height_2_1))
        self.Enemy_M5.setGeometry(QRect(xline_2_2, yline_2_2, width_2_1, height_2_1))
        self.label_enemy_field.setGeometry(QRect(xline_2_7, yline_2_6-22, width_2_1, 20))
        self.Enemy_Field.setGeometry(QRect(xline_2_7, yline_2_6, width_2_1, height_2_1))
        self.label_enemy_lpen.setGeometry(QRect(xline_2_7, yline_2_1-22, width_2_1, 20))
        self.Enemy_P1.setGeometry(QRect(xline_2_7, yline_2_1, width_2_1, height_2_1))
        self.label_enemy_rpen.setGeometry(QRect(xline_2_1, yline_2_1-22, width_2_1, 20))
        self.Enemy_P2.setGeometry(QRect(xline_2_1, yline_2_1, width_2_1, height_2_1))
        self.label_enemy_lp.setGeometry(QRect(xline_2_1, yline_2_6-22, width_2_1, 20))
        self.Enemy_LP.setGeometry(QRect(xline_2_1, yline_2_6, width_2_1, 21))
        # middle
        self.ExM_1.setGeometry(QRect(xline_2_3, yline_2_3, width_2_1, height_2_1))
        self.ExM_2.setGeometry(QRect(xline_2_5, yline_2_3, width_2_1, height_2_1))
        # self place
        self.Self_S1.setGeometry(QRect(xline_2_2, yline_2_5, width_2_1, height_2_1))
        self.Self_S2.setGeometry(QRect(xline_2_3, yline_2_5, width_2_1, height_2_1))
        self.Self_S3.setGeometry(QRect(xline_2_4, yline_2_5, width_2_1, height_2_1))
        self.Self_S4.setGeometry(QRect(xline_2_5, yline_2_5, width_2_1, height_2_1))
        self.Self_S5.setGeometry(QRect(xline_2_6, yline_2_5, width_2_1, height_2_1))
        self.Self_M1.setGeometry(QRect(xline_2_2, yline_2_4, width_2_1, height_2_1))
        self.Self_M2.setGeometry(QRect(xline_2_3, yline_2_4, width_2_1, height_2_1))
        self.Self_M3.setGeometry(QRect(xline_2_4, yline_2_4, width_2_1, height_2_1))
        self.Self_M4.setGeometry(QRect(xline_2_5, yline_2_4, width_2_1, height_2_1))
        self.Self_M5.setGeometry(QRect(xline_2_6, yline_2_4, width_2_1, height_2_1))
        self.label_self_lpen.setGeometry(QRect(xline_2_1, yline_2_5-22, width_2_1, 20))
        self.Self_P1.setGeometry(QRect(xline_2_1, yline_2_5, width_2_1, height_2_1))
        self.label_self_rpen.setGeometry(QRect(xline_2_7, yline_2_5-22, width_2_1, 20))
        self.Self_P2.setGeometry(QRect(xline_2_7, yline_2_5, width_2_1, height_2_1))
        self.label_self_field.setGeometry(QRect(xline_2_1, yline_2_7-22, width_2_1, 20))
        self.Self_Field.setGeometry(QRect(xline_2_1, yline_2_7, width_2_1, height_2_1))
        self.label_self_lp.setGeometry(QRect(xline_2_7, yline_2_8-22, width_2_1, 20))
        self.Self_LP.setGeometry(QRect(xline_2_7, yline_2_8, width_2_1, 21))

        # target/desc
        magic_3_1 = 85
        width_3_1 = 181 * width // self.origin_width
        height_3_1 = 200 * (height - magic_3_1) // (self.origin_height - magic_3_1)
        height_3_2 = height - 160 - height_3_1
        xline_3_1 = 810 * width // self.origin_width
        yline_3_1 = menu_height + height_3_1
        self.label_target_list.setGeometry(QRect(xline_3_1, menu_height, width_3_1, 20))
        self.Target_list.setGeometry(QRect(xline_3_1, menu_height + 20, width_3_1, height_3_1))
        self.Delete_target_button.setGeometry(QRect(xline_3_1, yline_3_1+25, width_3_1, 28))
        self.Dest_Box.setGeometry(QRect(xline_3_1, yline_3_1+63, width_3_1, 22))
        self.Move_card_button.setGeometry(QRect(xline_3_1, yline_3_1+90, width_3_1, 28))
        self.Erase_card_button.setGeometry(QRect(xline_3_1, yline_3_1+120, width_3_1, 28))
        self.Target_detail_browser.setGeometry(QRect(xline_3_1, yline_3_1+150, width_3_1, height_3_2 - 32))
        self.Target_effect_button.setGeometry(QRect(xline_3_1, yline_3_1 + 150 + height_3_2 - 30, (width_3_1 - 4) // 2, 28))
        self.Target_img_button.setGeometry(QRect(xline_3_1 + width_3_1 // 2 + 2, yline_3_1 + 150 + height_3_2 - 30, (width_3_1 - 4) // 2, 28))

        # search/operation buttoms
        width_4_1 = 181 * width // self.origin_width
        height_4_1 = height - 410
        xline_4_1 = 1000 * width // self.origin_width
        self.label_cardsearch.setGeometry(QRect(xline_4_1, menu_height, width_4_1, 20))
        self.NewCard_line.setGeometry(QRect(xline_4_1, menu_height + 20, width_4_1-42, 21))
        self.NewCard_button.setGeometry(QRect(xline_4_1+width_4_1-40, menu_height + 20, 40, 21))
        self.Newcard_List.setGeometry(QRect(xline_4_1, menu_height + 50, width_4_1, height_4_1))
        self.Create_card_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+55, width_4_1, 28))
        self.Rename_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+85, width_4_1, 28))
        self.Comment_Line.setGeometry(QRect(xline_4_1, menu_height + height_4_1+123, width_4_1, 21))
        self.Comment_card_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+150, width_4_1, 28))
        self.Comment_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+180, width_4_1, 28))
        self.LPTarget_Box.setGeometry(QRect(xline_4_1, menu_height + height_4_1+220, width_4_1, 22))
        self.LP_line.setGeometry(QRect(xline_4_1, menu_height + height_4_1+250, width_4_1, 21))
        self.AddLP_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+280, width_4_1, 28))
        self.DecLP_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+310, width_4_1, 28))
        self.CgeLP_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+340, width_4_1, 28))
        self.HalLP_button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+370, width_4_1, 28))

        # operation list
        width_5_1 = 181 * width // self.origin_width
        height_5_1 = 350 * height // self.origin_height
        height_5_2 = height - height_5_1 - 175
        xline_5_1 = 1190 * width // self.origin_width

        self.label_operation_list.setGeometry(QRect(xline_5_1, menu_height, width_5_1, 16))
        self.Operator_search.setGeometry(QRect(xline_5_1, menu_height + 20, width_5_1 - 23, 21))
        self.Operator_search_button.setGeometry(QRect(xline_5_1 + width_5_1 - 21, menu_height + 20, 21, 21))
        self.Operator_list.setGeometry(QRect(xline_5_1, menu_height + 50, width_5_1, height_5_1 - 20))
        self.Delete_ope_button.setGeometry(QRect(xline_5_1, menu_height + height_5_1+35, width_5_1, 28))
        self.CopyingOpe_list.setGeometry(QRect(xline_5_1, menu_height + height_5_1+70, width_5_1, height_5_2))
        self.Copy_ope_button.setGeometry(QRect(xline_5_1, menu_height + height_5_1+height_5_2+75, width_5_1, 28))
        self.Paste_ope_button.setGeometry(QRect(xline_5_1, menu_height + height_5_1+height_5_2+105, width_5_1, 28))
        self.Delete_copy_button.setGeometry(QRect(xline_5_1, menu_height + height_5_1+height_5_2+135, width_5_1, 28))

    def init_frame(self):
        '''初始化UI'''
        self.origin_width = 1380
        self.origin_height = 590
        self.mini_width = 960
        self.mini_height = 540
        self.setMinimumSize(self.mini_width, self.mini_height + self.menuBar().height())
        self.centralwidget = QWidget(self)

        # for small screen
        self.desktop = QApplication.desktop()
        self.screen = self.desktop.screenGeometry()
        if self.screen.width() < 1380:
            self.resize(self.mini_width, self.mini_height + self.menuBar().height())
        else:
            self.resize(self.origin_width, self.origin_height + self.menuBar().height())

        '''初始化label'''
        self.label_target_list = QLabel(self.centralwidget)
        self.label_target_list.setAlignment(Qt.AlignCenter)
        self.label_cardsearch = QLabel(self.centralwidget)
        self.label_cardsearch.setAlignment(Qt.AlignCenter)
        self.label_operation_list = QLabel(self.centralwidget)
        self.label_operation_list.setAlignment(Qt.AlignCenter)

        self.label_self_ex = QLabel(self.centralwidget)
        self.label_self_ex.setAlignment(Qt.AlignCenter)
        self.label_self_hand = QLabel(self.centralwidget)
        self.label_self_hand.setAlignment(Qt.AlignCenter)
        self.label_self_grave = QLabel(self.centralwidget)
        self.label_self_grave.setAlignment(Qt.AlignCenter)
        self.label_self_banish = QLabel(self.centralwidget)
        self.label_self_banish.setAlignment(Qt.AlignCenter)
        self.label_self_lpen = QLabel(self.centralwidget)
        self.label_self_lpen.setAlignment(Qt.AlignCenter)
        self.label_self_rpen = QLabel(self.centralwidget)
        self.label_self_rpen.setAlignment(Qt.AlignCenter)
        self.label_self_field = QLabel(self.centralwidget)
        self.label_self_field.setAlignment(Qt.AlignCenter)
        self.label_self_lp = QLabel(self.centralwidget)
        self.label_self_lp.setAlignment(Qt.AlignCenter)

        self.label_enemy_ex = QLabel(self.centralwidget)
        self.label_enemy_ex.setAlignment(Qt.AlignCenter)
        self.label_enemy_hand = QLabel(self.centralwidget)
        self.label_enemy_hand.setAlignment(Qt.AlignCenter)
        self.label_enemy_grave = QLabel(self.centralwidget)
        self.label_enemy_grave.setAlignment(Qt.AlignCenter)
        self.label_enemy_banish = QLabel(self.centralwidget)
        self.label_enemy_banish.setAlignment(Qt.AlignCenter)
        self.label_enemy_lpen = QLabel(self.centralwidget)
        self.label_enemy_lpen.setAlignment(Qt.AlignCenter)
        self.label_enemy_rpen = QLabel(self.centralwidget)
        self.label_enemy_rpen.setAlignment(Qt.AlignCenter)
        self.label_enemy_field = QLabel(self.centralwidget)
        self.label_enemy_field.setAlignment(Qt.AlignCenter)
        self.label_enemy_lp = QLabel(self.centralwidget)
        self.label_enemy_lp.setAlignment(Qt.AlignCenter)

        self.Target_list = QListWidget(self.centralwidget)
        self.Delete_target_button = QPushButton(self.centralwidget)
        self.Dest_Box = QComboBox(self.centralwidget)
        for i in range(36):
            self.Dest_Box.addItem("")
        self.Move_card_button = QPushButton(self.centralwidget)
        self.Erase_card_button = QPushButton(self.centralwidget)
        self.Target_detail_browser = QTextBrowser(self.centralwidget)
        self.Target_detail_browser.setOpenExternalLinks(True)
        self.Target_detail_browser.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.Target_effect_button = QPushButton(self.centralwidget)
        self.Target_img_button = QPushButton(self.centralwidget)
        self.Target_img_button.setFocusPolicy(Qt.NoFocus)

        self.NewCard_line = QLineEdit(self.centralwidget)
        self.NewCard_line.setPlaceholderText("输入卡片名称")
        self.NewCard_button = QPushButton(self.centralwidget)
        self.Newcard_List = QListWidget(self.centralwidget)
        self.Create_card_button = QPushButton(self.centralwidget)
        self.Rename_button = QPushButton(self.centralwidget)
        self.Rename_button.setEnabled(False)
        self.Rename_button.setFocusPolicy(Qt.NoFocus)
        self.Comment_Line = QLineEdit(self.centralwidget)
        self.Comment_Line.setPlaceholderText("输入注释")
        self.Comment_card_button = QPushButton(self.centralwidget)
        self.Comment_button = QPushButton(self.centralwidget)
        self.LPTarget_Box = QComboBox(self.centralwidget)
        self.LPTarget_Box.addItem("")
        self.LPTarget_Box.addItem("")
        self.LP_line = QLineEdit(self.centralwidget)
        regx = QRegExp("^[0-9]{15}$")
        validator = QRegExpValidator(regx, self.LP_line)
        self.LP_line.setValidator(validator)
        self.LP_line.setPlaceholderText("输入基本分变动")
        self.AddLP_button = QPushButton(self.centralwidget)
        self.DecLP_button = QPushButton(self.centralwidget)
        self.CgeLP_button = QPushButton(self.centralwidget)
        self.HalLP_button = QPushButton(self.centralwidget)

        self.Operator_list = QListWidget(self.centralwidget)
        self.Operator_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.Operator_search = QLineEdit(self.centralwidget)
        self.Operator_search.setPlaceholderText("输入操作内容搜索")
        self.Operator_search_button = QPushButton(self.centralwidget)
        self.Delete_ope_button = QPushButton(self.centralwidget)
        self.CopyingOpe_list = QListWidget(self.centralwidget)
        self.CopyingOpe_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.Copy_ope_button = QPushButton(self.centralwidget)
        self.Paste_ope_button = QPushButton(self.centralwidget)
        self.Delete_copy_button = QPushButton(self.centralwidget)

        self.Self_Ex = QListWidget(self.centralwidget)
        self.Self_Hand = QListWidget(self.centralwidget)
        self.Self_Grave = QListWidget(self.centralwidget)
        self.Self_Banish = QListWidget(self.centralwidget)
        self.Self_S1 = QListWidget(self.centralwidget)
        self.Self_S2 = QListWidget(self.centralwidget)
        self.Self_S3 = QListWidget(self.centralwidget)
        self.Self_S4 = QListWidget(self.centralwidget)
        self.Self_S5 = QListWidget(self.centralwidget)
        self.Self_M1 = QListWidget(self.centralwidget)
        self.Self_M2 = QListWidget(self.centralwidget)
        self.Self_M3 = QListWidget(self.centralwidget)
        self.Self_M4 = QListWidget(self.centralwidget)
        self.Self_M5 = QListWidget(self.centralwidget)
        self.Self_P1 = QListWidget(self.centralwidget)
        self.Self_P2 = QListWidget(self.centralwidget)
        self.Self_Field = QListWidget(self.centralwidget)
        self.Self_LP = QLineEdit(self.centralwidget)
        self.Self_LP.setText("8000")
        self.Self_LP.setEnabled(False)

        self.ExM_1 = QListWidget(self.centralwidget)
        self.ExM_2 = QListWidget(self.centralwidget)

        self.Enemy_Ex = QListWidget(self.centralwidget)
        self.Enemy_Hand = QListWidget(self.centralwidget)
        self.Enemy_Grave = QListWidget(self.centralwidget)
        self.Enemy_Banish = QListWidget(self.centralwidget)
        self.Enemy_S1 = QListWidget(self.centralwidget)
        self.Enemy_S2 = QListWidget(self.centralwidget)
        self.Enemy_S3 = QListWidget(self.centralwidget)
        self.Enemy_S4 = QListWidget(self.centralwidget)
        self.Enemy_S5 = QListWidget(self.centralwidget)
        self.Enemy_M1 = QListWidget(self.centralwidget)
        self.Enemy_M2 = QListWidget(self.centralwidget)
        self.Enemy_M3 = QListWidget(self.centralwidget)
        self.Enemy_M4 = QListWidget(self.centralwidget)
        self.Enemy_M5 = QListWidget(self.centralwidget)
        self.Enemy_Field = QListWidget(self.centralwidget)
        self.Enemy_P1 = QListWidget(self.centralwidget)
        self.Enemy_P2 = QListWidget(self.centralwidget)
        self.Enemy_LP = QLineEdit(self.centralwidget)
        self.Enemy_LP.setText("8000")
        self.Enemy_LP.setEnabled(False)
        self.placeframe()

        self.retranslateUi()

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.init_frame()

        # bar init
        bar = QMenuBar(self)
        self.setMenuBar(bar)
        self.new_bar = QAction("新建(&N)",self)
        self.new_bar.setShortcut("Ctrl+N")
        self.new_bar.triggered.connect(self.newfile)
        bar.addAction(self.new_bar)
        self.open_bar = QAction("打开(&O)",self)
        self.open_bar.setShortcut("Ctrl+O")
        self.open_bar.triggered.connect(self.save_and_open_file)
        bar.addAction(self.open_bar)
        self.recent_bar_list = bar.addMenu("打开…")
        self.recent_bar_list.triggered[QAction].connect(self.open_recent_file)
        self.save_bar = QAction("保存(&S)",self)
        self.save_bar.setShortcut("Ctrl+S")
        self.save_bar.triggered.connect(self.savefile)
        bar.addAction(self.save_bar)

        self.mirror_bar_init(bar)

        self.menu_bar_list = bar.addMenu("功能…")
        self.calculator_bar = QAction("计算器",self)
        self.calculator_bar.triggered.connect(self.open_calculator)
        self.menu_bar_list.addAction(self.calculator_bar)
        self.export_deck_bar = QAction("导出卡组",self)
        self.export_deck_bar.triggered.connect(self.export_deck)
        self.menu_bar_list.addAction(self.export_deck_bar)
        self.blur_search_bar = QAction("搜索效果文字",self,checkable=True)
        self.blur_search_bar.setChecked(True)
        self.blur_search_bar.triggered.connect(self.search_card)
        self.menu_bar_list.addAction(self.blur_search_bar)
        self.coloring_field_card = QAction("按照卡片种类显示颜色",self,checkable=True)
        self.coloring_field_card.setChecked(False)
        self.coloring_field_card.triggered.connect(self.refresh_color)
        self.menu_bar_list.addAction(self.coloring_field_card)

        self.about_bar = QAction("关于", self)
        self.about_bar.triggered.connect(self.open_about)
        bar.addAction(self.about_bar)
        self.quit_bar = QAction("退出", self)
        self.quit_bar.triggered.connect(self.close)
        bar.addAction(self.quit_bar)

        self.read_config()
        self.img_window_list = []

        # 读取卡片数据库
        self.card_datas = {}
        self.raw_datas = {}
        self.monster_datas = {}
        self.card_colors = {}
        self.id_map_by_name = {}
        self.ex_card_id_set = set()
        self.token_card_id_set = set()
        card_sorted = {}

        # 读取Pro1默认cdb
        if os.path.exists("cards.cdb"):
            self.read_cdb("cards.cdb", card_sorted)
        # 读取Pro1扩展包
        self.read_cdbs_from_dir("expansions", card_sorted)
        # 读取Pro2的cdb目录
        self.read_cdbs_from_dir("cdb", card_sorted)
        # Windows系统下，读取注册表中Pro2的安装目录
        if os.name == "nt":
            import winreg
            try:
                pro2_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths\YGOPro2.exe", access=winreg.KEY_READ)
                if pro2_key:
                    pro2_path = winreg.QueryValueEx(pro2_key, "path")
                    if len(pro2_path) > 0:
                        self.read_cdbs_from_dir(pro2_path[0], card_sorted)
            except Exception as e:
                pass
            try:
                pro2_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\YGOPro2.exe", access=winreg.KEY_READ)
                if pro2_key:
                    pro2_path = winreg.QueryValueEx(pro2_key, "path")
                    if len(pro2_path) > 0:
                        self.read_cdbs_from_dir(pro2_path[0], card_sorted)
            except Exception as e:
                pass
        
        self.card_names = list(self.card_datas.keys())
        self.card_names.sort(key=lambda x: (card_sorted[x]))
        if len(self.card_names) <= 0:
            self.Newcard_List.addItem("无数据库")
            self.Newcard_List.setEnabled(False)
            self.coloring_field_card.setEnabled(False)
        
        # sub windows
        self.calculate_window = calculator.Calculator()
        self.calculate_window.setdatas(self.monster_datas)
        self.about_window = about.UI_About(version_idx, version_name, self.version_url, self)

        # 初始化
        self.idx_represent_field = [
            self.Self_Hand, self.Self_S1, self.Self_S2, self.Self_S3, self.Self_S4, self.Self_S5,
            self.Self_Field, self.Self_P1, self.Self_P2, self.Self_M1, self.Self_M2, self.Self_M3, self.Self_M4, self.Self_M5,
            self.Self_Grave, self.Self_Banish, self.Self_Ex,
            self.Enemy_Hand, self.Enemy_S1, self.Enemy_S2, self.Enemy_S3, self.Enemy_S4, self.Enemy_S5,
            self.Enemy_Field, self.Enemy_P1, self.Enemy_P2, self.Enemy_M1, self.Enemy_M2, self.Enemy_M3, self.Enemy_M4, self.Enemy_M5,
            self.Enemy_Grave, self.Enemy_Banish, self.Enemy_Ex, self.ExM_1, self.ExM_2
        ]
        self.unsave_changed = False

        # 操作部分
        self.copying_operation = []
        self.Operator_search.textChanged.connect(self.search_operation)
        self.Operator_search.returnPressed.connect(self.search_operation_cycle)
        self.Operator_search_button.clicked.connect(self.search_operation_cycle)
        self.Operator_list.itemSelectionChanged.connect(self.operation_index_changed)
        self.Delete_ope_button.clicked.connect(self.remove_operator)
        self.Operator_list.doubleClicked.connect(self.copy_ope)
        self.Copy_ope_button.clicked.connect(self.copy_ope)
        self.CopyingOpe_list.itemSelectionChanged.connect(self.select_copying)
        self.CopyingOpe_list.doubleClicked.connect(self.remove_from_copying)
        self.Paste_ope_button.clicked.connect(self.paste_operator)
        self.Delete_copy_button.clicked.connect(self.remove_from_copying)

        # 判断是否有最近打开的文件，若有则尝试打开
        if self.fullfilename is not None and len(self.fullfilename) > 0:
            fullname = self.fullfilename
            temp_id = self.lastest_field_id
            self.newfile()
            try:
                self.openfile(fullname, temp_id)
            except Exception as e:
                self.fullfilename = ""
        else:
            self.newfile()

        # 对象部分
        self.Delete_target_button.clicked.connect(self.remove_from_targets)
        self.Target_list.clicked.connect(self.target_index_changed)
        self.Target_list.itemSelectionChanged.connect(self.target_index_changed)
        self.Target_list.doubleClicked.connect(self.remove_from_targets)
        self.Target_effect_button.clicked.connect(self.show_card_effect)
        self.Target_img_button.clicked.connect(self.view_pic)
        self.Move_card_button.clicked.connect(self.ope_movecards)

        # 添加/删除卡片部分
        self.NewCard_line.textChanged.connect(self.search_card)
        self.NewCard_line.returnPressed.connect(self.create_card)
        self.NewCard_button.clicked.connect(self.create_card)
        self.Newcard_List.doubleClicked.connect(self.fix_cardname)
        self.Newcard_List.clicked.connect(self.show_carddesp)
        self.Newcard_List.itemSelectionChanged.connect(self.show_carddesp)
        self.Rename_button.clicked.connect(self.card_rename)
        self.Create_card_button.clicked.connect(self.create_card)
        self.Erase_card_button.clicked.connect(self.erase_targets)

        # 基本分变更部分
        self.AddLP_button.clicked.connect(self.ope_LPAdd)
        self.DecLP_button.clicked.connect(self.ope_LPDec)
        self.CgeLP_button.clicked.connect(self.ope_LPCge)
        self.HalLP_button.clicked.connect(self.ope_LPHal)

        # 注释部分
        self.Comment_button.clicked.connect(self.ope_addcomment)
        self.Comment_card_button.clicked.connect(self.ope_addcarddesp)
        self.Comment_Line.returnPressed.connect(self.comment_enter)

        # 场上的卡片
        for field_id in range(len(self.idx_represent_field)):
            self.idx_represent_field[field_id].itemSelectionChanged.connect(partial(self.select_field, field_id))
            self.idx_represent_field[field_id].clicked.connect(partial(self.select_field, field_id))
            self.idx_represent_field[field_id].doubleClicked.connect(partial(self.target_field, field_id))

        self.update_signal.connect(self.update_hint)
        self.download_signal.connect(self.download_hint)
        self.process_signal.connect(self.process_hint)
        self.clear_img_signal.connect(self.img_cache_clear)
        self.update_check()
    
    def update_check(self):
        self.update_thread = Update_Thread(self, self.version_url)
        self.update_thread.setDaemon(True)
        self.update_thread.start()

    def keyPressEvent(self, event):
        '''键盘事件响应'''
        if event.key() == Qt.Key_Delete:
            # Delete键删除目标
            if self.Target_list.hasFocus():
                self.remove_from_targets()
            # Delete键删除操作
            elif self.Operator_list.hasFocus():
                self.remove_operator()
            elif self.CopyingOpe_list.hasFocus():
                self.remove_from_copying()
        # 回车键默认减少LP
        if self.LP_line.hasFocus() and (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter):
            self.ope_LPDec()
        # 其它事件
        QWidget.keyPressEvent(self, event)

    def resizeEvent(self, event):
        self.centralwidget.resize(self.width(), self.height())
        self.placeframe()

    def closeEvent(self, event):
        '''重写关闭窗口事件
        
        用于退出前确认保存更改'''
        if self.unsave_confirm():
            event.ignore()
        else:
            self.calculate_window.close()
            self.about_window.close()
            self.save_config()
            event.accept()

    def comment_enter(self):
        '''在注释栏回车时触发的事件
        
        根据目标数量确定为为卡片添加注释，或是添加操作备注'''
        if len(self.targets) > 0:
            self.ope_addcarddesp()
        else:
            self.ope_addcomment()

    def retranslateUi(self):
        self.setWindowTitle("DuelEditor")
        self.Operator_list.setSortingEnabled(False)
        self.label_operation_list.setText("操作列表(0/0)")
        self.label_target_list.setText("操作对象(0)")
        self.Delete_target_button.setText("对象中删除")
        self.Create_card_button.setText("←添加到对象")
        self.Move_card_button.setText("移动对象")
        self.Comment_card_button.setText("对象注释")
        self.Comment_button.setText("操作注释")
        self.label_self_ex.setText("己方额外(0)")
        self.label_self_hand.setText("己方手卡(0)")
        self.label_self_rpen.setText("己方右灵摆")
        self.label_self_lpen.setText("己方左灵摆")
        self.label_self_field.setText("己方场地")
        self.label_self_lp.setText("己方基本分")
        self.label_self_grave.setText("己方墓地(0)")
        self.label_self_banish.setText("己方除外(0)")
        self.label_enemy_rpen.setText("对方右灵摆")
        self.label_enemy_field.setText("对方场地")
        self.label_enemy_lpen.setText("对方左灵摆")
        self.label_enemy_lp.setText("对方基本分")
        self.label_enemy_grave.setText("对方墓地(0)")
        self.label_enemy_hand.setText("对方手卡(0)")
        self.label_enemy_ex.setText("对方额外(0)")
        self.label_enemy_banish.setText("对方除外(0)")
        self.Erase_card_button.setText("移除对象")
        for idx in range(len(idx_represent_str)):
            self.Dest_Box.setItemText(idx, idx_represent_str[idx])
        self.label_cardsearch.setText("卡片搜索(0)")
        self.Delete_ope_button.setText("删除操作")
        self.Copy_ope_button.setText("复制操作")
        self.Paste_ope_button.setText("粘贴操作")
        self.Delete_copy_button.setText("从剪切板删除")
        self.LPTarget_Box.setItemText(0, "己方")
        self.LPTarget_Box.setItemText(1, "对方")
        self.AddLP_button.setText("增加基本分")
        self.DecLP_button.setText("减少基本分")
        self.CgeLP_button.setText("变成基本分")
        self.HalLP_button.setText("基本分减半")
        self.Rename_button.setText("未选定卡")
        self.NewCard_button.setText("添加")
        self.Target_effect_button.setText("效果")
        self.Target_img_button.setText("卡图")
        self.Operator_search_button.setText("↓")

    def maketitle(self, process=""):
        '''根据当前正在打开的文件修改窗口标题'''
        if process is not None and process != "":
            title_name = "(%s)DuelEditor - %s"%(process, self.filename)
        else:
            title_name = "DuelEditor - %s"%self.filename
        if self.unsave_changed:
            title_name = "*" + title_name
        self.setWindowTitle(title_name)

    def newfile(self):
        if self.unsave_confirm():
            return
        self.lastest_field_id = -1
        self.operators = {"cardindex":0, "cards":{}, "operations":[]}
        self.fields = {0:deepcopy(init_field)}
        self.targets = []
        self.copying_operation = []
        self.filename = "Untitle.json"
        self.fullfilename = ""
        self.last_text = ""
        self.showing_card_id = None
        self.unsave_changed = False

        self.maketitle()
        self.update_rename_buttom()
        self.update_operationlist()
        self.update_copying()
        self.refresh_field()
        self.update_targetlist()
        self.show_cardinfo()
        self.search_card()

    def openfile(self, fullname=None, idx=None):
        '''打开文件'''
        show_error = (fullname == None)
        if self.unsave_confirm():
            return
        if not isinstance(fullname, str):
            fullname = str(QFileDialog.getOpenFileName(self, '选择打开的文件', self.fullfilename, filter="*.json")[0])
        if len(fullname) == 0:
            return
        if idx is None:
            idx = self.get_recent_index(fullname)
        origin_data = deepcopy(self.operators)
        try:
            with open(fullname,'r',encoding='utf-8') as f:
                json_data = f.read()
                dict_data = loads(json_data)
                self.operators = dict_data
                self.make_fields()
                self.update_operationlist()
                ope_idx = len(self.operators["operations"])-1
                if idx is not None:
                    ope_idx = min(idx, ope_idx)
                self.Operator_list.setCurrentRow(ope_idx)
                self.filename = os.path.split(fullname)[-1]
                self.fullfilename = fullname
                self.unsave_changed = False
                self.maketitle()
                self.update_recent(fullname, self.get_current_operation_index())
                return
        # 出错时尝试不使用utf-8编码打开文件
        except Exception as e:
            try:
                with open(fullname,'r') as f:
                    json_data = f.read()
                    dict_data = loads(json_data)
                    self.operators = dict_data
                    self.make_fields()
                    self.update_operationlist()
                    ope_idx = len(self.operators["operations"])-1
                    if idx is not None:
                        ope_idx = min(idx, ope_idx)
                    self.Operator_list.setCurrentRow(ope_idx)
                    self.filename = os.path.split(fullname)[-1]
                    self.fullfilename = fullname
                    self.unsave_changed = False
                    self.maketitle()
                    self.update_recent(fullname, self.get_current_operation_index())
                    return
            except:
                pass
        self.operators = origin_data
        self.make_fields()
        self.update_recent(fullname, -2)
        if show_error:
            QMessageBox.warning(self, "提示", "打开失败！", QMessageBox.Yes)

    def unsave_confirm(self):
        '''如果取消动作，则返回True，否则返回False'''
        if self.unsave_changed:
            reply = QMessageBox.warning(self, '保存', "是否保存当前文件'%s'？"%self.filename, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.savefile()
            elif reply == QMessageBox.No:
                self.unsave_changed = False
        return self.unsave_changed
    
    def savefile(self):
        '''保存文件'''
        fullname = str(QFileDialog.getSaveFileName(self,'保存为', self.fullfilename,"*.json")[0])
        if len(fullname) == 0:
            return
        self.filename = os.path.split(fullname)[-1]
        self.fullfilename = fullname
        json_data = dumps(self.operators,indent=2,ensure_ascii=False)
        with open(fullname,'w',encoding='utf-8') as f:
            f.write(json_data)
            QMessageBox.warning(self, "提示", "保存成功！", QMessageBox.Yes)
            self.unsave_changed = False
            self.maketitle()
        self.update_recent(fullname, self.get_current_operation_index())

    def make_fields(self, begin_at=0, end_at=None):
        '''根据操作生成各操作的场地
        
        若begin_at不大于0，则从初始场地开始生成，否则从第begin_at个动作后开始生成场地'''
        # 获取场地
        if begin_at <= 0:
            begin_at = 0
            self.fields.clear()
            lastest_field = deepcopy(init_field)
        else:
            lastest_field = deepcopy(self.fields[min(begin_at-1, len(self.fields) - 1)])
        # 遍历操作
        if end_at is None:
            end_at = len(self.operators["operations"])
        else:
            end_at = min(len(self.operators["operations"]), end_at+1)
        for idx in range(begin_at, end_at):
            '''type(str), args(list of int), dest(int), desp(str)'''
            operation = self.operators["operations"][idx]
            if operation["type"] == "move":
                for card_idx in operation["args"]:
                    lastest_field["locations"][card_idx] = operation["dest"]
            elif operation["type"] == "carddesp":
                for card_idx in operation["args"]:
                    lastest_field["desp"][card_idx] = operation["desp"]
            elif operation["type"] == "erase":
                for card_idx in operation["args"]:
                    if card_idx in lastest_field["locations"]:
                        lastest_field["locations"].pop(card_idx)
            elif operation["type"] == "LPAdd":
                lastest_field["LP"][operation["args"][0]] += operation["args"][1]
            elif operation["type"] == "LPDec":
                lastest_field["LP"][operation["args"][0]] -= operation["args"][1]
            elif operation["type"] == "LPCge":
                lastest_field["LP"][operation["args"][0]] = operation["args"][1]
            elif operation["type"] == "LPHal":
                lastest_field["LP"][operation["args"][0]] = (lastest_field["LP"][operation["args"][0]] + 1) // 2
            # 卡片移动时，对场地列表进行更新
            if operation["type"] in ["move","erase"]:
                for card_idx in operation["args"]:
                    if idx > 0 and card_idx in self.fields[idx-1]["locations"]:
                        last_locat = self.fields[idx-1]["locations"][card_idx]
                        lastest_field["fields"][last_locat].remove(card_idx)
                    if operation["type"] == "move":
                        lastest_field["fields"][operation["dest"]].append(card_idx)

            # 将场地复制到列表中用以读取
            self.fields[idx] = deepcopy(lastest_field)
        # 没有操作会导致没有场地被放置到列表中，用以作为初始场地
        if len(self.fields) == 0:
            self.fields[0] = lastest_field

    def get_last_location(self, card_id, ope_id):
        '''获取指定卡片在上一个操作中的位置'''
        if ope_id <= 0:
            return "未知"
        field = self.fields[ope_id-1]
        if card_id in field["locations"]:
            return idx_represent_str[field["locations"][card_id]]
        else:
            return "未知"

    def get_current_field(self):
        '''获取当前操作对应的场地信息

        场地格式：

        locations(dict), desp(dict), LP(list), fields(list of list)'''
        ope_id = self.get_current_operation_index()
        if ope_id < 0:
            ope_id = 0
        return self.fields[ope_id]

    def insert_operation(self, operation, update=True):
        '''插入操作。操作格式：\n\ntype(str), args(list of int), dest(int), desp(str)'''
        # 判断是插入或新增
        ope_id = self.get_current_operation_index()
        self.lastest_field_id = ope_id
        if ope_id < 0:
            self.operators["operations"].append(operation)
            ope_id = 0
        else:
            ope_id += 1
            self.operators["operations"].insert(ope_id, operation)
        if update:
            # self.make_fields(ope_id)
            self.make_fields(self.lastest_field_id, ope_id)
            self.lastest_field_id = ope_id
            self.update_operationlist()
            self.Operator_list.setCurrentRow(ope_id)
            self.show_opeinfo()
            self.unsave_changed = True
            self.maketitle()
            self.label_target_list.setText("操作对象(%d)"%len(self.targets))
            #self.Operator_list.setFocus()

    def show_cardinfo(self, card_id=None):
        '''根据card_id，在信息栏显示卡片详情'''
        # 清空
        if card_id is None:
            self.Target_detail_browser.document().clear()
            self.Target_detail_browser.setText("")
            return
        if card_id not in self.operators["cards"]:
            return
        card_name = self.operators["cards"][card_id]["Name"]

        self.showing_card_id = card_id
        self.update_rename_buttom()
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            if self.show_card_effect():
                return

        field = self.get_current_field()
        card_locat = "未知"
        card_desp = "无"
        if card_id in field["locations"]:
            card_locat = idx_represent_str[field["locations"][card_id]]
        if card_id in field["desp"]:
            card_desp = field["desp"][card_id]
        result = "[%s]\n位置：%s\n备注：%s"%(card_name, card_locat, card_desp)
        self.Target_detail_browser.document().clear()
        self.Target_detail_browser.setText(result)
    
    def show_card_effect(self):
        '''显示卡片的效果'''
        if self.showing_card_id is None:
            return False
        if self.showing_card_id not in self.operators["cards"]:
            return False
        card_name = self.operators["cards"][self.showing_card_id]["Name"]

        search_list = [card_name, card_name[:-1]]
        for name in search_list:
            if name in self.card_datas:
                text = self.card_datas[name]
                self.Target_detail_browser.setHtml(text)
                return True
        
        return False
    
    def show_opeinfo(self, idx=None):
        '''显示指定操作详情\n\nidx为空时，显示选定操作的详情'''
        # 获取操作
        self.showing_card_id = None
        self.update_rename_buttom()
        if idx is None:
            idx = self.get_current_operation_index()
            if idx < 0:
                return
        operation = self.operators["operations"][idx]

        result = ""
        if operation["type"] == "move":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、\n"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
        elif operation["type"] == "carddesp":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、\n"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s %s"%(card_name, operation["desp"])
        elif operation["type"] == "erase":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、\n"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s 被移除"%(card_name)
        elif operation["type"][0:2] == "LP":
            if operation['args'][0]==0:
                target = "己方"
            else:
                target = "对方"
            actions = {"Add":"增加","Dec":"降低","Cge":"变成","Hal":"减半"}
            subope = operation["type"][2:]
            action = actions[subope]
            point = ""
            if action != "减半":
                point = "%d"%operation['args'][1]
            result = "%sLP%s%s"%(target,action,point)
        elif operation["type"] == "comment":
            result = operation["desp"]
        self.Target_detail_browser.document().clear()
        self.Target_detail_browser.setText(result)

    def create_card(self):
        '''新增卡片'''
        cardname = self.NewCard_line.text()
        self.NewCard_line.setText("")
        if cardname == "":
            return
        # 获取当前卡片idx，通过+1来作为新卡片的idx
        idx = str(self.operators["cardindex"])
        self.operators["cardindex"] += 1
        self.operators["cards"][idx] = {"Name": cardname}
        self.targets.append(idx)
        self.label_target_list.setText("操作对象(%d)"%len(self.targets))
        self.update_targetlist()

    def remove_from_targets(self):
        '''从操作对象中移除卡片'''
        target_idx = self.Target_list.selectedIndexes()
        # 如果没有选定卡片，则结束
        if len(target_idx) == 0:
            return
        target_idx = target_idx[0].row()
        del self.targets[target_idx]
        # 刷新
        self.clear_unuse_cards()
        self.label_target_list.setText("操作对象(%d)"%len(self.targets))
        self.Target_detail_browser.clear()
        self.update_targetlist()
        self.showing_card_id = None
        self.update_rename_buttom()

    def remove_operator(self):
        '''移除操作'''
        # 从操作列表中获得当前选定的操作
        selected = self.Operator_list.selectedIndexes()
        if len(selected) <= 0:
            return
        # 确认提示
        reply = QMessageBox.information(self, 'Confirm', "确认要从操作列表中删除选定操作吗？该操作不可逆。", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        idx_list = [item.row() for item in selected]
        idx_list.sort(reverse=True)
        self.unsave_changed = True
        self.maketitle()
        for idx in idx_list:
            del self.operators["operations"][idx]
        self.clear_unuse_cards()
        # self.make_fields(idx)
        self.lastest_field_id = idx - 1
        self.update_operationlist()
        if len(self.operators["operations"]) > 0 and idx == 0:
            self.Operator_list.setCurrentRow(0)
        else:
            self.Operator_list.setCurrentRow(idx-1)
        self.show_opeinfo()

    def paste_operator(self):
        '''粘贴操作'''
        sel_idx_list = self.CopyingOpe_list.selectedIndexes()
        idx_list = []
        for sel_idx in sel_idx_list:
            idx_list.append(sel_idx.row())
        if len(idx_list) <= 0:
            if len(self.copying_operation) == 1:
                idx_list.append(0)
            else:
                return
        idx_list.reverse()
        for idx in idx_list:
            operation = self.copying_operation[idx]
            self.insert_operation(operation, idx == idx_list[len(idx_list)-1])
        self.remove_from_copying(False)
        self.update_copying()

    def copy_ope(self):
        '''复制操作'''
        # 多项复制
        idx_list = self.Operator_list.selectedIndexes()
        if len(idx_list) < 1:
            return
        for item in idx_list:
            idx = item.row()
            ope = deepcopy(self.operators["operations"][idx])
            self.copying_operation.append(ope)
        self.update_copying()
    
    def update_copying(self):
        '''描绘复制列表中的操作'''
        self.CopyingOpe_list.clear()
        operation_list = self.copying_operation
        # 判断当前是否有复制中的操作
        if len(self.copying_operation) <= 0:
            self.Paste_ope_button.setEnabled(False)
            self.CopyingOpe_list.addItem("无操作")
            self.CopyingOpe_list.setEnabled(False)
            return
        self.Paste_ope_button.setEnabled(True)
        self.CopyingOpe_list.setEnabled(True)
        for operation in operation_list:
            # 根据类型描绘操作
            if operation["type"] == "move":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
                self.CopyingOpe_list.addItem(result)
            elif operation["type"] == "carddesp":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s %s"%(card_name, operation["desp"])
                self.CopyingOpe_list.addItem(result)
            elif operation["type"][0:2] == "LP":
                if operation['args'][0]==0:
                    target = "己方"
                else:
                    target = "对方"
                actions = {"Add":"增加","Dec":"降低","Cge":"变成","Hal":"减半"}
                subope = operation["type"][2:]
                action = actions[subope]
                point = ""
                if action != "减半":
                    point = "%d"%operation['args'][1]
                result = "%sLP%s%s"%(target,action,point)
                self.CopyingOpe_list.addItem(result)
            elif operation["type"] == "comment":
                self.CopyingOpe_list.addItem(operation["desp"])
                # 注释高亮
                self.CopyingOpe_list.item(self.CopyingOpe_list.count()-1).setForeground(QColor('green'))
            elif operation["type"] == "erase":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s 被移除"%(card_name)
                self.CopyingOpe_list.addItem(result)

    def select_copying(self):
        '''选择复制中的操作时，显示内容'''
        idx_item = self.CopyingOpe_list.currentIndex().row()
        if idx_item == -1 or idx_item >= len(self.copying_operation):
            return
        operation = self.copying_operation[idx_item]
        if operation == {}:
            return
        result = ""
        if operation["type"] == "move":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、\n"
                first_card = False
                card_name += "[%s]"%(self.operators["cards"][card_idx]["Name"])
            result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
        elif operation["type"] == "carddesp":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、\n"
                first_card = False
                card_name += "[%s]"%(self.operators["cards"][card_idx]["Name"])
            result = "%s %s"%(card_name, operation["desp"])
        elif operation["type"] == "erase":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、\n"
                first_card = False
                card_name += "[%s]"%(self.operators["cards"][card_idx]["Name"])
            result = "%s 被移除"%(card_name)
        elif operation["type"][0:2] == "LP":
            if operation['args'][0]==0:
                target = "己方"
            else:
                target = "对方"
            actions = {"Add":"增加","Dec":"降低","Cge":"变成","Hal":"减半"}
            subope = operation["type"][2:]
            action = actions[subope]
            point = ""
            if action != "减半":
                point = "%d"%operation['args'][1]
            result = "%sLP%s%s"%(target,action,point)
        elif operation["type"] == "comment":
            result = operation["desp"]
        self.Target_detail_browser.document().clear()
        self.Target_detail_browser.setText(result)

    def remove_from_copying(self, asking=True):
        idx_list = self.CopyingOpe_list.selectedIndexes()
        copying_size = len(self.copying_operation)
        if len(idx_list) <= 0 and copying_size != 1:
            return
        if asking:
            # 确认提示
            reply = QMessageBox.information(self, 'Confirm', "确认要从复制列表中删除选定操作吗？该操作不可逆。", QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return
        idx_list = [item.row() for item in idx_list]
        idx_list.sort(reverse=True)
        if len(idx_list) == 0 and copying_size == 1:
            idx_list.append(0)
        self.CopyingOpe_list.setCurrentRow(0)
        for idx in idx_list:
            del self.copying_operation[idx]
        self.update_copying()

    def target_index_changed(self):
        '''对象列表发生变更时触发\n\n通常需要更新卡片描述'''
        idx = self.Target_list.selectedIndexes()
        if len(idx) == 0:
            idx = -1
        else:
            idx = idx[0].row()
        if idx < 0:
            return
        for lst in self.idx_represent_field:
            if len(lst.selectedIndexes()) > 0:
                lst.clearSelection()
        card_id = self.targets[idx]
        self.show_cardinfo(card_id)

    def operation_index_changed(self):
        '''选择其它操作时，更新显示的场地'''
        self.refresh_field()
        self.update_targetlist()
        self.show_opeinfo()
        self.update_operation_label()
    
    def get_current_operation_index(self):
        '''获取当前选中的操作的index值。若选择非法，则返回-1'''
        index = self.Operator_list.currentIndex().row()
        if index >= len(self.operators["operations"]):
            return -1
        return index

    def update_targetlist(self):
        '''更新对象列表'''
        ope_id = self.get_current_operation_index()
        
        # 按钮禁用/恢复
        if len(self.targets) == 0:
            self.Move_card_button.setEnabled(False)
            self.Erase_card_button.setEnabled(False)
            self.Comment_card_button.setEnabled(False)
        else:
            self.Move_card_button.setEnabled(True)
            self.Erase_card_button.setEnabled(True)
            self.Comment_card_button.setEnabled(True)

        self.Target_list.clear()
        searching_name = self.NewCard_line.text()
        for target in self.targets:
            target_name = self.operators["cards"][target]["Name"]
            target_field = self.get_last_location(target, ope_id+1)
            self.Target_list.addItem("[%s]%s"%(target_field, target_name))
            possible_name = [target_name, target_name[:-1]]
            for name in possible_name:
                if self.coloring_field_card.isChecked() and name in self.card_colors:
                    self.Target_list.item(self.Target_list.count()-1).setForeground(cardcolors_dict[self.card_colors[name]])
                    break

            # 如果和搜索栏内容匹配则变为斜体
            if len(searching_name) > 0 and searching_name in target_name:
                self.Target_list.item(self.Target_list.count()-1).setFont(self.italic_font)
    
    def update_operationlist(self):
        '''操作格式：\n\ntype(str), args(list of int), dest(int), desp(str)'''
        self.Operator_list.clear()
        for ope_idx in range(len(self.operators["operations"])):
            operation = self.operators["operations"][ope_idx]
            if operation["type"] == "move":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
                self.Operator_list.addItem(result)
            elif operation["type"] == "carddesp":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s %s"%(card_name, operation["desp"])
                self.Operator_list.addItem(result)
                # 卡片修改标记
                self.Operator_list.item(self.Operator_list.count()-1).setForeground(QColor('darkblue'))
            elif operation["type"][0:2] == "LP":
                if operation['args'][0]==0:
                    target = "己方"
                else:
                    target = "对方"
                actions = {"Add":"增加","Dec":"降低","Cge":"变成","Hal":"减半"}
                subope = operation["type"][2:]
                action = actions[subope]
                point = ""
                if action != "减半":
                    point = "%d"%operation['args'][1]
                result = "%sLP%s%s"%(target,action,point)
                self.Operator_list.addItem(result)
                # LP修改标记
                self.Operator_list.item(self.Operator_list.count()-1).setForeground(QColor('darkgrey'))
                # 判断是否导致基本分归零
                if ope_idx <= self.lastest_field_id:
                    field = self.fields[ope_idx]
                    if field["LP"][0] <= 0 or field["LP"][1] <= 0:
                        # 归零高亮
                        self.Operator_list.item(self.Operator_list.count()-1).setForeground(QColor('red'))
            elif operation["type"] == "comment":
                self.Operator_list.addItem(operation["desp"])
                # 注释高亮
                self.Operator_list.item(self.Operator_list.count()-1).setForeground(QColor('green'))
            elif operation["type"] == "erase":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s 被移除"%(card_name)
                self.Operator_list.addItem(result)
            if ope_idx > self.lastest_field_id:
                pass
                # self.Operator_list.item(self.Operator_list.count()-1).setFont(self.italic_font)
        self.update_operation_label()

    def update_operation_label(self):
        '''刷新显示的操作列表信息'''
        ope_count = len(self.operators["operations"])
        ope_index = self.get_current_operation_index()+1
        self.label_operation_list.setText("操作列表(%d/%d)"%(ope_index, ope_count))

    def refresh_color(self):
        self.refresh_field()
        self.update_targetlist()
        self.search_card()

    def refresh_field(self):
        '''刷新场地'''
        for cardlist in self.idx_represent_field:
            cardlist.clear()
        
        # 获取最后一步操作
        idx = self.get_current_operation_index()
        if idx < 0 or self.lastest_field_id < idx:
            self.make_fields(self.lastest_field_id, idx)
            for operation_idx in range(self.lastest_field_id, min(self.Operator_list.count(), idx+1)):
                item = self.Operator_list.item(operation_idx)
                if item is not None:
                    item.setFont(self.normal_font)
                    field = self.fields[operation_idx]
                    if field["LP"][0] <= 0 or field["LP"][1] <= 0:
                        # 归零高亮
                        item.setForeground(QColor('red'))
            self.lastest_field_id = idx
        if idx < 0:
            operation = {"type":"None", "args":[]}
        else:
            operation = deepcopy(self.operators["operations"][idx])
        
        # 获取当前场地
        field = self.get_current_field()
        self.Self_LP.setText("%d"%field["LP"][0])
        self.Self_LP.setStyleSheet("color:black")
        self.Enemy_LP.setText("%d"%field["LP"][1])
        self.Enemy_LP.setStyleSheet("color:black")
        
        # 若最后操作为LP修改，则高亮修改LP
        if operation["type"][0:2] == "LP":
            if operation["args"][0] == 0:
                self.Self_LP.setStyleSheet("color:red")
            else:
                self.Enemy_LP.setStyleSheet("color:red")
        
        # 清除操作对象，为后续判断使用
        if operation["type"] not in ["move","carddesp"]:
            operation["args"].clear()

        # 获取搜索框内容
        searching_name = self.NewCard_line.text()

        # 描绘框内
        label_colors = ["QLabel{color:rgb(0,0,0)}",
                        "QLabel{color:rgb(0,0,0)}",
                        "QLabel{color:rgb(0,0,0)}",
                        "QLabel{color:rgb(0,0,0)}",
                        "QLabel{color:rgb(0,0,0)}",
                        "QLabel{color:rgb(0,0,0)}",
                        "QLabel{color:rgb(0,0,0)}",
                        "QLabel{color:rgb(0,0,0)}"]
        searched_frames = [self.Enemy_Ex, self.Enemy_Hand, self.Enemy_Grave, self.Enemy_Banish,
                self.Self_Ex, self.Self_Hand, self.Self_Grave, self.Self_Banish]
        labels = [self.label_enemy_ex, self.label_enemy_hand, self.label_enemy_grave, self.label_enemy_banish,
                self.label_self_ex, self.label_self_hand, self.label_self_grave, self.label_self_banish]
        for frameidx in range(len(idx_represent_str)):
            frame = self.idx_represent_field[frameidx]
            cardlist = field["fields"][frameidx]
            for card_id in reversed(cardlist):
                show_list = self.idx_represent_field[frameidx]
                # 获取卡片名字
                card_name = self.operators["cards"][card_id]["Name"]
                show_list.addItem(card_name)
                # 若为最后操作对象之一，使用粗体
                bl_font = card_id in operation["args"]
                # 若为搜索对象，使用斜体
                it_font = len(searching_name) > 0 and searching_name in card_name
                if it_font:
                    if frame in searched_frames:
                        label_colors[searched_frames.index(frame)] = "QLabel{color:rgb(255,0,102,255)}"
                    if bl_font:
                        show_list.item(show_list.count()-1).setFont(self.bold_italic_font)
                    else:
                        show_list.item(show_list.count()-1).setFont(self.italic_font)
                elif bl_font:
                    show_list.item(show_list.count()-1).setFont(self.bold_font)

                # 根据卡片种类进行上色
                if self.coloring_field_card.isChecked():
                    possible_name = [card_name, card_name[:-1]]
                    for name in possible_name:
                        if name in self.card_colors:
                            show_list.item(show_list.count()-1).setForeground(cardcolors_dict[self.card_colors[name]])
                            break
        
        # 数量标注
        self.label_enemy_ex.setText("对方额外(%d)"%self.Enemy_Ex.count())
        self.label_enemy_hand.setText("对方手卡(%d)"%self.Enemy_Hand.count())
        self.label_enemy_grave.setText("对方墓地(%d)"%self.Enemy_Grave.count())
        self.label_enemy_banish.setText("对方除外(%d)"%self.Enemy_Banish.count())
        self.label_self_ex.setText("己方额外(%d)"%self.Self_Ex.count())
        self.label_self_hand.setText("己方手卡(%d)"%self.Self_Hand.count())
        self.label_self_grave.setText("己方墓地(%d)"%self.Self_Grave.count())
        self.label_self_banish.setText("己方除外(%d)"%self.Self_Banish.count())
        for i in range(8):
            labels[i].setStyleSheet(label_colors[i])
 
    def ope_LPAdd(self):
        '''增加对象LP。'''
        lp_point = self.LP_line.text()
        try:
            lp_point = int(lp_point)
        except:
            return
        lp_target = self.LPTarget_Box.currentIndex()
        ope = {"type":"LPAdd", "args":[lp_target, lp_point], "dest":-1, "desp":""}
        self.insert_operation(ope)
    
    def ope_LPDec(self):
        '''减少对象LP。'''
        lp_point = self.LP_line.text()
        try:
            lp_point = int(lp_point)
        except:
            return
        lp_target = self.LPTarget_Box.currentIndex()
        ope = {"type":"LPDec", "args":[lp_target, lp_point], "dest":-1, "desp":""}
        self.insert_operation(ope)
    
    def ope_LPCge(self):
        '''更改对象LP。'''
        lp_point = self.LP_line.text()
        try:
            lp_point = int(lp_point)
        except:
            return
        lp_target = self.LPTarget_Box.currentIndex()
        ope = {"type":"LPCge", "args":[lp_target, lp_point], "dest":-1, "desp":""}
        self.insert_operation(ope)

    def ope_LPHal(self):
        '''对象LP减半。'''
        lp_target = self.LPTarget_Box.currentIndex()
        ope = {"type":"LPHal", "args":[lp_target, 0], "dest":-1, "desp":""}
        self.insert_operation(ope)

    def ope_movecards(self):
        '''移动卡片'''
        if len(self.targets) == 0:
            return
        self.Target_detail_browser.document().clear()
        self.Target_detail_browser.setText("")
        ope = {"type":"move", "args":self.targets.copy(), "dest": self.Dest_Box.currentIndex(), "desp":""}
        self.targets.clear()
        self.Target_list.clear()
        self.insert_operation(ope)

    def ope_addcomment(self):
        '''添加注释'''
        comment = self.Comment_Line.text()
        if len(comment) == 0:
            return
        ope = {"type":"comment", "args":[], "dest":0, "desp": comment}
        self.insert_operation(ope)
        self.Comment_Line.clear()

    def ope_addcarddesp(self):
        '''添加卡片描述'''
        comment = self.Comment_Line.text()
        if len(comment) == 0 or len(self.targets) == 0:
            return
        ope_id = self.get_current_operation_index()
        if ope_id < 0:
            ope_id = 0

        # 判断卡片是否在场上，若不在场上则不能添加注释
        for card_id in self.targets:
            if self.get_last_location(card_id, ope_id+1) == "未知":
                QMessageBox.warning(self, "错误", "不能给尚未加入的卡片添加注释！", QMessageBox.Yes)
                return
        ope = {"type":"carddesp", "args":self.targets.copy(), "dest":0, "desp": comment}
        self.targets.clear()
        self.Target_list.clear()
        self.Comment_Line.clear()
        self.insert_operation(ope)

    def erase_targets(self):
        '''将对象卡片移除出场'''
        if len(self.targets) == 0:
            return
        # 移除确认
        reply = QMessageBox.information(self, 'Confirm', "确认要删除吗？\n被删除的卡片在之后的操作中不会再出现。", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        self.Target_detail_browser.document().clear()
        self.Target_detail_browser.setText("")
        ope = {"type":"erase", "args":self.targets.copy(), "dest": 0, "desp":""}
        self.targets.clear()
        self.Target_list.clear()
        self.insert_operation(ope)

    def select_field(self, field_id):
        '''选择场上的卡片时调用'''
        # 获取场地
        lst = self.idx_represent_field[field_id]
        # 获取卡片索引
        selected = lst.selectedIndexes()
        if len(selected) < 1:
            return
        # 设置动作目标（便携操作）
        self.Dest_Box.setCurrentIndex(field_id)
        selected = selected[0].row()
        # 取消对象列表的焦点
        self.Target_list.clearSelection()
        # 取消其它场地的焦点
        for other_lst in self.idx_represent_field:
            if other_lst != lst:
                other_lst.clearSelection()
        
        # 查找选定卡片
        field = self.get_current_field()
        cardlist = field["fields"][field_id]
        card_id = cardlist[len(cardlist)-1-selected]
        self.show_cardinfo(card_id)
    
    def target_field(self, field_id):
        '''将场上的卡选为对象'''
        # 获取场地
        lst = self.idx_represent_field[field_id]
        # 获取卡片
        selected = lst.selectedIndexes()
        if len(selected) < 1:
            return
        selected = selected[0].row()
        # 取消焦点
        self.Target_list.clearSelection()
        for other_lst in self.idx_represent_field:
            if other_lst != lst:
                other_lst.clearSelection()
        # 查找对应卡片
        field = self.get_current_field()
        cardlist = field["fields"][field_id]
        card_id = cardlist[len(cardlist)-1-selected]
        if card_id not in self.targets:
            self.targets.append(card_id)
            self.label_target_list.setText("操作对象(%d)"%len(self.targets))
            self.update_targetlist()

    def text_check_legal(self, text, included, excluded):
        '''根据include group和exclude group，判断文字是否符合条件'''
        for i in included:
            if i not in text:
                return False
        for e in excluded:
            if e in text:
                return False
        return True

    def search_card(self):
        '''根据输入框的名字，在下拉框查找卡片'''
        # 名字修改过则进行高亮刷新
        if self.last_text != self.NewCard_line.text():
            self.last_text = self.NewCard_line.text()
            self.refresh_field()
            self.update_targetlist()
        # 判断是否有名字
        text = self.NewCard_line.text()
        if not self.Newcard_List.isEnabled():
            return
        if len(text) == 0:
            self.Newcard_List.clear()
            return
        self.Newcard_List.clear()
        # 缓存
        hit = []
        hit_in_name = []
        hit_in_effect = []
        # 多条件搜索
        included = []
        excluded = []
        split_text = text.split(" ")
        for sub_text in split_text:
            if len(sub_text) == 0:
                continue
            if sub_text[0] == "-":
                excluded.append(sub_text[1:])
            else:
                included.append(sub_text)
        if len(included)+len(excluded)==0:
            return
        # 遍历搜索符合条件的卡片
        for cardname in self.card_names:
            if text == cardname:
                hit.append(cardname)
            elif self.text_check_legal(cardname, included, excluded):
                hit_in_name.append(cardname)
            elif self.blur_search_bar.isChecked() and self.text_check_legal(self.raw_datas[cardname], included, excluded):
                hit_in_effect.append(cardname)
        # 添加到列表
        for name in hit:
            self.Newcard_List.addItem(name)
            self.Newcard_List.item(self.Newcard_List.count()-1).setFont(self.bold_font)
            if self.coloring_field_card.isChecked():
                self.Newcard_List.item(self.Newcard_List.count()-1).setForeground(cardcolors_dict[self.card_colors[name]])
        for name in hit_in_name:
            self.Newcard_List.addItem(name)
            if self.coloring_field_card.isChecked():
                self.Newcard_List.item(self.Newcard_List.count()-1).setForeground(cardcolors_dict[self.card_colors[name]])
        for name in hit_in_effect:
            self.Newcard_List.addItem(name)
            self.Newcard_List.item(self.Newcard_List.count()-1).setFont(self.italic_font)
            if self.coloring_field_card.isChecked():
                self.Newcard_List.item(self.Newcard_List.count()-1).setForeground(cardcolors_dict[self.card_colors[name]])
        self.label_cardsearch.setText("卡片搜索(%d)"%self.Newcard_List.count())
    
    def search_operation_cycle(self):
        '''根据给定内容搜索操作。'''
        self.search_operation(True)

    def search_operation(self, cycle=False):
        '''根据给定内容搜索操作。'''
        text = self.Operator_search.text()
        if text == "":
            return
        
        current_index = self.get_current_operation_index()
        if current_index < 0:
            return
        if not cycle:
            current_index = 0

        index_pointer = (current_index + 1) % self.Operator_list.count()
        while(index_pointer != current_index):
            if text in self.Operator_list.item(index_pointer).text():
                self.Operator_list.setCurrentRow(index_pointer)
                return
            index_pointer = (index_pointer + 1) % self.Operator_list.count()

    def show_carddesp(self):
        '''显示卡片的注释'''
        idx = self.Newcard_List.selectedIndexes()
        if len(idx) < 1:
            return
        cardname = self.Newcard_List.item(idx[0].row()).text()
        if cardname in self.card_datas:
            text = self.card_datas[cardname]
            self.Target_detail_browser.setHtml(text)
        self.update_img_buttom()

    def fix_cardname(self,qindex):
        '''补全卡名'''
        index = qindex.row()
        if index < 0:
            return
        self.NewCard_line.setText(self.Newcard_List.item(index).text())

    def update_rename_buttom(self):
        '''更新重命名按钮'''
        if self.showing_card_id is None:
            self.Rename_button.setEnabled(False)
            self.Target_effect_button.setEnabled(False)
            self.Rename_button.setText("未选定卡")
        else:
            self.Rename_button.setEnabled(True)
            self.Target_effect_button.setEnabled(True)
            cardname = self.operators["cards"][self.showing_card_id]["Name"]
            self.Rename_button.setText("重命名[%s]"%cardname)
        self.update_img_buttom()
    
    def update_img_buttom(self):
        if self.Newcard_List.hasFocus():
            idx = self.Newcard_List.selectedIndexes()
            if len(idx) < 1:
                return
            self.Target_img_button.setEnabled(True)
        elif self.showing_card_id is not None:
            self.Target_img_button.setEnabled(True)
        else:
            self.Target_img_button.setEnabled(False)

    def card_rename(self):
        '''卡片重命名'''
        if self.showing_card_id is None:
            return
        text = self.NewCard_line.text()
        if self.Newcard_List.hasFocus():
            idx = self.Newcard_List.selectedIndexes()
            if len(idx) > 0:
                text = self.Newcard_List.item(idx[0].row()).text()
        if len(text) == 0:
            return
        # 提示
        reply = QMessageBox.warning(self, '提示', "是否要把[%s]重命名为[%s]？"%(self.operators["cards"][self.showing_card_id]["Name"],text), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # 修改卡片信息
        ope_idx = self.get_current_operation_index()
        if ope_idx < 0:
            return

        # 刷新
        self.operators["cards"][self.showing_card_id]["Name"] = text
        self.update_rename_buttom()
        self.unsave_changed = True
        self.maketitle()
        self.update_operationlist()
        self.update_copying()
        self.Operator_list.setCurrentRow(ope_idx)
        self.refresh_field()
        self.update_targetlist()
        self.search_card()
    
    def open_calculator(self):
        '''打开计算器'''
        self.calculate_window.show()
    
    def open_about(self):
        '''打开关于窗口'''
        self.about_window.show()

    def update_hint(self, name):
        '''检查到更新的版本时弹出窗口'''
        box = QMessageBox(QMessageBox.Question, "检查更新", "检查到最新版本：%s，是否下载？"%name)
        direct_download = box.addButton("直接下载", QMessageBox.YesRole)
        page_download = box.addButton("打开页面", QMessageBox.YesRole)
        box.addButton("取消", QMessageBox.NoRole)
        box.exec_()
        if box.clickedButton() == direct_download:
            self.download_thread = Download_Thread(self, self.release_url)
            self.download_thread.setDaemon(True)
            self.download_thread.version_name = name
            self.download_thread.start()
        elif box.clickedButton() == page_download:
            webbrowser.open("https://github.com/Wind2009-Louse/DuelEditor/releases/tag/%s"%name)
    
    def process_hint(self, pcs):
        '''从下载线程返回的进程提示'''
        self.maketitle(pcs)

    def download_hint(self, name):
        '''从下载线程返回的结果提示'''
        QMessageBox.about(self, "提示", name)

    def clear_unuse_cards(self):
        '''清除没有在操作中使用过的卡片，节省空间'''
        all_cards = set(self.operators["cards"].keys())
        all_cards -= set(self.targets)
        for ope in self.operators["operations"]:
            if ope["type"][0:2] != "LP":
                all_cards -= set(ope["args"])
        for ope_copying in self.copying_operation:
            if ope_copying["type"][0:2] != "LP":
                all_cards -= set(ope_copying["args"])
        for c in all_cards:
            self.operators["cards"].pop(c,"fail")
        while(self.operators["cardindex"] > 0 and str(self.operators["cardindex"]-1) not in self.operators["cards"]):
            self.operators["cardindex"] -= 1

    def read_config(self):
        '''读取可能存在的配置文件'''
        config_data = None
        self.fullfilename = ""
        self.lastest_field_id = -1
        self.recent_file_list = []
        try:
            f = open("DuelEditorConfig.jsn", 'r', encoding='utf-8')
            config_data = loads(f.read())
        except Exception as e:
            pass
        enable_config = [[self.blur_search_bar, "blur_search"], [self.coloring_field_card, "coloring_field"]]
        for cfg in enable_config:
            try:
                bar = cfg[0]
                sel = config_data[cfg[1]]
                if sel == 0:
                    bar.setChecked(False)
                else:
                    bar.setChecked(True)
            except Exception as e:
                continue
        
        try:
            self.fullfilename = config_data["last_file"]
        except:
            self.fullfilename = ""
        try:
            self.lastest_field_id = config_data["last_operation"]
        except:
            pass
        # 1.21 最近文件列表
        try:
            self.recent_file_list = config_data["recent"]
            if len(self.recent_file_list) > 0:
                most_recent = self.recent_file_list[0]
                self.fullfilename = most_recent["name"]
                self.lastest_field_id = most_recent["idx"]
        except:
            pass
        
        try:
            width = max(config_data["width"], self.mini_width)
            height = max(config_data["height"], self.mini_height)
            self.resize(width, height)
        except:
            pass
        
        try:
            self.version_url = config_data["version_url"]
            self.release_url = config_data["release_url"]
        except:
            self.version_url = mirror_setting[default_mirror]["version"]
            self.release_url = mirror_setting[default_mirror]["release"]
        self.mirror_bar_update()

    def save_config(self):
        self.update_recent(self.fullfilename, self.get_current_operation_index())
        '''保存配置文件'''
        config = {"blur_search": 1 if self.blur_search_bar.isChecked() else 0,
                "coloring_field": 1 if self.coloring_field_card.isChecked() else 0,
                "recent": self.recent_file_list,
                "width": self.width(),
                "height": self.height(),
                "version_url": self.version_url,
                "release_url": self.release_url}
        config_data = dumps(config)
        with open("DuelEditorConfig.jsn", 'w', encoding='utf-8') as f:
            f.write(config_data)

    def view_pic(self):
        card_name = ""
        if self.Newcard_List.hasFocus():
            idx = self.Newcard_List.selectedIndexes()
            if len(idx) < 1:
                return
            card_name = self.Newcard_List.item(idx[0].row()).text()
        if card_name == "" and self.showing_card_id is not None and self.showing_card_id in self.operators["cards"]:
            card_name = self.operators["cards"][self.showing_card_id]["Name"]

        if len(card_name) == 0:
            return
        search_list = [card_name, card_name[:-1]]
        show_card_key = 0
        show_card_name = ""

        # 本地目录图片
        dir_list = [os.path.join(os.path.abspath('.'), "pics")]
        # YGOPro2图片
        if os.name == "nt":
            import winreg
            try:
                pro2_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths\YGOPro2.exe", access=winreg.KEY_READ)
                if pro2_key:
                    pro2_path = winreg.QueryValueEx(pro2_key, "path")
                    if len(pro2_path) > 0:
                        dir_list.append(os.path.join(pro2_path[0], "picture", "card"))
            except Exception as e:
                pass
            try:
                pro2_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\YGOPro2.exe", access=winreg.KEY_READ)
                if pro2_key:
                    pro2_path = winreg.QueryValueEx(pro2_key, "path")
                    if len(pro2_path) > 0:
                        dir_list.append(os.path.join(pro2_path[0], "picture", "card"))
            except Exception as e:
                pass

        for name in search_list:
            if name in self.id_map_by_name:
                show_card_key = self.id_map_by_name[name]
                show_card_name = name
                for search_dir in dir_list:
                    png_file_name = os.path.join(search_dir, "%d.png"%show_card_key)
                    jpg_file_name = os.path.join(search_dir, "%d.jpg"%show_card_key)
                    if os.path.exists(png_file_name) or os.path.exists(jpg_file_name):
                        pic_window_ref = pic_window.UI_PIC(self, show_card_key, name)
                        pic_window_ref.show()
                        self.img_window_list.append(pic_window_ref)
                        return

        if show_card_key == 0:
            QMessageBox.warning(self, "提示", "该卡片没有图片！", QMessageBox.Yes)
        else:
            reply = QMessageBox.warning(self, '提示', "找不到[%s]的卡图，是否下载？"%show_card_name, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                pic_window_ref = pic_window.UI_PIC(self, show_card_key, show_card_name)
                pic_window_ref.show()
                self.img_window_list.append(pic_window_ref)

    def export_deck(self):
        '''导出卡组'''
        # 判断是否有deck文件夹
        open_dir = os.path.abspath('.')
        deck_dir = os.path.join(os.path.abspath('.'), "deck")
        if os.path.exists(deck_dir):
            open_dir = deck_dir
        
        # 获取
        self_filename = str(QFileDialog.getSaveFileName(self,'己方卡组', os.path.join(open_dir, "self.ydk"),"*.ydk")[0])
        if len(self_filename) == 0:
            return
        open_dir = os.path.dirname(self_filename)
        enemy_filename = str(QFileDialog.getSaveFileName(self,'对方卡组', os.path.join(open_dir, "opposite.ydk"),"*.ydk")[0])
        if len(enemy_filename) == 0:
            return
        
        # 开始导出(0=main, 1=ex)
        self_deck_list = [[], []]
        enemy_deck_list = [[], []]
        undefined_name = []

        try:
            self.make_fields()
            operation_list = self.operators["operations"]
            last_controller = -2
            for ope_idx in range(len(operation_list)):
                ope = operation_list[ope_idx]
                if ope["type"] != "move":
                    continue
                for card_idx in ope["args"]:
                    last_place = self.get_last_location(card_idx, ope_idx)
                    new_card_to_add = True
                    if last_place != "未知":
                        new_card_to_add = False
                    card_name = self.operators["cards"][card_idx]["Name"]
                    goal_str = idx_represent_str[ope["dest"]]
                    controller = -2
                    for check_str in idx_represent_controller.keys():
                        if check_str in goal_str:
                            controller = idx_represent_controller[check_str]
                            break
                    if controller == 0:
                        controller = last_controller
                    if controller in [-2, 0]:
                        print("[%s]找不到所在地[%s]的控制者。"%(card_name, goal_str))
                    last_controller = controller
                    if new_card_to_add:
                        card_pic_id = self.get_id_by_name(card_name)
                        if card_pic_id == -1:
                            card_pic_id = 48588176
                            undefined_name.append(card_name)
                        if card_pic_id in self.token_card_id_set:
                            continue
                        ex_idx = 1 if card_pic_id in self.ex_card_id_set else 0
                        if controller == 1:
                            self_deck_list[ex_idx].append(str(card_pic_id))
                        if controller == -1:
                            enemy_deck_list[ex_idx].append(str(card_pic_id))
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "提示", "生成卡组失败：%s"%str(e), QMessageBox.Yes)
            return
        if self.generate_deck(self_deck_list, self_filename, "己方卡组") and self.generate_deck(enemy_deck_list, enemy_filename, "对方卡组"):
            result_str = "导出成功！"
            if len(undefined_name) > 0:
                result_str += "\n以下卡片无法被识别，已被设为默认卡片：\n" + "\n".join(undefined_name)
            QMessageBox.warning(self, "提示", result_str, QMessageBox.Yes)

    def get_id_by_name(self, card_name):
        '''根据卡片名称，获取卡片ID。查询不到的情况下，返回-1。'''
        search_list = [card_name, card_name[:-1]]
        for name in search_list:
            if name in self.id_map_by_name:
                return self.id_map_by_name[name]
        return -1
    
    def generate_deck(self, deck_list, file_name, fail_by):
        '''根据export_deck生成的卡组数据，生成卡组'''
        deck_str = "\n".join(("#created by DuelEditor\n#main", "\n".join(deck_list[0]), "#extra", "\n".join(deck_list[1])))
        try:
            with open(file_name,'w',encoding='utf-8') as f:
                f.write(deck_str)
            warning_msg = []
            if len(deck_list[0]) > 60:
                warning_msg.append("%s主卡组数量为%d，超过60张。"%(fail_by, len(deck_list[0])))
            if len(deck_list[1]) > 15:
                warning_msg.append("%s额外卡组数量为%d，超过15张。"%(fail_by, len(deck_list[1])))
            if len(warning_msg) > 0:
                QMessageBox.warning(self, "提示", "\n".join(warning_msg), QMessageBox.Yes)
            return True
        except Exception as e:
            QMessageBox.warning(self, "提示", "保存%s失败：%s"%(fail_by, str(e)), QMessageBox.Yes)
            return False

    def img_cache_clear(self, signal=None):
        new_list = []
        for window in self.img_window_list:
            if window is None:
                continue
            if window.isHidden():
                continue
            new_list.append(window)
        self.img_window_list = new_list

    def mirror_bar_init(self, bar):
        self.mirror_bar_list = bar.addMenu("镜像源…")

        self.mirror_action_dict = {}
        for m_name in mirror_setting.keys():
            act = QAction(m_name, self, checkable=True)
            self.mirror_bar_list.addAction(act)
            self.mirror_action_dict[m_name] = act
        act = QAction("自定义", self, checkable=True)
        act.setEnabled(False)
        self.mirror_bar_list.addAction(act)
        self.mirror_action_dict["自定义"] = act
        self.mirror_bar_list.triggered[QAction].connect(self.mirror_bar_update)

    def mirror_bar_update(self, qaction=None):
        global mirror_setting
        if qaction is not None:
            sel = qaction.text()
            if sel in mirror_setting:
                m = mirror_setting[sel]
                self.version_url = m["version"]
                self.release_url = m["release"]
                self.about_window.url = m["version"]
        identi = None
        identi_checked = True
        for act_item in self.mirror_action_dict.items():
            act_name = act_item[0]
            act = act_item[1]
            if act_name == "自定义":
                identi = act
                continue
            else:
                m = mirror_setting[act_name]
                if self.version_url == m["version"] and self.release_url == m["release"]:
                    identi_checked = False
                    act.setChecked(True)
                else:
                    act.setChecked(False)
                
        if identi is not None:
            identi.setChecked(identi_checked)
            
    def get_recent_index(self, filename):
        '''
        获取指定文件的最新记录
        '''
        for his in self.recent_file_list:
            if filename == his["name"]:
                return his["idx"]
        return None

    def update_recent(self, filename, idx):
        '''
        更新最近文件列表
        idx<-1时为删除
        '''

        # 更新最近记录
        if filename is None or len(filename) <= 0:
            return
        if self.recent_file_list is None:
            self.recent_file_list = []
        try:
            target = None
            for his_idx in range(0, len(self.recent_file_list)) :
                his = self.recent_file_list[his_idx]
                if filename == his["name"]:
                    target = his
                    target["idx"] = idx
                    del self.recent_file_list[his_idx]
                    break
            if idx >= -1:
                if target is None:
                    target = {"name": filename, "idx": idx}
                if len(self.recent_file_list) >= 10:
                    self.recent_file_list = self.recent_file_list[0:9]
                self.recent_file_list.insert(0, target)
        except Exception as e:
            print(e)

        # 更新bar
        try:
            self.recent_bar_list.clear()
            if len(self.recent_file_list) == 0:
                act = QAction("(无)", self)
                act.setEnabled(False)
                self.recent_bar_list.addAction(act)
            else:
                for his in self.recent_file_list:
                    act = QAction(his["name"], self)
                    self.recent_bar_list.addAction(act)
        except Exception as e:
            print(e)
    
    def save_and_open_file(self, filename=None):
        '''
        菜单栏用，先保存当前配置，然后调用打开
        '''
        self.save_config()
        self.openfile(filename)

    def open_recent_file(self, act=None):
        '''
        打开最近文件时调用
        '''
        if act is None:
            return
        self.save_and_open_file(act.text())
    
    def read_cdb(self, filename, card_sorted):
        '''
        读取cdb文件
        '''
        cardtypes = {0x1: "怪兽", 0x2: "<font color='#0A8000'>魔法</font>", 0x4: "<font color='#EB1E80'>陷阱</font>", 0x10: "<font color='#A8A800'>通常</font>", 0x20: "<font color='#B24400'>效果</font>", 0x40: "<font color='#6C226C'>融合</font>", 0x80: "<font color='#1080EB'>仪式</font>", 0x200: "灵魂", 0x400: "同盟", 0x800: "二重", 0x1000: "调整", 0x2000: "<font color='#A8A8A8'>同调</font>", 0x4000: "<font color='#626262'>衍生物</font>", 0x10000: "速攻", 0x20000: "永续", 0x40000: "装备", 0x80000: "场地", 0x100000: "反击", 0x200000: "反转", 0x400000: "卡通", 0x800000: "<span style='background:black'><font color='#FFFFFF'>超量</font></span>", 0x1000000: "灵摆", 0x2000000: "特殊召唤", 0x4000000: "<font color='#033E74'>连接</font>"}
        cardraces = {0x1: "战士族", 0x2: "魔法师族", 0x4: "天使族", 0x8: "恶魔族", 0x10: "不死族", 0x20: "机械族", 0x40: "水族", 0x80: "炎族", 0x100: "岩石族", 0x200: "鸟兽族", 0x400: "植物族", 0x800: "昆虫族", 0x1000: "雷族", 0x2000: "龙族", 0x4000: "兽族", 0x8000: "兽战士族", 0x10000: "恐龙族", 0x20000: "鱼族", 0x40000: "海龙族", 0x80000: "爬虫类族", 0x100000: "念动力族", 0x200000: "幻神兽族", 0x400000: "创造神族", 0x800000: "幻龙族", 0x1000000: "电子界族"}
        cardattrs = {0x1: "<font color='#121516'>地</font>", 0x2: "<font color='#0993D3'>水</font>", 0x4: "<font color='red'>炎</font>", 0x8: "<font color='#1B5D33'>风</font>", 0x10: "<font color='#7F5D32'>光</font>", 0x20: "<font color='#9A2B89'>暗</font>", 0x40: "<font color='DarkGoldenRod'>神</font>"}
        excardtypes = {0x40: "融合", 0x2000: "同调", 0x800000: "超量", 0x4000000: "连接"}
        tokentype = 0x4000
        linkmarkers = {0x40:"[↖]", 0x80:"[↑]", 0x100:"[↗]", 0x8:"[←]", 0x20:"[→]", 0x1: "[↙]", 0x2:"[↓]", 0x4:"[↘]"}
        cardcolors_list = [0x2, 0x4, 0x10, 0x40, 0x80, 0x2000, 0x800000, 0x4000000, 0x4000]

        search_type = {0x1: 1, 0x2: 2, 0x4:3}
        search_subtype = {0x10: 1, 0x40: 3, 0x80:4, 0x2000: 5, 0x800000:6, 0x4000000:7, 0x4000:8,
            0x10000: 3, 0x20000: 4, 0x40000:5, 0x80000:6, 0x100000: 7}

        sql_conn = None
        try:
            sql_conn = connect(filename)
            cur = sql_conn.cursor()
            # 0 id
            # 1 ot
            # 2 alias
            # 3 setcode
            # 4 type
            # 5 atk
            # 6 def
            # 7 level
            # 8 race
            # 9 attribute
            # 10 category
            # 11 name
            # 12 desc
            sel = cur.execute("select datas.*, texts.name, texts.desc from datas inner join texts on texts.id = datas.id;")
            for carddata in sel:
                if carddata[11] not in self.card_datas.keys():
                    card_sorted_index = [0,2,0,0,0]
                    # 卡片类型（排序）
                    for c_type in search_type.keys():
                        if carddata[4] & c_type != 0:
                            card_sorted_index[0] = search_type[c_type]
                    for c_subtype in search_subtype.keys():
                        if carddata[4] & c_subtype != 0:
                            card_sorted_index[1] = search_subtype[c_subtype]
                    # 卡片颜色
                    self.card_colors[carddata[11]] = 0xffffffff
                    for color_set in cardcolors_list:
                        if carddata[4] & color_set != 0:
                            self.card_colors[carddata[11]] = color_set
                            break
                    # 生成描述
                    desp = ""
                    # 种类
                    for types in cardtypes.keys():
                        if carddata[4] & types != 0:
                            if types in excardtypes.keys():
                                self.ex_card_id_set.add(carddata[0])
                            elif types == tokentype:
                                self.token_card_id_set.add(carddata[0])
                            if desp != "":
                                desp += "/"
                            desp += cardtypes[types]
                    if carddata[4] in [0x2, 0x4]:
                        desp += "/通常"
                    # 怪兽信息
                    if carddata[4] & 0x1 != 0:
                        # 等阶/Link
                        if carddata[4] & 0x4000000 != 0:
                            desp += " Link-%d"%carddata[7]
                            card_sorted_index[2] = 13 - carddata[7]
                        else:
                            desp += " %d★"%(carddata[7]&0xffff)
                            card_sorted_index[2] = 13 - carddata[7]&0xffff
                        # 属性/种族
                        attr_str = ""
                        for attr in cardattrs.keys():
                            if carddata[9] & attr != 0:
                                if attr_str != "":
                                    attr_str += "&"
                                attr_str += cardattrs[attr]
                        race_str = ""
                        for race in cardraces.keys():
                            if carddata[8] & race != 0:
                                if race_str != "":
                                    race_str += "&"
                                race_str += cardraces[race]
                        desp += " %s/%s"%(attr_str, race_str)
                        # ATK/DEF
                        monster_ad = [carddata[5],0]
                        if carddata[5] < 0:
                            desp += " ?"
                        else:
                            desp += " %d"%carddata[5]
                        card_sorted_index[3] = -max(carddata[5], 0)
                        card_sorted_index[4] = -carddata[6]
                        if carddata[4] & 0x4000000 == 0:
                            monster_ad[1] = carddata[6]
                            if carddata[6] < 0:
                                desp += "/?"
                            else:
                                desp += "/%d"%carddata[6]
                        else:
                            desp += " "
                            for marker in linkmarkers.keys():
                                if carddata[6] & marker != 0:
                                    desp += linkmarkers[marker]
                        self.monster_datas[carddata[11]] = monster_ad
                    
                    card_sorted[carddata[11]] = card_sorted_index
                    # 效果换行
                    eff_desp = carddata[12]
                    eff_desp = sub(r"\r\n",r"<br>",eff_desp)
                    desp += "<br>%s"%eff_desp
                    self.card_datas[carddata[11]] = "[<a href=\"https://ygocdb.com/card/%d\">%s</a>]<br>%s"%(carddata[0], carddata[11], desp)
                    raw_desp = "%d%s<br>%s"%(carddata[0], carddata[11], desp)
                    raw_desp = sub(r"<font[^>]+?>([^<]+?)</font>",r"\1",raw_desp)
                    raw_desp = sub(r"<span[^>]+?>([^<]+?)</span>",r"\1",raw_desp)
                    raw_desp = sub(r"<br>",r"",raw_desp)
                    self.raw_datas[carddata[11]] = raw_desp
                    self.id_map_by_name[carddata[11]] = carddata[0]
        except Exception as e:
            print(e)
        finally:
            if sql_conn:
                sql_conn.close()

    def read_cdbs_from_dir(self, dir_name, card_sorted):
        '''
        从文件夹中读取cdb
        '''
        full_dirname = os.path.join(os.getcwd(), dir_name)
        if os.access(full_dirname, os.F_OK):
            for root, dirs, files in os.walk(full_dirname):
                for ex_fname in files:
                    try:
                        # cdb文件，直接读取
                        if ex_fname.endswith(".cdb"):
                            self.read_cdb(os.path.join(root, ex_fname), card_sorted)
                        # ypk/zip文件，读取压缩包内容
                        if ex_fname.endswith(".ypk") or ex_fname.endswith(".zip"):
                            self.read_cdbs_from_zip(os.path.join(root, ex_fname), card_sorted)
                    except Exception as e:
                        print(e)

    def read_cdbs_from_zip(self, zip_filename, card_sorted):
        '''
        从压缩包中读取cdb
        '''
        if zipfile.is_zipfile(zip_filename):
            with zipfile.ZipFile(zip_filename, mode='r') as zipf:
                tmp_path = mkdtemp()
                for zip_fn in zipf.namelist():
                    # 找到压缩包内的cdb，解压到临时目录读取，读取完毕后删除
                    if zip_fn.endswith(".cdb"):
                        zipf.extract(zip_fn, tmp_path)
                        self.read_cdb(os.path.join(tmp_path, zip_fn), card_sorted)
                rmtree(tmp_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = Ui_MainWindow()

    m_window.show()
    sys.exit(app.exec_())

