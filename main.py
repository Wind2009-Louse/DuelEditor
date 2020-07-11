#encoding:utf-8
import sys
from json import loads, dumps
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QAction, QMenuBar
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QTextBrowser, QPushButton, QLineEdit, QComboBox, QMainWindow
from PyQt5.QtCore import QRect, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QColor
from functools import partial
from copy import deepcopy
import os
import re
import calculator, about
from sqlite3 import connect

idx_represent_str = ["己方手卡", "己方魔陷_1", "己方魔陷_2", "己方魔陷_3", "己方魔陷_4", "己方魔陷_5", "己方场地", "己方灵摆_1", "己方灵摆_2", "己方怪兽_1", "己方怪兽_2", "己方怪兽_3", "己方怪兽_4", "己方怪兽_5", "己方墓地", "己方除外", "己方额外", "对方手卡", "对方魔陷_1", "对方魔陷_2", "对方魔陷_3", "对方魔陷_4", "对方魔陷_5", "对方场地", "对方灵摆_1", "对方灵摆_2", "对方怪兽_1", "对方怪兽_2", "对方怪兽_3", "对方怪兽_4", "对方怪兽_5", "对方墓地", "对方除外", "对方额外", "额外怪兽区_1", "额外怪兽区_2"]
init_field = {"locations":{}, "desp":{}, "LP":[8000,8000], "fields":[]}
for t in range(len(idx_represent_str)):
    init_field["fields"].append([])
version = 130

