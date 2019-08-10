#encoding:utf-8
import sys
from json import loads, dumps
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QTextBrowser, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import QRect, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QColor
from functools import partial
from copy import deepcopy
import os
from sqlite3 import connect

idx_represent_str = ["己方手卡", "己方魔陷_1", "己方魔陷_2", "己方魔陷_3", "己方魔陷_4", "己方魔陷_5", "己方场地", "己方灵摆_1", "己方灵摆_2", "己方怪兽_1", "己方怪兽_2", "己方怪兽_3", "己方怪兽_4", "己方怪兽_5", "己方墓地", "己方除外", "己方额外", "对方手卡", "对方魔陷_1", "对方魔陷_2", "对方魔陷_3", "对方魔陷_4", "对方魔陷_5", "对方场地", "对方灵摆_1", "对方灵摆_2", "对方怪兽_1", "对方怪兽_2", "对方怪兽_3", "对方怪兽_4", "对方怪兽_5", "对方墓地", "对方除外", "对方额外", "额外怪兽区_1", "额外怪兽区_2"]

class Ui_OSelector(QWidget):
    def __init__(self):
        super(Ui_OSelector, self).__init__()
        self.result = -1
        self.setObjectName("Ui_OSelector")
        self.resize(439, 342)
        self.setFixedSize(439, 342)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.Confirm_Buttom = QPushButton(self.centralwidget)
        self.Confirm_Buttom.setGeometry(QRect(200, 280, 91, 28))
        self.Confirm_Buttom.setObjectName("Confirm_Buttom")
        self.Delete_Buttom = QPushButton(self.centralwidget)
        self.Delete_Buttom.setGeometry(QRect(330, 280, 91, 28))
        self.Delete_Buttom.setObjectName("Delete_Buttom")
        self.Operator_detail = QTextBrowser(self.centralwidget)
        self.Operator_detail.setGeometry(QRect(200, 10, 231, 261))
        self.Operator_detail.setObjectName("textBrowser")
        self.Operator_list = QListWidget(self.centralwidget)
        self.Operator_list.setGeometry(QRect(0, 10, 191, 301))
        self.Operator_list.setObjectName("listView")

        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("选择要插入到的位置")
        self.Confirm_Buttom.setText("确定")
        self.Delete_Buttom.setText("取消")

    def set_status(self, datas):
        self.operators = deepcopy(datas)
        self.show_list()

    def show_list(self):
        self.Operator_list.clear()
        for operation in self.operators["operations"]:
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
            elif operation["type"] == "comment":
                self.Operator_list.addItem(operation["desp"])
            elif operation["type"] == "erase":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s 被移除"%(card_name)
                self.Operator_list.addItem(result)

    def show_opeinfo(self, idx=None):
        if idx is None:
            idx = self.Operator_list.selectedIndexes()
            if len(idx) < 1:
                return
            idx = idx[0].row()
        operation = self.operators["operations"][idx]
        if operation["type"] == "move":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
            self.Operator_detail.setText(result)
        elif operation["type"] == "carddesp":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、"
                first_card = False
                card_name += self.operators["cards"][card_idx]["Name"]
            result = "%s %s"%(card_name, operation["desp"])
            self.Operator_detail.setText(result)
        elif operation["type"] == "erase":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、"
                first_card = False
                card_name += self.operators["cards"][card_idx]["Name"]
            result = "%s 被移除"%(card_name)
            self.Operator_detail.setText(result)
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
            self.Operator_detail.setText(result)
        elif operation["type"] == "comment":
            self.Operator_detail.setText(operation["desp"])

    def get_result(self):
        return self.result
    
    def confirm(self):
        idx = self.Operator_list.selectedIndexes()
        if len(idx) == 0:
            result = -1
        else:
            result = idx[0].row()
        self.close()
    
    def refuse(self):
        self.close()

    @staticmethod
    def get_index():
        dialog=Ui_OSelector()
        result=dialog.exec_()
        return dialog.get_result()