class Ui_MainWindow(QMainWindow):
    def placeframe(self):
        menu_height = self.menuBar().height()
        width = self.width()
        height = self.height() - menu_height
        # print(width, height)

        width_1_1 = 191 * width / self.origin_width
        height_1_1 = 143 * height / self.origin_height
        if height < self.origin_height:
            height_1_1 = 143 - (self.origin_height - height) / 2
        xline_1_1 = 10
        xline_1_2 = 10 + 200 * width / self.origin_width
        xline_1_3 = 10 + 400 * width / self.origin_width
        xline_1_4 = 10 + 600 * width / self.origin_width
        yline_1_1 = menu_height + 8
        yline_1_2 = menu_height + (self.origin_height - 10) * height / self.origin_height - height_1_1
        if height < self.origin_height:
            yline_1_2 = menu_height + (self.origin_height - 153) - (self.origin_height - height) / 2

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
        xline_2_2 = 10 + 120 * width / self.origin_width
        xline_2_3 = 10 + 120 * width / self.origin_width + width_2_0
        xline_2_4 = 10 + 120 * width / self.origin_width + width_2_0 * 2
        xline_2_5 = 10 + 120 * width / self.origin_width + width_2_0 * 3
        xline_2_6 = 10 + 120 * width / self.origin_width + width_2_0 * 4
        xline_2_7 = 10 + 680 * width / self.origin_width
        yline_2_1 = yline_1_1 + height_1_1 + 30
        yline_2_2 = yline_2_1 + height_2_0
        yline_2_3 = yline_2_1 + height_2_0 * 2 # 280 * height / self.origin_height
        yline_2_4 = yline_2_1 + height_2_0 * 3 # 330 * height / self.origin_height
        yline_2_5 = yline_2_1 + height_2_0 * 4 # 380 * height / self.origin_height
        yline_2_6 = yline_2_1 + height_2_0 + 25 # 255 * height / self.origin_height
        yline_2_7 = yline_2_5 - height_2_0 - 25 # 305 * height / self.origin_height
        yline_2_8 = yline_2_5 - 45 # 335 * height / self.origin_height
        if height < self.origin_height:
            diff = (self.origin_height - height) / 2
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
        width_3_1 = 181 * width / self.origin_width
        height_3_1 = 235 * (height - magic_3_1) / (self.origin_height - magic_3_1)
        height_3_2 = height - 160 - height_3_1
        xline_3_1 = 810 * width / self.origin_width
        self.label_target_list.setGeometry(QRect(xline_3_1, menu_height, width_3_1, 20))
        self.Target_list.setGeometry(QRect(xline_3_1, menu_height + 20, width_3_1, height_3_1))
        self.Delete_target.setGeometry(QRect(xline_3_1, menu_height + height_3_1+25, width_3_1, 28))
        self.Dest_Box.setGeometry(QRect(xline_3_1, menu_height + height_3_1+63, width_3_1, 22))
        self.MoveCard_Button.setGeometry(QRect(xline_3_1, menu_height + height_3_1+90, width_3_1, 28))
        self.EraseCard_Button.setGeometry(QRect(xline_3_1, menu_height + height_3_1+120, width_3_1, 28))
        self.Target_detail.setGeometry(QRect(xline_3_1, menu_height + height_3_1+150, width_3_1, height_3_2))

        # search/operation buttoms
        width_4_1 = 181 * width / self.origin_width
        height_4_1 = height - 410
        xline_4_1 = 1000 * width / self.origin_width
        self.label_cardsearch.setGeometry(QRect(xline_4_1, menu_height, width_4_1, 20))
        self.NewCard_line.setGeometry(QRect(xline_4_1, menu_height + 20, width_4_1, 21))
        self.Newcard_List.setGeometry(QRect(xline_4_1, menu_height + 50, width_4_1, height_4_1))
        self.CreateCard_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+55, width_4_1, 28))
        self.NewCard_Rename_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+85, width_4_1, 28))
        self.Comment_Line.setGeometry(QRect(xline_4_1, menu_height + height_4_1+123, width_4_1, 21))
        self.CommentCard_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+150, width_4_1, 28))
        self.Comment_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+180, width_4_1, 28))
        self.LPTarget_Box.setGeometry(QRect(xline_4_1, menu_height + height_4_1+220, width_4_1, 22))
        self.LP_line.setGeometry(QRect(xline_4_1, menu_height + height_4_1+250, width_4_1, 21))
        self.AddLP_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+280, width_4_1, 28))
        self.DecLP_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+310, width_4_1, 28))
        self.CgeLP_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+340, width_4_1, 28))
        self.HalLP_Button.setGeometry(QRect(xline_4_1, menu_height + height_4_1+370, width_4_1, 28))

        # operation list
        width_5_1 = 181 * width / self.origin_width
        height_5_1 = height - 200
        xline_5_1 = 1190 * width / self.origin_width

        self.label_operation_list.setGeometry(QRect(xline_5_1, menu_height, width_5_1, 16))
        self.Operator_search.setGeometry(QRect(xline_5_1, menu_height + 20, width_5_1 - 23, 21))
        self.Operator_search_button.setGeometry(QRect(xline_5_1 + width_5_1 - 21, menu_height + 20, 21, 21))
        self.Operator_list.setGeometry(QRect(xline_5_1, menu_height + 50, width_5_1, height_5_1 - 20))
        self.DeleteOpe_Button.setGeometry(QRect(xline_5_1, menu_height + height_5_1+35, width_5_1, 28))
        self.SelectedOpe_list.setGeometry(QRect(xline_5_1, menu_height + height_5_1+70, width_5_1, 55))
        self.CopyOpe_Button.setGeometry(QRect(xline_5_1, menu_height + height_5_1+130, width_5_1, 28))
        self.MoveOpe_Button.setGeometry(QRect(xline_5_1, menu_height + height_5_1+160, width_5_1, 28))

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
        self.Delete_target = QPushButton(self.centralwidget)
        self.Dest_Box = QComboBox(self.centralwidget)
        for i in range(36):
            self.Dest_Box.addItem("")
        self.MoveCard_Button = QPushButton(self.centralwidget)
        self.EraseCard_Button = QPushButton(self.centralwidget)
        self.Target_detail = QTextBrowser(self.centralwidget)

        self.NewCard_line = QLineEdit(self.centralwidget)
        self.NewCard_line.setPlaceholderText("输入卡片名称")
        self.Newcard_List = QListWidget(self.centralwidget)
        self.CreateCard_Button = QPushButton(self.centralwidget)
        self.NewCard_Rename_Button = QPushButton(self.centralwidget)
        self.Comment_Line = QLineEdit(self.centralwidget)
        self.Comment_Line.setPlaceholderText("输入注释")
        self.CommentCard_Button = QPushButton(self.centralwidget)
        self.Comment_Button = QPushButton(self.centralwidget)
        self.LPTarget_Box = QComboBox(self.centralwidget)
        self.LPTarget_Box.addItem("")
        self.LPTarget_Box.addItem("")
        self.LP_line = QLineEdit(self.centralwidget)
        regx = QRegExp("^[0-9]{15}$")
        validator = QRegExpValidator(regx, self.LP_line)
        self.LP_line.setValidator(validator)
        self.LP_line.setPlaceholderText("输入基本分变动")
        self.AddLP_Button = QPushButton(self.centralwidget)
        self.DecLP_Button = QPushButton(self.centralwidget)
        self.CgeLP_Button = QPushButton(self.centralwidget)
        self.HalLP_Button = QPushButton(self.centralwidget)

        self.Operator_list = QListWidget(self.centralwidget)
        self.Operator_search = QLineEdit(self.centralwidget)
        self.Operator_search.setPlaceholderText("输入操作内容搜索")
        self.Operator_search_button = QPushButton(self.centralwidget)
        self.DeleteOpe_Button = QPushButton(self.centralwidget)
        self.SelectedOpe_list = QListWidget(self.centralwidget)
        self.CopyOpe_Button = QPushButton(self.centralwidget)
        self.MoveOpe_Button = QPushButton(self.centralwidget)

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
        idx_represent_str = ["己方手卡", "己方魔陷_1", "己方魔陷_2", "己方魔陷_3", "己方魔陷_4", "己方魔陷_5", "己方场地", "己方灵摆_1", "己方灵摆_2", "己方怪兽_1", "己方怪兽_2", "己方怪兽_3", "己方怪兽_4", "己方怪兽_5", "己方墓地", "己方除外", "己方额外", "对方手卡", "对方魔陷_1", "对方魔陷_2", "对方魔陷_3", "对方魔陷_4", "对方魔陷_5", "对方场地", "对方灵摆_1", "对方灵摆_2", "对方怪兽_1", "对方怪兽_2", "对方怪兽_3", "对方怪兽_4", "对方怪兽_5", "对方墓地", "对方除外", "对方额外", "额外怪兽区_1", "额外怪兽区_2"]
        cardtypes = {0x1: "怪兽", 0x2: "<font color='#008972'>魔法</font>", 0x4: "<font color='#B12B7A'>陷阱</font>", 0x10: "通常", 0x20: "<font color='#BA6337'>效果</font>", 0x40: "<font color='#803D90'>融合</font>", 0x80: "<font color='#5F7EBB'>仪式</font>", 0x200: "灵魂", 0x400: "同盟", 0x800: "二重", 0x1000: "调整", 0x2000: "同调", 0x4000: "衍生物", 0x10000: "速攻", 0x20000: "永续", 0x40000: "装备", 0x80000: "场地", 0x100000: "反击", 0x200000: "反转", 0x400000: "卡通", 0x800000: "<span style='background:black'><font color='#FFFFFF'>超量</font></span>", 0x1000000: "灵摆", 0x2000000: "特殊召唤", 0x4000000: "<font color='#0874AC'>连接</font>"}
        cardraces = {0x1: "战士族", 0x2: "魔法师族", 0x4: "天使族", 0x8: "恶魔族", 0x10: "不死族", 0x20: "机械族", 0x40: "水族", 0x80: "炎族", 0x100: "岩石族", 0x200: "鸟兽族", 0x400: "植物族", 0x800: "昆虫族", 0x1000: "雷族", 0x2000: "龙族", 0x4000: "兽族", 0x8000: "兽战士族", 0x10000: "恐龙族", 0x20000: "鱼族", 0x40000: "海龙族", 0x80000: "爬虫类族", 0x100000: "念动力族", 0x200000: "幻神兽族", 0x400000: "创造神族", 0x800000: "幻龙族", 0x1000000: "电子界族"}
        cardattrs = {0x1: "<font color='#height_1_1 - 22516'>地</font>", 0x2: "<font color='#0993D3'>水</font>", 0x4: "<font color='red'>炎</font>", 0x8: "<font color='#1B5D33'>风</font>", 0x10: "<font color='#7F5D32'>光</font>", 0x20: "<font color='#9A2B89'>暗</font>", 0x40: "<font color='DarkGoldenRod'>神</font>"}
        linkmarkers = {0x40:"[↖]", 0x80:"[↑]", 0x100:"[↗]", 0x8:"[←]", 0x20:"[→]", 0x1: "[↙]", 0x2:"[↓]", 0x4:"[↘]"}
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
        self.open_bar.triggered.connect(self.openfile)
        bar.addAction(self.open_bar)
        self.save_bar = QAction("保存(&S)",self)
        self.save_bar.setShortcut("Ctrl+S")
        self.save_bar.triggered.connect(self.savefile)
        bar.addAction(self.save_bar)
        self.calculator_bar = QAction("计算器",self)
        self.calculator_bar.triggered.connect(self.open_calculator)
        bar.addAction(self.calculator_bar)
        self.about_bar = QAction("关于", self)
        self.about_bar.triggered.connect(self.open_about)
        bar.addAction(self.about_bar)
        self.quit_bar = QAction("退出", self)
        self.quit_bar.triggered.connect(self.close)
        bar.addAction(self.quit_bar)

        # 读取卡片数据库
        self.card_names = []
        self.card_datas = {}
        self.monster_datas = {}
        try:
            if not os.path.exists("cards.cdb"):
                raise
            sql_conn = connect('cards.cdb')
            cur = sql_conn.cursor()
            sel = cur.execute("select * from texts;")
            cur_2 = sql_conn.cursor()
            for row in sel:
                self.card_names.append(row[1])
                if row[1] not in self.card_datas.keys():
                    carddata_search = cur_2.execute("select * from datas where id=%d;"%row[0])
                    searched = False
                    for carddata in carddata_search:
                        searched = True
                        # 生成描述
                        desp = ""
                        # 种类
                        for types in cardtypes.keys():
                            if carddata[4] & types != 0:
                                if desp != "":
                                    desp += "/"
                                desp += cardtypes[types]
                        # 怪兽信息
                        if carddata[4] & 0x1 != 0:
                            # 等阶/Link
                            if carddata[4] & 0x4000000 != 0:
                                desp += " Link-%d"%carddata[7]
                            else:
                                desp += " %d★"%(carddata[7]&0xffff)
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
                            self.monster_datas[row[1]] = monster_ad
                        # 效果换行
                        eff_desp = row[2]
                        eff_desp = re.sub(r"\r\n",r"<br>",eff_desp)
                        desp += "<br>%s"%eff_desp
                        self.card_datas[row[1]] = desp
                    if not searched:
                        continue
            sql_conn.close()
        except Exception as e:
            self.Newcard_List.addItem("无数据库")
            self.Newcard_List.setEnabled(False)
        
        # sub windows
        self.calculate_window = calculator.Calculator()
        self.calculate_window.setdatas(self.monster_datas)
        self.about_window = about.UI_About(version)

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
        self.newfile()

        # 操作部分
        self.copying_operation = {}
        self.Operator_search.textChanged.connect(self.search_operation)
        self.Operator_search.returnPressed.connect(self.search_operation_cycle)
        self.Operator_search_button.clicked.connect(self.search_operation_cycle)
        self.Operator_list.itemSelectionChanged.connect(self.operation_index_changed)
        self.DeleteOpe_Button.clicked.connect(self.remove_operator)
        self.Operator_list.doubleClicked.connect(self.copy_ope)
        self.CopyOpe_Button.clicked.connect(self.copy_ope)
        self.SelectedOpe_list.itemSelectionChanged.connect(self.select_copying)
        self.MoveOpe_Button.clicked.connect(self.paste_operator)

        # 对象部分
        self.Delete_target.clicked.connect(self.remove_from_targets)
        self.Target_list.itemSelectionChanged.connect(self.target_index_changed)
        self.Target_list.doubleClicked.connect(self.remove_from_targets)
        self.MoveCard_Button.clicked.connect(self.ope_movecards)

        # 添加/删除卡片部分
        self.NewCard_line.textChanged.connect(self.search_card)
        self.NewCard_line.returnPressed.connect(self.create_card)
        self.Newcard_List.doubleClicked.connect(self.fix_cardname)
        self.Newcard_List.clicked.connect(self.show_carddesp)
        self.Newcard_List.itemSelectionChanged.connect(self.show_carddesp)
        self.NewCard_Rename_Button.clicked.connect(self.card_rename)
        self.CreateCard_Button.clicked.connect(self.create_card)
        self.EraseCard_Button.clicked.connect(self.erase_targets)

        # 基本分变更部分
        self.AddLP_Button.clicked.connect(self.ope_LPAdd)
        self.DecLP_Button.clicked.connect(self.ope_LPDec)
        self.CgeLP_Button.clicked.connect(self.ope_LPCge)
        self.HalLP_Button.clicked.connect(self.ope_LPHal)

        # 注释部分
        self.Comment_Button.clicked.connect(self.ope_addcomment)
        self.CommentCard_Button.clicked.connect(self.ope_addcarddesp)
        self.Comment_Line.returnPressed.connect(self.comment_enter)

        # 场上的卡片
        for field_id in range(len(self.idx_represent_field)):
            self.idx_represent_field[field_id].itemSelectionChanged.connect(partial(self.select_field, field_id))
            self.idx_represent_field[field_id].clicked.connect(partial(self.select_field, field_id))
            self.idx_represent_field[field_id].doubleClicked.connect(partial(self.target_field, field_id))

    def keyPressEvent(self, event):
        '''键盘事件响应'''
        if event.key() == Qt.Key_Delete:
            # Delete键删除目标
            if self.Target_list.hasFocus():
                self.remove_from_targets()
            # Delete键删除操作
            elif self.Operator_list.hasFocus():
                self.remove_operator()
        # 回车键默认减少LP
        if self.LP_line.hasFocus() and event.key() == Qt.Key_Return:
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
        self.Delete_target.setText("对象中删除")
        self.CreateCard_Button.setText("←添加到对象")
        self.MoveCard_Button.setText("移动对象")
        self.CommentCard_Button.setText("对象注释")
        self.Comment_Button.setText("操作注释")
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
        self.EraseCard_Button.setText("移除对象")
        for idx in range(len(idx_represent_str)):
            self.Dest_Box.setItemText(idx, idx_represent_str[idx])
        self.label_cardsearch.setText("卡片搜索")
        self.DeleteOpe_Button.setText("删除操作")
        self.CopyOpe_Button.setText("复制操作")
        self.MoveOpe_Button.setText("粘贴操作")
        self.LPTarget_Box.setItemText(0, "己方")
        self.LPTarget_Box.setItemText(1, "对方")
        self.AddLP_Button.setText("增加基本分")
        self.DecLP_Button.setText("减少基本分")
        self.CgeLP_Button.setText("变成基本分")
        self.HalLP_Button.setText("基本分减半")
        self.NewCard_Rename_Button.setText("重命名选定卡")
        self.Operator_search_button.setText("↓")

    def maketitle(self):
        '''根据当前正在打开的文件修改窗口标题'''
        title_name = "DuelEditor - %s"%self.filename
        if self.unsave_changed:
            title_name = "*" + title_name
        self.setWindowTitle(title_name)

    def newfile(self):
        if self.unsave_confirm():
            return
        self.operators = {"cardindex":0, "cards":{}, "operations":[]}
        self.fields = {0:deepcopy(init_field)}
        self.targets = []
        self.copying_operation = {}
        self.filename = "Untitle.json"
        self.last_text = ""
        self.showing_card_id = None
        self.unsave_changed = False

        self.maketitle()
        self.update_operationlist()
        self.update_copying()
        self.refresh_field()
        self.update_targetlist()
        self.show_cardinfo()
        self.search_card()

    def openfile(self):
        '''打开文件'''
        if self.unsave_confirm():
            return
        fullname = str(QFileDialog.getOpenFileName(self, '选择打开的文件',filter="*.json")[0])
        if len(fullname) == 0:
            return
        origin_data = deepcopy(self.operators)
        try:
            with open(fullname,'r') as f:
                json_data = f.read()
                dict_data = loads(json_data)
                self.operators = dict_data
                self.make_fields()
                self.update_operationlist()
                self.Operator_list.setCurrentRow(len(self.operators["operations"])-1)
                self.filename = os.path.split(fullname)[-1]
                self.unsave_changed = False
                self.maketitle()
                return
        # 出错时尝试使用utf-8编码打开文件
        except:
            try:
                with open(fullname,'r',encoding='utf-8') as f:
                    json_data = f.read()
                    dict_data = loads(json_data)
                    self.operators = dict_data
                    self.make_fields()
                    self.update_operationlist()
                    self.Operator_list.setCurrentRow(len(self.operators["operations"])-1)
                    self.filename = os.path.split(fullname)[-1]
                    self.unsave_changed = False
                    self.maketitle()
                    return
            except:
                pass
        self.operators = origin_data
        self.make_fields()
        QMessageBox.warning(self, "提示", "打开失败！", QMessageBox.Yes)

    def unsave_confirm(self):
        '''如果取消动作，则返回True，否则返回False'''
        if self.unsave_changed:
            reply = QMessageBox.warning(self, '保存', "是否保存当前文件'%s'？"%self.filename, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return True
            if reply == QMessageBox.Yes:
                self.savefile()
        return False
    
    def savefile(self):
        '''保存文件'''
        fullname = str(QFileDialog.getSaveFileName(self,'保存为', self.filename,"*.json")[0])
        if len(fullname) == 0:
            return
        self.filename = os.path.split(fullname)[-1]
        json_data = dumps(self.operators,indent=2,ensure_ascii=False)
        with open(fullname,'w',encoding='utf-8') as f:
            f.write(json_data)
            QMessageBox.warning(self, "提示", "保存成功！", QMessageBox.Yes)
            self.unsave_changed = False
            self.maketitle()

    def make_fields(self, begin_at=0):
        '''根据操作生成各操作的场地
        
        若begin_at为0，则从初始场地开始生成，否则从第begin_at个动作后开始生成场地'''
        # 获取场地
        if begin_at == 0:
            self.fields.clear()
            lastest_field = deepcopy(init_field)
        else:
            lastest_field = deepcopy(self.fields[begin_at-1])
        # 遍历操作
        for idx in range(begin_at, len(self.operators["operations"])):
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
        if ope_id == 0:
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
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            ope_id = 0
        else:
            ope_id = ope_id[0].row()
        return self.fields[ope_id]

    def insert_operation(self, operation):
        '''插入操作。操作格式：\n\ntype(str), args(list of int), dest(int), desp(str)'''
        # 判断是插入或新增
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            self.operators["operations"].append(operation)
            ope_id = 0
        else:
            ope_id = ope_id[0].row()+1
            self.operators["operations"].insert(ope_id, operation)
        self.make_fields(ope_id)
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
            self.Target_detail.setText("")
            return
        if card_id not in self.operators["cards"]:
            return
        card_name = self.operators["cards"][card_id]["Name"]

        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            search_list = [card_name, card_name[:-1]]
            for name in search_list:
                if name in self.card_datas:
                    text = "[%s]<br>%s"%(name, self.card_datas[name])
                    self.Target_detail.setHtml(text)
                    return

        self.showing_card_id = card_id
        field = self.get_current_field()
        card_locat = "未知"
        card_desp = "无"
        if card_id in field["locations"]:
            card_locat = idx_represent_str[field["locations"][card_id]]
        if card_id in field["desp"]:
            card_desp = field["desp"][card_id]
        result = "[%s]\n位置：%s\n备注：%s"%(card_name, card_locat, card_desp)
        self.Target_detail.setText(result)
    
    def show_opeinfo(self, idx=None):
        '''显示指定操作详情\n\nidx为空时，显示选定操作的详情'''
        # 获取操作
        self.showing_card_id = None
        if idx is None:
            idx = self.Operator_list.selectedIndexes()
            if len(idx) < 1:
                return
            idx = idx[0].row()
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
        self.Target_detail.setText(result)

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
        self.label_target_list.setText("操作对象(%d)"%len(self.targets))
        self.Target_detail.clear()
        self.update_targetlist()

    def remove_operator(self):
        '''移除操作'''
        # 从操作列表中获得当前选定的操作
        idx = self.Operator_list.selectedIndexes()
        if len(idx) < 1:
            return
        # 确认提示
        reply = QMessageBox.information(self, 'Confirm', "确认要删除吗？该操作不可逆。", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        idx = idx[0].row()
        self.unsave_changed = True
        self.maketitle()
        del self.operators["operations"][idx]
        self.make_fields(idx)
        self.update_operationlist()
        if len(self.operators["operations"]) > 0 and idx == 0:
            self.Operator_list.setCurrentRow(0)
        else:
            self.Operator_list.setCurrentRow(idx-1)
        self.show_opeinfo()

    def paste_operator(self):
        '''粘贴操作'''
        if self.copying_operation == {}:
            return
        self.insert_operation(self.copying_operation)
        self.copying_operation = {}
        self.update_copying()

    def copy_ope(self):
        '''复制操作'''
        idx = self.Operator_list.selectedIndexes()
        if len(idx) < 1:
            return
        idx = idx[0].row()
        ope = deepcopy(self.operators["operations"][idx])
        self.copying_operation = ope
        self.update_copying()
    
    def update_copying(self):
        '''描绘复制中的操作'''
        self.SelectedOpe_list.clear()
        operation = self.copying_operation
        # 判断当前是否有复制中的操作
        if self.copying_operation == {}:
            self.MoveOpe_Button.setEnabled(False)
            self.SelectedOpe_list.addItem("无操作")
            self.SelectedOpe_list.setEnabled(False)
            return
        self.MoveOpe_Button.setEnabled(True)
        self.SelectedOpe_list.setEnabled(True)

        # 根据类型描绘操作
        if operation["type"] == "move":
            card_idx = operation["args"][0]
            card_name = self.operators["cards"][card_idx]["Name"]
            if len(operation["args"])>1:
                card_name += "等"
            result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
            self.SelectedOpe_list.addItem(result)
        elif operation["type"] == "carddesp":
            card_idx = operation["args"][0]
            card_name = self.operators["cards"][card_idx]["Name"]
            if len(operation["args"])>1:
                card_name += "等"
            result = "%s %s"%(card_name, operation["desp"])
            self.SelectedOpe_list.addItem(result)
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
            self.SelectedOpe_list.addItem(result)
        elif operation["type"] == "comment":
            self.SelectedOpe_list.addItem(operation["desp"])
            # 注释高亮
            self.SelectedOpe_list.item(0).setForeground(QColor('green'))
        elif operation["type"] == "erase":
            card_idx = operation["args"][0]
            card_name = self.operators["cards"][card_idx]["Name"]
            if len(operation["args"])>1:
                card_name += "等"
            result = "%s 被移除"%(card_name)
            self.SelectedOpe_list.addItem(result)

    def select_copying(self):
        '''选择复制中的操作时，显示内容'''
        if self.copying_operation == {}:
            return
        operation = self.copying_operation
        if operation != {}:
            result = ""
            if operation["type"] == "move":
                card_name = ""
                first_card = True
                for card_idx in operation["args"]:
                    if not first_card:
                        card_name += "、\n"
                    first_card = False
                    card_name += "%s"%(self.operators["cards"][card_idx]["Name"])
                result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
            elif operation["type"] == "carddesp":
                card_name = ""
                first_card = True
                for card_idx in operation["args"]:
                    if not first_card:
                        card_name += "、\n"
                    first_card = False
                    card_name += "%s"%(self.operators["cards"][card_idx]["Name"])
                result = "%s %s"%(card_name, operation["desp"])
            elif operation["type"] == "erase":
                card_name = ""
                first_card = True
                for card_idx in operation["args"]:
                    if not first_card:
                        card_name += "、\n"
                    first_card = False
                    card_name += "%s"%(self.operators["cards"][card_idx]["Name"])
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
            self.Target_detail.setText(result)

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
        self.SelectedOpe_list.clearSelection()
        self.refresh_field()
        self.update_targetlist()
        self.show_opeinfo()
        self.update_operation_label()

    def update_targetlist(self):
        '''更新对象列表'''
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            ope_id = 0
        else:
            ope_id = ope_id[0].row()
        
        # 按钮禁用/恢复
        if len(self.targets) == 0:
            self.MoveCard_Button.setEnabled(False)
            self.EraseCard_Button.setEnabled(False)
            self.CommentCard_Button.setEnabled(False)
        else:
            self.MoveCard_Button.setEnabled(True)
            self.EraseCard_Button.setEnabled(True)
            self.CommentCard_Button.setEnabled(True)

        self.Target_list.clear()
        searching_name = self.NewCard_line.text()
        for target in self.targets:
            target_name = self.operators["cards"][target]["Name"]
            target_field = self.get_last_location(target, ope_id+1)
            self.Target_list.addItem("[%s]%s"%(target_field, target_name))
            # 如果和搜索栏内容匹配则变色
            if len(searching_name) > 0 and searching_name in target_name:
                self.Target_list.item(self.Target_list.count()-1).setForeground(QColor('red'))
    
    def update_operationlist(self):
        '''操作格式：\n\ntype(str), args(list of int), dest(int), desp(str)
        
        因为需要读取场地来判断LP是否归零，因此需要在调用make_fields()后再调用该函数'''
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
                # 判断是否导致基本分归零
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
        self.update_operation_label()

    def update_operation_label(self):
        '''刷新显示的操作列表信息'''
        ope_count = len(self.operators["operations"])
        ope_index_list = self.Operator_list.selectedIndexes()
        if len(ope_index_list) == 0:
            ope_index = 0
        else:
            ope_index = ope_index_list[0].row()+1
        self.label_operation_list.setText("操作列表(%d/%d)"%(ope_index, ope_count))

    def refresh_field(self):
        '''刷新场地'''
        for cardlist in self.idx_represent_field:
            cardlist.clear()
        
        # 获取最后一步操作
        idx = self.Operator_list.selectedIndexes()
        if len(idx) < 1:
            operation = {"type":"None", "args":[]}
        else:
            idx = idx[0].row()
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
        label_colors = ["QLabel{color:rgb(0,0,0,255)}",
                        "QLabel{color:rgb(0,0,0,255)}",
                        "QLabel{color:rgb(0,0,0,255)}",
                        "QLabel{color:rgb(0,0,0,255)}",
                        "QLabel{color:rgb(0,0,0,255)}",
                        "QLabel{color:rgb(0,0,0,255)}",
                        "QLabel{color:rgb(0,0,0,255)}",
                        "QLabel{color:rgb(0,0,0,255)}"]
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
                # 若为最后操作对象之一，绿色高亮
                if card_id in operation["args"]:
                    show_list.item(show_list.count()-1).setForeground(QColor('green'))
                else:
                    show_list.item(show_list.count()-1).setForeground(QColor('black'))
                # 若符合搜索对象，红色高亮
                if len(searching_name) > 0 and searching_name in card_name:
                    show_list.item(show_list.count()-1).setForeground(QColor('red'))
                    if frame in searched_frames:
                        label_colors[searched_frames.index(frame)] = "QLabel{color:rgb(255,0,102,255)}"
        
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
        self.Target_detail.setText("")
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
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            ope_id = 0
        else:
            ope_id = ope_id[0].row()

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
        self.Target_detail.setText("")
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
        # 遍历搜索符合条件的卡片
        for cardname in self.card_datas.keys():
            if text == cardname:
                hit.append(cardname)
            elif text in cardname:
                hit_in_name.append(cardname)
            elif text in self.card_datas[cardname]:
                hit_in_effect.append(cardname)
        # 添加到列表
        for name in hit:
            self.Newcard_List.addItem(name)
            self.Newcard_List.item(self.Newcard_List.count()-1).setForeground(QColor('green'))
        for name in hit_in_name:
            self.Newcard_List.addItem(name)
        for name in hit_in_effect:
            self.Newcard_List.addItem(name)
            self.Newcard_List.item(self.Newcard_List.count()-1).setForeground(QColor('grey'))
    
    def search_operation_cycle(self):
        self.search_operation(True)

    def search_operation(self, cycle=False):
        text = self.Operator_search.text()
        if text == "":
            return
        
        current_index = self.Operator_list.selectedIndexes()
        if len(current_index) < 1:
            return
        current_index = current_index[0].row()
        if not cycle:
            current_index = 0

        index_pointer = (current_index + 1) % self.Operator_list.count()
        while(index_pointer != current_index):
            if text in self.Operator_list.item(index_pointer).text():
                self.Operator_list.setCurrentRow(index_pointer)
                return
            index_pointer = (index_pointer + 1) % self.Operator_list.count()

    def show_carddesp(self):
        idx = self.Newcard_List.selectedIndexes()
        if len(idx) < 1:
            return
        cardname = self.Newcard_List.item(idx[0].row()).text()
        if cardname in self.card_datas:
            text = "[%s]<br>%s"%(cardname, self.card_datas[cardname])
            self.Target_detail.setHtml(text)

    def fix_cardname(self,qindex):
        '''补全卡名'''
        index = qindex.row()
        if index < 0:
            return
        self.NewCard_line.setText(self.Newcard_List.item(index).text())

    def card_rename(self):
        '''卡片重命名'''
        if self.showing_card_id is None:
            return
        text = self.NewCard_line.text()
        if len(text) == 0:
            return
        # 提示
        reply = QMessageBox.warning(self, '提示', "是否要把[%s]重命名为[%s]？"%(self.operators["cards"][self.showing_card_id]["Name"],text), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # 修改卡片信息
        ope_idx = self.Operator_list.selectedIndexes()
        if len(ope_idx) < 1:
            return
        ope_idx = ope_idx[0].row()

        # 刷新
        self.operators["cards"][self.showing_card_id]["Name"] = text
        self.unsave_changed = True
        self.maketitle()
        self.update_operationlist()
        self.Operator_list.setCurrentRow(ope_idx)
        self.refresh_field()
        self.update_targetlist()
        self.show_cardinfo(self.showing_card_id)
        self.search_card()
    
    def open_calculator(self):
        '''打开计算器'''
        self.calculate_window.show()
    
    def open_about(self):
        '''打开关于窗口'''
        self.about_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = Ui_MainWindow()

    m_window.show()
    sys.exit(app.exec_())