class Ui_MainWindow(QWidget):
    def labelset(self):
        self.label_ope = QLabel(self.centralwidget)
        self.label_ope.setGeometry(QRect(1190, 0, 41, 16))
        self.label_ope.setObjectName("label_ope")
        self.label_target = QLabel(self.centralwidget)
        self.label_target.setGeometry(QRect(870, 0, 81, 20))
        self.label_target.setObjectName("label_target")
        self.label_self_ex = QLabel(self.DuelFrame)
        self.label_self_ex.setGeometry(QRect(10, 470, 141, 20))
        self.label_self_ex.setAlignment(Qt.AlignCenter)
        self.label_self_ex.setObjectName("label_self_hands")
        self.label_self__hands = QLabel(self.DuelFrame)
        self.label_self__hands.setGeometry(QRect(220, 470, 141, 20))
        self.label_self__hands.setAlignment(Qt.AlignCenter)
        self.label_self__hands.setObjectName("label_self_hand")
        self.label_self_hands_3 = QLabel(self.DuelFrame)
        self.label_self_hands_3.setGeometry(QRect(710, 390, 81, 20))
        self.label_self_hands_3.setObjectName("label_self_hands_3")
        self.label_self_hands_9 = QLabel(self.DuelFrame)
        self.label_self_hands_9.setGeometry(QRect(30, 390, 81, 20))
        self.label_self_hands_9.setObjectName("label_self_hands_9")
        self.label_self_hands_10 = QLabel(self.DuelFrame)
        self.label_self_hands_10.setGeometry(QRect(30, 310, 81, 20))
        self.label_self_hands_10.setObjectName("label_self_hands_10")
        self.label_self_hands_11 = QLabel(self.DuelFrame)
        self.label_self_hands_11.setGeometry(QRect(710, 330, 81, 20))
        self.label_self_hands_11.setObjectName("label_self_hands_11")
        self.label_self_grave = QLabel(self.DuelFrame)
        self.label_self_grave.setGeometry(QRect(440, 470, 141, 20))
        self.label_self_grave.setAlignment(Qt.AlignCenter)
        self.label_self_grave.setObjectName("label_self_grave")
        self.label_self_banish = QLabel(self.DuelFrame)
        self.label_self_banish.setGeometry(QRect(650, 470, 141, 20))
        self.label_self_banish.setAlignment(Qt.AlignCenter)
        self.label_self_banish.setObjectName("label_self_banish")
        self.label_self_hands_16 = QLabel(self.DuelFrame)
        self.label_self_hands_16.setGeometry(QRect(30, 160, 81, 20))
        self.label_self_hands_16.setObjectName("label_self_hands_16")
        self.label_self_hands_18 = QLabel(self.DuelFrame)
        self.label_self_hands_18.setGeometry(QRect(710, 240, 81, 20))
        self.label_self_hands_18.setObjectName("label_self_hands_18")
        self.label_enemy_grave = QLabel(self.DuelFrame)
        self.label_enemy_grave.setGeometry(QRect(440, 10, 141, 20))
        self.label_enemy_grave.setAlignment(Qt.AlignCenter)
        self.label_enemy_grave.setObjectName("label_enemy_grave")
        self.label_enemy_hand = QLabel(self.DuelFrame)
        self.label_enemy_hand.setGeometry(QRect(220, 10, 141, 20))
        self.label_enemy_hand.setAlignment(Qt.AlignCenter)
        self.label_enemy_hand.setObjectName("label_enemy_hand")
        self.label_enemy_ex = QLabel(self.DuelFrame)
        self.label_enemy_ex.setGeometry(QRect(10, 10, 141, 20))
        self.label_enemy_ex.setAlignment(Qt.AlignCenter)
        self.label_enemy_ex.setObjectName("label_enemy_ex")
        self.label_enemy_banish = QLabel(self.DuelFrame)
        self.label_enemy_banish.setGeometry(QRect(650, 10, 141, 20))
        self.label_enemy_banish.setAlignment(Qt.AlignCenter)
        self.label_enemy_banish.setObjectName("label_enemy_banish")
        self.label_self_hands_19 = QLabel(self.DuelFrame)
        self.label_self_hands_19.setGeometry(QRect(710, 160, 81, 20))
        self.label_self_hands_19.setObjectName("label_self_hands_19")
        self.label_self_hand1 = QLabel(self.DuelFrame)
        self.label_self_hand1.setGeometry(QRect(30, 240, 81, 20))
        self.label_self_hand1.setObjectName("label_self_hand1")
        self.label_target_2 = QLabel(self.centralwidget)
        self.label_target_2.setGeometry(QRect(1010, 0, 81, 20))
        self.label_target_2.setObjectName("label_target_2")

    def init_frame(self):
        self.setObjectName("MainWindow")
        self.resize(1306, 639)
        self.setFixedSize(1306, 639)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.DuelFrame = QWidget(self.centralwidget)
        self.DuelFrame.setGeometry(QRect(10, 0, 811, 631))
        self.DuelFrame.setObjectName("DuelFrame")
        self.labelset()

        self.Operator_list = QListWidget(self.centralwidget)
        self.Operator_list.setGeometry(QRect(1120, 20, 181, 351))
        self.Operator_list.setObjectName("Operator_list")
        self.Operator_detail = QTextBrowser(self.centralwidget)
        self.Operator_detail.setGeometry(QRect(1120, 380, 181, 151))
        self.Operator_detail.setObjectName("Operator_detail")
        self.Operator_detail.setWordWrapMode(True)
        self.Target_list = QListWidget(self.centralwidget)
        self.Target_list.setGeometry(QRect(830, 20, 141, 251))
        self.Target_list.setObjectName("Target_list")
        self.Delete_target = QPushButton(self.centralwidget)
        self.Delete_target.setGeometry(QRect(830, 280, 141, 28))
        self.Delete_target.setObjectName("Delete_target")
        self.Target_detail = QTextBrowser(self.centralwidget)
        self.Target_detail.setGeometry(QRect(830, 420, 141, 141))
        self.Target_detail.setObjectName("Target_detail")
        self.CreateCard_Button = QPushButton(self.centralwidget)
        self.CreateCard_Button.setGeometry(QRect(980, 280, 131, 28))
        self.CreateCard_Button.setObjectName("CreateCard_Button")
        self.MoveCard_Button = QPushButton(self.centralwidget)
        self.MoveCard_Button.setGeometry(QRect(830, 350, 141, 28))
        self.MoveCard_Button.setObjectName("MoveCard_Button")
        self.CommentCard_Button = QPushButton(self.centralwidget)
        self.CommentCard_Button.setGeometry(QRect(980, 350, 131, 28))
        self.CommentCard_Button.setObjectName("CommentCard_Button")
        self.Comment_Button = QPushButton(self.centralwidget)
        self.Comment_Button.setGeometry(QRect(980, 380, 131, 28))
        self.Comment_Button.setObjectName("Comment_Button")
        self.Self_Ex = QListWidget(self.DuelFrame)
        self.Self_Ex.setGeometry(QRect(10, 500, 141, 121))
        self.Self_Ex.setObjectName("Self_Ex")
        self.Self_Hand = QListWidget(self.DuelFrame)
        self.Self_Hand.setGeometry(QRect(220, 500, 141, 121))
        self.Self_Hand.setObjectName("Self_Hand")
        self.Self_S1 = QListWidget(self.DuelFrame)
        self.Self_S1.setGeometry(QRect(130, 410, 111, 51))
        self.Self_S1.setObjectName("Self_S1")
        self.Self_S2 = QListWidget(self.DuelFrame)
        self.Self_S2.setGeometry(QRect(240, 410, 111, 51))
        self.Self_S2.setObjectName("Self_S2")
        self.Self_S3 = QListWidget(self.DuelFrame)
        self.Self_S3.setGeometry(QRect(350, 410, 111, 51))
        self.Self_S3.setObjectName("Self_S3")
        self.Self_S4 = QListWidget(self.DuelFrame)
        self.Self_S4.setGeometry(QRect(460, 410, 111, 51))
        self.Self_S4.setObjectName("Self_S4")
        self.Self_S5 = QListWidget(self.DuelFrame)
        self.Self_S5.setGeometry(QRect(570, 410, 111, 51))
        self.Self_S5.setObjectName("Self_S5")
        self.Self_P2 = QListWidget(self.DuelFrame)
        self.Self_P2.setGeometry(QRect(690, 420, 111, 41))
        self.Self_P2.setObjectName("Self_P2")
        self.Self_P1 = QListWidget(self.DuelFrame)
        self.Self_P1.setGeometry(QRect(10, 420, 111, 41))
        self.Self_P1.setObjectName("Self_P1")
        self.Self_Field = QListWidget(self.DuelFrame)
        self.Self_Field.setGeometry(QRect(10, 340, 111, 41))
        self.Self_Field.setObjectName("Self_Field")
        self.Self_LP = QLineEdit(self.DuelFrame)
        self.Self_LP.setText("8000")
        self.Self_LP.setEnabled(False)
        self.Self_LP.setGeometry(QRect(690, 360, 111, 21))
        self.Self_LP.setObjectName("Self_LP")
        self.Self_M5 = QListWidget(self.DuelFrame)
        self.Self_M5.setGeometry(QRect(570, 360, 111, 51))
        self.Self_M5.setObjectName("Self_M5")
        self.Self_M1 = QListWidget(self.DuelFrame)
        self.Self_M1.setGeometry(QRect(130, 360, 111, 51))
        self.Self_M1.setObjectName("Self_M1")
        self.Self_M2 = QListWidget(self.DuelFrame)
        self.Self_M2.setGeometry(QRect(240, 360, 111, 51))
        self.Self_M2.setObjectName("Self_M2")
        self.Self_M4 = QListWidget(self.DuelFrame)
        self.Self_M4.setGeometry(QRect(460, 360, 111, 51))
        self.Self_M4.setObjectName("Self_M4")
        self.Self_M3 = QListWidget(self.DuelFrame)
        self.Self_M3.setGeometry(QRect(350, 360, 111, 51))
        self.Self_M3.setObjectName("Self_M3")
        self.Self_Grave = QListWidget(self.DuelFrame)
        self.Self_Grave.setGeometry(QRect(440, 500, 141, 121))
        self.Self_Grave.setObjectName("Self_Grave")
        self.Self_Banish = QListWidget(self.DuelFrame)
        self.Self_Banish.setGeometry(QRect(650, 500, 141, 121))
        self.Self_Banish.setObjectName("Self_Banish")
        self.Enemy_P1 = QListWidget(self.DuelFrame)
        self.Enemy_P1.setGeometry(QRect(690, 190, 111, 41))
        self.Enemy_P1.setObjectName("Enemy_P1")
        self.Enemy_M4 = QListWidget(self.DuelFrame)
        self.Enemy_M4.setGeometry(QRect(240, 240, 111, 51))
        self.Enemy_M4.setObjectName("Enemy_M4")
        self.Enemy_S3 = QListWidget(self.DuelFrame)
        self.Enemy_S3.setGeometry(QRect(350, 190, 111, 51))
        self.Enemy_S3.setObjectName("Enemy_S3")
        self.ExM_2 = QListWidget(self.DuelFrame)
        self.ExM_2.setGeometry(QRect(460, 300, 111, 51))
        self.ExM_2.setObjectName("ExM_2")
        self.Enemy_LP = QLineEdit(self.DuelFrame)
        self.Enemy_LP.setGeometry(QRect(10, 270, 111, 21))
        self.Enemy_LP.setObjectName("Enemy_LP")
        self.Enemy_LP.setText("8000")
        self.Enemy_LP.setEnabled(False)
        self.Enemy_Field = QListWidget(self.DuelFrame)
        self.Enemy_Field.setGeometry(QRect(690, 270, 111, 41))
        self.Enemy_Field.setObjectName("Enemy_Field")
        self.Enemy_P2 = QListWidget(self.DuelFrame)
        self.Enemy_P2.setGeometry(QRect(10, 190, 111, 41))
        self.Enemy_P2.setObjectName("Enemy_P2")
        self.Enemy_S2 = QListWidget(self.DuelFrame)
        self.Enemy_S2.setGeometry(QRect(460, 190, 111, 51))
        self.Enemy_S2.setObjectName("Enemy_S2")
        self.ExM_1 = QListWidget(self.DuelFrame)
        self.ExM_1.setGeometry(QRect(240, 300, 111, 51))
        self.ExM_1.setObjectName("ExM_1")
        self.Enemy_M2 = QListWidget(self.DuelFrame)
        self.Enemy_M2.setGeometry(QRect(460, 240, 111, 51))
        self.Enemy_M2.setObjectName("Enemy_M2")
        self.Enemy_M1 = QListWidget(self.DuelFrame)
        self.Enemy_M1.setGeometry(QRect(570, 240, 111, 51))
        self.Enemy_M1.setObjectName("Enemy_M1")

        self.Enemy_S4 = QListWidget(self.DuelFrame)
        self.Enemy_S4.setGeometry(QRect(240, 190, 111, 51))
        self.Enemy_S4.setObjectName("Enemy_S4")
        self.Enemy_S1 = QListWidget(self.DuelFrame)
        self.Enemy_S1.setGeometry(QRect(570, 190, 111, 51))
        self.Enemy_S1.setObjectName("Enemy_S1")
        self.Enemy_S5 = QListWidget(self.DuelFrame)
        self.Enemy_S5.setGeometry(QRect(130, 190, 111, 51))
        self.Enemy_S5.setObjectName("Enemy_S5")
        self.Enemy_M5 = QListWidget(self.DuelFrame)
        self.Enemy_M5.setGeometry(QRect(130, 240, 111, 51))
        self.Enemy_M5.setObjectName("Enemy_M5")
        self.Enemy_M3 = QListWidget(self.DuelFrame)
        self.Enemy_M3.setGeometry(QRect(350, 240, 111, 51))
        self.Enemy_M3.setObjectName("Enemy_M3")
        self.Enemy_Banish = QListWidget(self.DuelFrame)
        self.Enemy_Banish.setGeometry(QRect(650, 40, 141, 121))
        self.Enemy_Banish.setObjectName("Enemy_Banish")
        self.Enemy_Ex = QListWidget(self.DuelFrame)
        self.Enemy_Ex.setGeometry(QRect(10, 40, 141, 121))
        self.Enemy_Ex.setObjectName("Enemy_Ex")
        self.Enemy_Hand = QListWidget(self.DuelFrame)
        self.Enemy_Hand.setGeometry(QRect(220, 40, 141, 121))
        self.Enemy_Hand.setObjectName("Enemy_Hand")
        self.Enemy_Grave = QListWidget(self.DuelFrame)
        self.Enemy_Grave.setGeometry(QRect(440, 40, 141, 121))
        self.Enemy_Grave.setObjectName("Enemy_Grave")
        self.Open_Buttom = QPushButton(self.DuelFrame)
        self.Open_Buttom.setGeometry(QRect(140, 310, 91, 28))
        self.Open_Buttom.setObjectName("Open_Buttom")
        self.Save_Buttom = QPushButton(self.DuelFrame)
        self.Save_Buttom.setGeometry(QRect(580, 310, 91, 28))
        self.Save_Buttom.setObjectName("Save_Buttom")
        self.EraseCard_Button = QPushButton(self.centralwidget)
        self.EraseCard_Button.setGeometry(QRect(830, 380, 141, 28))
        self.EraseCard_Button.setObjectName("EraseCard_Button")
        self.Dest_Box = QComboBox(self.centralwidget)
        self.Dest_Box.setGeometry(QRect(830, 320, 141, 22))
        self.Dest_Box.setObjectName("Dest_Box")
        for i in range(36):
            self.Dest_Box.addItem("")
        self.NewCard_line = QLineEdit(self.centralwidget)
        self.NewCard_line.setGeometry(QRect(980, 20, 131, 21))
        self.NewCard_line.setObjectName("NewCard_line")
        self.Newcard_List = QListWidget(self.centralwidget)
        self.Newcard_List.setGeometry(QRect(980, 50, 131, 221))
        self.Newcard_List.setObjectName("Newcard_List")
        self.DeleteOpe_Button = QPushButton(self.centralwidget)
        self.DeleteOpe_Button.setGeometry(QRect(1120, 540, 181, 28))
        self.DeleteOpe_Button.setObjectName("DeleteOpe_Button")
        self.CopyOpe_Button = QPushButton(self.centralwidget)
        self.CopyOpe_Button.setGeometry(QRect(1120, 570, 181, 28))
        self.CopyOpe_Button.setObjectName("CopyOpe_Button")
        self.MoveOpe_Button = QPushButton(self.centralwidget)
        self.MoveOpe_Button.setGeometry(QRect(1120, 600, 181, 28))
        self.MoveOpe_Button.setObjectName("MoveOpe_Button")
        self.LPTarget_Box = QComboBox(self.centralwidget)
        self.LPTarget_Box.setGeometry(QRect(980, 450, 131, 22))
        self.LPTarget_Box.setObjectName("LPTarget_Box")
        self.LPTarget_Box.addItem("")
        self.LPTarget_Box.addItem("")
        self.LP_line = QLineEdit(self.centralwidget)
        self.LP_line.setGeometry(QRect(980, 480, 131, 21))
        self.LP_line.setObjectName("LP_line")
        regx = QRegExp("^[0-9]{15}$")
        validator = QRegExpValidator(regx, self.LP_line)
        self.LP_line.setValidator(validator)

        self.AddLP_Button = QPushButton(self.centralwidget)
        self.AddLP_Button.setGeometry(QRect(980, 510, 131, 28))
        self.AddLP_Button.setObjectName("AddLP_Button")
        self.DecLP_Button = QPushButton(self.centralwidget)
        self.DecLP_Button.setGeometry(QRect(980, 540, 131, 28))
        self.DecLP_Button.setObjectName("DecLP_Button")
        self.CgeLP_Button = QPushButton(self.centralwidget)
        self.CgeLP_Button.setGeometry(QRect(980, 570, 131, 28))
        self.CgeLP_Button.setObjectName("CgeLP_Button")
        self.HalLP_Button = QPushButton(self.centralwidget)
        self.HalLP_Button.setGeometry(QRect(980, 600, 131, 28))
        self.HalLP_Button.setObjectName("HalLP_Button")
        self.NewCard_Rename = QLineEdit(self.centralwidget)
        self.NewCard_Rename.setGeometry(QRect(830, 570, 141, 21))
        self.NewCard_Rename.setObjectName("NewCard_Rename")
        self.NewCard_Rename_Button = QPushButton(self.centralwidget)
        self.NewCard_Rename_Button.setGeometry(QRect(830, 600, 141, 28))
        self.NewCard_Rename_Button.setObjectName("NewCard_Rename_Button")
        self.Comment_Line = QLineEdit(self.centralwidget)
        self.Comment_Line.setGeometry(QRect(980, 320, 131, 21))
        self.Comment_Line.setObjectName("Comment_Line")

        self.retranslateUi(self)

    def __init__(self):
        idx_represent_str = ["己方手卡", "己方魔陷_1", "己方魔陷_2", "己方魔陷_3", "己方魔陷_4", "己方魔陷_5", "己方场地", "己方灵摆_1", "己方灵摆_2", "己方怪兽_1", "己方怪兽_2", "己方怪兽_3", "己方怪兽_4", "己方怪兽_5", "己方墓地", "己方除外", "己方额外", "对方手卡", "对方魔陷_1", "对方魔陷_2", "对方魔陷_3", "对方魔陷_4", "对方魔陷_5", "对方场地", "对方灵摆_1", "对方灵摆_2", "对方怪兽_1", "对方怪兽_2", "对方怪兽_3", "对方怪兽_4", "对方怪兽_5", "对方墓地", "对方除外", "对方额外", "额外怪兽区_1", "额外怪兽区_2"]
        super(Ui_MainWindow, self).__init__()
        self.init_frame()

        # 读取卡片数据库
        self.card_names = []
        try:
            if not os.path.exists("cards.cdb"):
                raise
            sql_conn = connect('cards.cdb')
            cur = sql_conn.cursor()
            sel = cur.execute("select * from texts;")
            for row in sel:
                self.card_names.append(row[1])
            sql_conn.close()
        except Exception as e:
            self.Newcard_List.addItem("无数据库")
            self.Newcard_List.setEnabled(False)

        # 初始化
        self.idx_represent_field = [self.Self_Hand, self.Self_S1, self.Self_S2, self.Self_S3, self.Self_S4, self.Self_S5, self.Self_Field, self.Self_P1, self.Self_P2, self.Self_M1, self.Self_M2, self.Self_M3, self.Self_M4, self.Self_M5, self.Self_Grave, self.Self_Banish, self.Self_Ex, self.Enemy_Hand, self.Enemy_S1, self.Enemy_S2, self.Enemy_S3, self.Enemy_S4, self.Enemy_S5, self.Enemy_Field, self.Enemy_P1, self.Enemy_P2, self.Enemy_M1, self.Enemy_M2, self.Enemy_M3, self.Enemy_M4, self.Enemy_M5, self.Enemy_Grave, self.Enemy_Banish, self.Enemy_Ex, self.ExM_1, self.ExM_2]
        self.operators = {"cardindex":0, "cards":{}, "operations":[]}
        self.fields = {0:{"locations":{}, "desp":{}, "LP":[0,0]}}
        self.targets = []
        self.filename = "Untitle.json"
        self.last_text = ""

        # 打开/保存文件
        self.Open_Buttom.clicked.connect(self.openfile)
        self.Save_Buttom.clicked.connect(self.savefile)

        # 操作部分
        self.Operator_list.itemSelectionChanged.connect(self.operation_index_changed)
        self.DeleteOpe_Button.clicked.connect(self.remove_operator)
        self.CopyOpe_Button.clicked.connect(self.copy_ope)
        # TODO
        self.MoveOpe_Button.setEnabled(False)
        self.MoveOpe_Button.clicked.connect(self.move_operator)

        # 对象部分
        self.Delete_target.clicked.connect(self.remove_from_targets)
        self.Target_list.itemSelectionChanged.connect(self.target_index_changed)
        self.Target_list.doubleClicked.connect(self.remove_from_targets)
        self.MoveCard_Button.clicked.connect(self.ope_movecards)

        # 添加/删除卡片部分
        self.NewCard_line.textChanged.connect(self.search_card)
        self.NewCard_line.returnPressed.connect(self.create_card)
        self.Newcard_List.doubleClicked.connect(self.fix_cardname)
        self.NewCard_Rename_Button.clicked.connect(self.card_rename)
        self.NewCard_Rename.returnPressed.connect(self.card_rename)
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
            self.idx_represent_field[field_id].doubleClicked.connect(partial(self.target_field, field_id))

    def keyPressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_S:
                self.savefile()
            elif event.key() == Qt.Key_O:
                self.openfile()
        if event.key() == Qt.Key_Delete:
            if self.Target_list.hasFocus():
                self.remove_from_targets()
            elif self.Operator_list.hasFocus():
                self.remove_operator()
        if self.LP_line.hasFocus() and event.key() == Qt.Key_Return:
            self.ope_LPDec()
        QWidget.keyPressEvent(self, event)

    def comment_enter(self):
        if len(self.targets) > 0:
            self.ope_addcarddesp()
        else:
            self.ope_addcomment()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("DuelEditor")
        __sortingEnabled = self.Operator_list.isSortingEnabled()
        self.Operator_list.setSortingEnabled(False)

        self.Operator_list.setSortingEnabled(__sortingEnabled)
        self.label_ope.setText("操作")
        self.label_target.setText("操作对象")
        self.Delete_target.setText("对象中删除")
        self.CreateCard_Button.setText("←添加到对象")
        self.MoveCard_Button.setText("移动对象")
        self.CommentCard_Button.setText("对象注释")
        self.Comment_Button.setText("操作注释")
        self.label_self_ex.setText("己方额外")
        self.label_self__hands.setText("己方手卡")
        self.label_self_hands_3.setText("己方右灵摆")
        self.label_self_hands_9.setText("己方左灵摆")
        self.label_self_hands_10.setText("己方场地")
        self.label_self_hands_11.setText("己方基本分")
        self.label_self_grave.setText("己方墓地")
        self.label_self_banish.setText("己方除外")
        self.label_self_hands_16.setText("对方右灵摆")
        self.label_self_hands_18.setText("对方场地")
        self.label_self_hands_19.setText("对方左灵摆")
        self.label_self_hand1.setText("对方基本分")
        self.label_enemy_grave.setText("对方墓地")
        self.label_enemy_hand.setText("对方手卡")
        self.label_enemy_ex.setText("对方额外")
        self.label_enemy_banish.setText("对方除外")
        self.Open_Buttom.setText("打开(O)")
        self.Save_Buttom.setText("保存(S)")
        self.EraseCard_Button.setText("移除对象")
        for idx in range(len(idx_represent_str)):
            self.Dest_Box.setItemText(idx, idx_represent_str[idx])
        self.label_target_2.setText("创建卡片")
        self.DeleteOpe_Button.setText("删除操作")
        self.CopyOpe_Button.setText("复制操作")
        self.MoveOpe_Button.setText("移动操作")
        self.LPTarget_Box.setItemText(0, "己方")
        self.LPTarget_Box.setItemText(1, "对方")
        self.AddLP_Button.setText("增加基本分")
        self.DecLP_Button.setText("减少基本分")
        self.CgeLP_Button.setText("变成基本分")
        self.HalLP_Button.setText("基本分减半")
        self.NewCard_Rename_Button.setText("重命名")

    def openfile(self):
        fullname = str(QFileDialog.getOpenFileName(self, '选择打开的文件',filter="*.json")[0])
        if len(fullname) == 0:
            return
        self.filename = os.path.split(fullname)[-1]
        self.setWindowTitle("DuelEditor - %s"%self.filename)
        with open(fullname,'r') as f:
            json_data = f.read()
            dict_data = loads(json_data)
            self.operators = dict_data
            self.update_operationlist()
            self.make_fields()
            self.Operator_list.setCurrentRow(len(self.operators["operations"])-1)
            return
        QMessageBox.warning(self, "提示", "打开失败！", QMessageBox.Yes)

    def savefile(self):
        fullname = str(QFileDialog.getSaveFileName(self,'保存为', self.filename,"*.json")[0])
        if len(fullname) == 0:
            return
        self.filename = os.path.split(fullname)[-1]
        self.setWindowTitle("DuelEditor - %s"%self.filename)
        json_data = dumps(self.operators,indent=2,ensure_ascii=False)
        with open(fullname,'w') as f:
            f.write(json_data)
            QMessageBox.warning(self, "提示", "保存成功！", QMessageBox.Yes)

    def make_fields(self, begin_at=0):
        '''根据操作生成各操作的场地'''
        if begin_at == 0:
            self.fields.clear()
            lastest_field = {"locations":{}, "desp":{}, "LP":[8000,8000]}
        else:
            lastest_field = deepcopy(self.fields[begin_at-1])
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
            self.fields[idx] = deepcopy(lastest_field)
        if len(self.fields) == 0:
            self.fields[0] = lastest_field

    def get_last_location(self, card_id, ope_id):
        '''获取卡片的上一个位置'''
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

        locations(dict), desp(dict), LP(list)'''
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            ope_id = 0
        else:
            ope_id = ope_id[0].row()
        return self.fields[ope_id]

    def insert_operation(self, operation):
        '''插入操作。格式：\n\ntype(str), args(list of int), dest(int), desp(str)'''
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            self.operators["operations"].append(operation)
            ope_id = 0
        else:
            ope_id = ope_id[0].row()+1
            self.operators["operations"].insert(ope_id, operation)
        self.update_operationlist()
        self.make_fields(ope_id)
        self.Operator_list.setCurrentRow(ope_id)
        self.show_opeinfo()
        #self.Operator_list.setFocus()

    def show_cardinfo(self, card_id):
        '''根据card_id，在信息栏显示卡片详情'''
        if card_id not in self.operators["cards"]:
            return
        self.showing_card_id = card_id
        field = self.get_current_field()
        card_name = self.operators["cards"][card_id]["Name"]
        card_locat = "未知"
        card_desp = "无"
        if card_id in field["locations"]:
            card_locat = idx_represent_str[field["locations"][card_id]]
        if card_id in field["desp"]:
            card_desp = field["desp"][card_id]
        result = "[%s]\n位置：%s\n备注：%s"%(card_name, card_locat, card_desp)
        self.Target_detail.setText(result)
    
    def show_opeinfo(self, idx=None):
        if idx is None:
            idx = self.Operator_list.selectedIndexes()
            if len(idx) < 1:
                return
            idx = idx[0].row()
        operation = self.operators["operations"][idx]
        if operation["type"] == "move":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
            self.Operator_detail.setText(result)
        elif operation["type"] == "carddesp":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s %s"%(card_name, operation["desp"])
            self.Operator_detail.setText(result)
        elif operation["type"] == "erase":
            card_name = ""
            first_card = True
            for card_idx in operation["args"]:
                if not first_card:
                    card_name += "、"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s 被移除"%(card_name)
            self.Operator_detail.setText(result)
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
            self.Operator_detail.setText(result)
        elif operation["type"] == "comment":
            self.Operator_detail.setText(operation["desp"])

    def create_card(self):
        cardname = self.NewCard_line.text()
        self.NewCard_line.setText("")
        if cardname == "":
            return
        idx = str(self.operators["cardindex"])
        self.operators["cardindex"] += 1
        self.operators["cards"][idx] = {"Name": cardname}
        self.targets.append(idx)
        self.update_targetlist()

    def remove_from_targets(self):
        target_idx = self.Target_list.selectedIndexes()
        if len(target_idx) == 0:
            return
        target_idx = target_idx[0].row()
        del self.targets[target_idx]
        self.Target_detail.clear()
        self.update_targetlist()

    def remove_operator(self):
        idx = self.Operator_list.selectedIndexes()
        if len(idx) < 1:
            return
        reply = QMessageBox.information(self, 'Confirm', "确认要删除吗？该操作不可逆。", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        idx = idx[0].row()
        del self.operators["operations"][idx]
        self.make_fields(idx)
        self.update_operationlist()
        self.Operator_list.setCurrentRow(idx-1)
        self.show_opeinfo()

    def move_operator(self):
        dialogue = Ui_OSelector()
        dialogue.set_status(self.operators)
        dialogue.show()
        #runner=dialogue.exec_()
        result=dialogue.get_result()
        print(result)

    def copy_ope(self):
        idx = self.Operator_list.selectedIndexes()
        if len(idx) < 1:
            return
        idx = idx[0].row()
        ope = deepcopy(self.operators["operations"][idx])
        self.insert_operation(ope)

    def target_index_changed(self):
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
        self.refresh_field()
        self.show_opeinfo()

    def update_targetlist(self):
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            ope_id = 0
        else:
            ope_id = ope_id[0].row()
        self.Target_list.clear()
        for target in self.targets:
            target_name = self.operators["cards"][target]["Name"]
            target_field = self.get_last_location(target, ope_id+1)
            self.Target_list.addItem("[%s]%s"%(target_field, target_name))
    
    def update_operationlist(self):
        '''操作格式：\n\ntype(str), args(list of int), dest(int), desp(str)'''
        self.Operator_list.clear()
        for operation in self.operators["operations"]:
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
            elif operation["type"] == "comment":
                self.Operator_list.addItem(operation["desp"])
                self.Operator_list.item(self.Operator_list.count()-1).setForeground(QColor('green'))
            elif operation["type"] == "erase":
                card_idx = operation["args"][0]
                card_name = self.operators["cards"][card_idx]["Name"]
                if len(operation["args"])>1:
                    card_name += "等"
                result = "%s 被移除"%(card_name)
                self.Operator_list.addItem(result)

    def refresh_field(self):
        '''刷新场地'''
        for cardlist in self.idx_represent_field:
            cardlist.clear()
        
        idx = self.Operator_list.selectedIndexes()
        if len(idx) < 1:
            operation = {"type":"None", "args":[]}
        else:
            idx = idx[0].row()
            operation = deepcopy(self.operators["operations"][idx])
        
        field = self.get_current_field()
        self.Self_LP.setText("%d"%field["LP"][0])
        self.Self_LP.setStyleSheet("color:black")
        self.Enemy_LP.setText("%d"%field["LP"][1])
        self.Enemy_LP.setStyleSheet("color:black")
        if operation["type"][0:2] == "LP":
            if operation["args"][0] == 0:
                self.Self_LP.setStyleSheet("color:red")
            else:
                self.Enemy_LP.setStyleSheet("color:red")
        if operation["type"] not in ["move","carddesp"]:
            operation["args"].clear()
        searching_name = self.NewCard_line.text()
        for card_id in field['locations'].keys():
            list_id = field["locations"][card_id]
            show_list = self.idx_represent_field[list_id]
            card_name = self.operators["cards"][card_id]["Name"]
            show_list.addItem(card_name)
            if card_id in operation["args"]:
                show_list.item(show_list.count()-1).setForeground(QColor('green'))
            else:
                show_list.item(show_list.count()-1).setForeground(QColor('black'))
            if len(searching_name) > 0 and searching_name in card_name:
                show_list.item(show_list.count()-1).setForeground(QColor('red'))
        self.label_enemy_ex.setText("对方额外(%d)"%self.Enemy_Ex.count())
        self.label_enemy_hand.setText("对方手卡(%d)"%self.Enemy_Hand.count())
        self.label_enemy_grave.setText("对方墓地(%d)"%self.Enemy_Grave.count())
        self.label_enemy_banish.setText("对方除外(%d)"%self.Enemy_Banish.count())
        self.label_self_ex.setText("己方额外(%d)"%self.Self_Ex.count())
        self.label_self__hands.setText("己方手卡(%d)"%self.Self_Hand.count())
        self.label_self_grave.setText("己方墓地(%d)"%self.Self_Grave.count())
        self.label_self_banish.setText("己方除外(%d)"%self.Self_Banish.count())
 
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
        if len(self.targets) == 0:
            return
        self.Target_detail.setText("")
        ope = {"type":"move", "args":self.targets.copy(), "dest": self.Dest_Box.currentIndex(), "desp":""}
        self.targets.clear()
        self.Target_list.clear()
        self.insert_operation(ope)

    def ope_addcomment(self):
        comment = self.Comment_Line.text()
        if len(comment) == 0:
            return
        ope = {"type":"comment", "args":[], "dest":0, "desp": comment}
        self.insert_operation(ope)
        self.Comment_Line.clear()

    def ope_addcarddesp(self):
        comment = self.Comment_Line.text()
        if len(comment) == 0 or len(self.targets) == 0:
            return
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            ope_id = 0
        else:
            ope_id = ope_id[0].row()
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
        if len(self.targets) == 0:
            return
        reply = QMessageBox.information(self, 'Confirm', "确认要删除吗？\n被删除的卡片在之后的操作中不会再出现。", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        self.Target_detail.setText("")
        ope = {"type":"erase", "args":self.targets.copy(), "dest": 0, "desp":""}
        self.targets.clear()
        self.Target_list.clear()
        self.insert_operation(ope)

    def select_field(self, field_id):
        lst = self.idx_represent_field[field_id]
        selected = lst.selectedIndexes()
        if len(selected) < 1:
            return
        self.Dest_Box.setCurrentIndex(field_id)
        selected = selected[0].row()
        self.Target_list.clearSelection()
        for other_lst in self.idx_represent_field:
            if other_lst != lst:
                other_lst.clearSelection()
        field = self.get_current_field()
        for card_id in field["locations"].keys():
            if field["locations"][card_id] == field_id:
                if selected == 0:
                    self.show_cardinfo(card_id)
                selected -= 1
    
    def target_field(self, field_id):
        lst = self.idx_represent_field[field_id]
        selected = lst.selectedIndexes()
        if len(selected) < 1:
            return
        selected = selected[0].row()
        self.Target_list.clearSelection()
        for other_lst in self.idx_represent_field:
            if other_lst != lst:
                other_lst.clearSelection()
        field = self.get_current_field()
        for card_id in field["locations"].keys():
            if field["locations"][card_id] == field_id:
                if selected == 0:
                    if card_id not in self.targets:
                        self.targets.append(card_id)
                        self.update_targetlist()
                selected -= 1

    def search_card(self):
        if self.last_text != self.NewCard_line.text():
            self.last_text = self.NewCard_line.text()
            self.refresh_field()
        text = self.NewCard_line.text()
        if not self.Newcard_List.isEnabled():
            return
        if len(text) == 0:
            self.Newcard_List.clear()
            return
        self.Newcard_List.clear()
        for cardname in self.card_names:
            if text in cardname:
                self.Newcard_List.addItem(cardname)
    
    def fix_cardname(self,qindex):
        index = qindex.row()
        if index < 0:
            return
        self.NewCard_line.setText(self.Newcard_List.item(index).text())

    def card_rename(self):
        if self.showing_card_id is None:
            return
        text = self.NewCard_Rename.text()
        if len(text) == 0:
            return

        ope_idx = self.Operator_list.selectedIndexes()
        if len(ope_idx) < 1:
            return
        ope_idx = ope_idx[0].row()

        self.operators["cards"][self.showing_card_id]["Name"] = text
        #self.make_fields()
        self.update_operationlist()
        self.Operator_list.setCurrentRow(ope_idx)
        self.refresh_field()
        self.update_targetlist()
        self.show_cardinfo(self.showing_card_id)
        self.show_opeinfo()
        self.search_card()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = Ui_MainWindow()

    m_window.show()
    sys.exit(app.exec_())