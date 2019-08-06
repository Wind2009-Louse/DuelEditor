from PyQt5 import QtCore, QtGui, QtWidgets
import json
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from functools import partial
import copy
import os
import sqlite3

class Ui_MainWindow(QtWidgets.QWidget):
    def labelset(self):
        self.label_ope = QtWidgets.QLabel(self.centralwidget)
        self.label_ope.setGeometry(QtCore.QRect(1190, 0, 41, 16))
        self.label_ope.setObjectName("label_ope")
        self.label_target = QtWidgets.QLabel(self.centralwidget)
        self.label_target.setGeometry(QtCore.QRect(870, 0, 81, 20))
        self.label_target.setObjectName("label_target")
        self.label_self_hands = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands.setGeometry(QtCore.QRect(50, 470, 81, 20))
        self.label_self_hands.setObjectName("label_self_hands")
        self.label_self_hands_2 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_2.setGeometry(QtCore.QRect(260, 470, 81, 20))
        self.label_self_hands_2.setObjectName("label_self_hands_2")
        self.label_self_hands_3 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_3.setGeometry(QtCore.QRect(710, 390, 81, 20))
        self.label_self_hands_3.setObjectName("label_self_hands_3")
        self.label_self_hands_9 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_9.setGeometry(QtCore.QRect(30, 390, 81, 20))
        self.label_self_hands_9.setObjectName("label_self_hands_9")
        self.label_self_hands_10 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_10.setGeometry(QtCore.QRect(30, 310, 81, 20))
        self.label_self_hands_10.setObjectName("label_self_hands_10")
        self.label_self_hands_11 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_11.setGeometry(QtCore.QRect(710, 330, 81, 20))
        self.label_self_hands_11.setObjectName("label_self_hands_11")
        self.label_self_hands_14 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_14.setGeometry(QtCore.QRect(480, 470, 81, 20))
        self.label_self_hands_14.setObjectName("label_self_hands_14")
        self.label_self_hands_15 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_15.setGeometry(QtCore.QRect(690, 470, 81, 20))
        self.label_self_hands_15.setObjectName("label_self_hands_15")
        self.label_self_hands_16 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_16.setGeometry(QtCore.QRect(30, 160, 81, 20))
        self.label_self_hands_16.setObjectName("label_self_hands_16")
        self.label_self_hands_18 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_18.setGeometry(QtCore.QRect(710, 240, 81, 20))
        self.label_self_hands_18.setObjectName("label_self_hands_18")
        self.label_self_hands_17 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_17.setGeometry(QtCore.QRect(480, 10, 81, 20))
        self.label_self_hands_17.setObjectName("label_self_hands_17")
        self.label_self_hands_4 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_4.setGeometry(QtCore.QRect(260, 10, 81, 20))
        self.label_self_hands_4.setObjectName("label_self_hands_4")
        self.label_self_hands_12 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_12.setGeometry(QtCore.QRect(50, 10, 81, 20))
        self.label_self_hands_12.setObjectName("label_self_hands_12")
        self.label_self_hands_20 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_20.setGeometry(QtCore.QRect(690, 10, 81, 20))
        self.label_self_hands_20.setObjectName("label_self_hands_20")
        self.label_self_hands_19 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_19.setGeometry(QtCore.QRect(710, 160, 81, 20))
        self.label_self_hands_19.setObjectName("label_self_hands_19")
        self.label_self_hands_21 = QtWidgets.QLabel(self.DuelFrame)
        self.label_self_hands_21.setGeometry(QtCore.QRect(30, 240, 81, 20))
        self.label_self_hands_21.setObjectName("label_self_hands_21")
        self.label_target_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_target_2.setGeometry(QtCore.QRect(1010, 0, 81, 20))
        self.label_target_2.setObjectName("label_target_2")

    def init_frame(self):
        self.setObjectName("MainWindow")
        self.resize(1306, 639)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.DuelFrame = QtWidgets.QWidget(self.centralwidget)
        self.DuelFrame.setGeometry(QtCore.QRect(10, 0, 811, 631))
        self.DuelFrame.setObjectName("DuelFrame")
        self.labelset()

        self.Operator_list = QtWidgets.QListWidget(self.centralwidget)
        self.Operator_list.setGeometry(QtCore.QRect(1130, 20, 141, 341))
        self.Operator_list.setObjectName("Operator_list")
        self.Operator_detail = QtWidgets.QTextBrowser(self.centralwidget)
        self.Operator_detail.setGeometry(QtCore.QRect(1130, 380, 141, 151))
        self.Operator_detail.setObjectName("Operator_detail")
        self.Operator_detail.setWordWrapMode(True)
        self.Target_list = QtWidgets.QListWidget(self.centralwidget)
        self.Target_list.setGeometry(QtCore.QRect(830, 20, 141, 341))
        self.Target_list.setObjectName("Target_list")
        self.Delete_target = QtWidgets.QPushButton(self.centralwidget)
        self.Delete_target.setGeometry(QtCore.QRect(830, 370, 141, 28))
        self.Delete_target.setObjectName("Delete_target")
        self.Target_detail = QtWidgets.QTextBrowser(self.centralwidget)
        self.Target_detail.setGeometry(QtCore.QRect(830, 420, 141, 141))
        self.Target_detail.setObjectName("Target_detail")
        self.CreateCard_Button = QtWidgets.QPushButton(self.centralwidget)
        self.CreateCard_Button.setGeometry(QtCore.QRect(980, 190, 131, 28))
        self.CreateCard_Button.setObjectName("CreateCard_Button")
        self.MoveCard_Button = QtWidgets.QPushButton(self.centralwidget)
        self.MoveCard_Button.setGeometry(QtCore.QRect(980, 300, 131, 28))
        self.MoveCard_Button.setObjectName("MoveCard_Button")
        self.CommentCard_Button = QtWidgets.QPushButton(self.centralwidget)
        self.CommentCard_Button.setGeometry(QtCore.QRect(980, 380, 131, 28))
        self.CommentCard_Button.setObjectName("CommentCard_Button")
        self.Comment_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Comment_Button.setGeometry(QtCore.QRect(980, 410, 131, 28))
        self.Comment_Button.setObjectName("Comment_Button")
        self.Self_Ex = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_Ex.setGeometry(QtCore.QRect(10, 500, 141, 121))
        self.Self_Ex.setObjectName("Self_Ex")
        self.Self_Hand = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_Hand.setGeometry(QtCore.QRect(220, 500, 141, 121))
        self.Self_Hand.setObjectName("Self_Hand")
        self.Self_S1 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_S1.setGeometry(QtCore.QRect(130, 410, 111, 51))
        self.Self_S1.setObjectName("Self_S1")
        self.Self_S2 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_S2.setGeometry(QtCore.QRect(240, 410, 111, 51))
        self.Self_S2.setObjectName("Self_S2")
        self.Self_S3 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_S3.setGeometry(QtCore.QRect(350, 410, 111, 51))
        self.Self_S3.setObjectName("Self_S3")
        self.Self_S4 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_S4.setGeometry(QtCore.QRect(460, 410, 111, 51))
        self.Self_S4.setObjectName("Self_S4")
        self.Self_S5 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_S5.setGeometry(QtCore.QRect(570, 410, 111, 51))
        self.Self_S5.setObjectName("Self_S5")
        self.Self_P2 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_P2.setGeometry(QtCore.QRect(690, 420, 111, 41))
        self.Self_P2.setObjectName("Self_P2")
        self.Self_P1 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_P1.setGeometry(QtCore.QRect(10, 420, 111, 41))
        self.Self_P1.setObjectName("Self_P1")
        self.Self_Field = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_Field.setGeometry(QtCore.QRect(10, 340, 111, 41))
        self.Self_Field.setObjectName("Self_Field")
        self.Self_LP = QtWidgets.QLineEdit(self.DuelFrame)
        self.Self_LP.setText("8000")
        self.Self_LP.setEnabled(False)
        self.Self_LP.setGeometry(QtCore.QRect(690, 360, 111, 21))
        self.Self_LP.setObjectName("Self_LP")
        self.Self_M5 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_M5.setGeometry(QtCore.QRect(570, 360, 111, 51))
        self.Self_M5.setObjectName("Self_M5")
        self.Self_M1 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_M1.setGeometry(QtCore.QRect(130, 360, 111, 51))
        self.Self_M1.setObjectName("Self_M1")
        self.Self_M2 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_M2.setGeometry(QtCore.QRect(240, 360, 111, 51))
        self.Self_M2.setObjectName("Self_M2")
        self.Self_M4 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_M4.setGeometry(QtCore.QRect(460, 360, 111, 51))
        self.Self_M4.setObjectName("Self_M4")
        self.Self_M3 = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_M3.setGeometry(QtCore.QRect(350, 360, 111, 51))
        self.Self_M3.setObjectName("Self_M3")
        self.Self_Grave = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_Grave.setGeometry(QtCore.QRect(440, 500, 141, 121))
        self.Self_Grave.setObjectName("Self_Grave")
        self.Self_Banish = QtWidgets.QListWidget(self.DuelFrame)
        self.Self_Banish.setGeometry(QtCore.QRect(650, 500, 141, 121))
        self.Self_Banish.setObjectName("Self_Banish")
        self.Enemy_P1 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_P1.setGeometry(QtCore.QRect(690, 190, 111, 41))
        self.Enemy_P1.setObjectName("Enemy_P1")
        self.Enemy_M4 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_M4.setGeometry(QtCore.QRect(240, 240, 111, 51))
        self.Enemy_M4.setObjectName("Enemy_M4")
        self.Enemy_S3 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_S3.setGeometry(QtCore.QRect(350, 190, 111, 51))
        self.Enemy_S3.setObjectName("Enemy_S3")
        self.ExM_2 = QtWidgets.QListWidget(self.DuelFrame)
        self.ExM_2.setGeometry(QtCore.QRect(460, 300, 111, 51))
        self.ExM_2.setObjectName("ExM_2")
        self.Enemy_LP = QtWidgets.QLineEdit(self.DuelFrame)
        self.Enemy_LP.setGeometry(QtCore.QRect(10, 270, 111, 21))
        self.Enemy_LP.setObjectName("Enemy_LP")
        self.Enemy_LP.setText("8000")
        self.Enemy_LP.setEnabled(False)
        self.Enemy_Field = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_Field.setGeometry(QtCore.QRect(690, 270, 111, 41))
        self.Enemy_Field.setObjectName("Enemy_Field")
        self.Enemy_P2 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_P2.setGeometry(QtCore.QRect(10, 190, 111, 41))
        self.Enemy_P2.setObjectName("Enemy_P2")
        self.Enemy_S2 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_S2.setGeometry(QtCore.QRect(460, 190, 111, 51))
        self.Enemy_S2.setObjectName("Enemy_S2")
        self.ExM_1 = QtWidgets.QListWidget(self.DuelFrame)
        self.ExM_1.setGeometry(QtCore.QRect(240, 300, 111, 51))
        self.ExM_1.setObjectName("ExM_1")
        self.Enemy_M2 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_M2.setGeometry(QtCore.QRect(460, 240, 111, 51))
        self.Enemy_M2.setObjectName("Enemy_M2")
        self.Enemy_M1 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_M1.setGeometry(QtCore.QRect(570, 240, 111, 51))
        self.Enemy_M1.setObjectName("Enemy_M1")

        self.Enemy_S4 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_S4.setGeometry(QtCore.QRect(240, 190, 111, 51))
        self.Enemy_S4.setObjectName("Enemy_S4")
        self.Enemy_S1 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_S1.setGeometry(QtCore.QRect(570, 190, 111, 51))
        self.Enemy_S1.setObjectName("Enemy_S1")
        self.Enemy_S5 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_S5.setGeometry(QtCore.QRect(130, 190, 111, 51))
        self.Enemy_S5.setObjectName("Enemy_S5")
        self.Enemy_M5 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_M5.setGeometry(QtCore.QRect(130, 240, 111, 51))
        self.Enemy_M5.setObjectName("Enemy_M5")
        self.Enemy_M3 = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_M3.setGeometry(QtCore.QRect(350, 240, 111, 51))
        self.Enemy_M3.setObjectName("Enemy_M3")
        self.Enemy_Banish = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_Banish.setGeometry(QtCore.QRect(650, 40, 141, 121))
        self.Enemy_Banish.setObjectName("Enemy_Banish")
        self.Enemy_Ex = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_Ex.setGeometry(QtCore.QRect(10, 40, 141, 121))
        self.Enemy_Ex.setObjectName("Enemy_Ex")
        self.Enemy_Hand = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_Hand.setGeometry(QtCore.QRect(220, 40, 141, 121))
        self.Enemy_Hand.setObjectName("Enemy_Hand")
        self.Enemy_Grave = QtWidgets.QListWidget(self.DuelFrame)
        self.Enemy_Grave.setGeometry(QtCore.QRect(440, 40, 141, 121))
        self.Enemy_Grave.setObjectName("Enemy_Grave")
        self.Open_Buttom = QtWidgets.QPushButton(self.DuelFrame)
        self.Open_Buttom.setGeometry(QtCore.QRect(140, 310, 91, 28))
        self.Open_Buttom.setObjectName("Open_Buttom")
        self.Save_Buttom = QtWidgets.QPushButton(self.DuelFrame)
        self.Save_Buttom.setGeometry(QtCore.QRect(580, 310, 91, 28))
        self.Save_Buttom.setObjectName("Save_Buttom")
        self.EraseCard_Button = QtWidgets.QPushButton(self.centralwidget)
        self.EraseCard_Button.setGeometry(QtCore.QRect(980, 220, 131, 28))
        self.EraseCard_Button.setObjectName("EraseCard_Button")
        self.Dest_Box = QtWidgets.QComboBox(self.centralwidget)
        self.Dest_Box.setGeometry(QtCore.QRect(980, 270, 131, 22))
        self.Dest_Box.setObjectName("Dest_Box")
        for i in range(36):
            self.Dest_Box.addItem("")
        self.NewCard_line = QtWidgets.QLineEdit(self.centralwidget)
        self.NewCard_line.setGeometry(QtCore.QRect(980, 20, 131, 21))
        self.NewCard_line.setObjectName("NewCard_line")
        self.Newcard_List = QtWidgets.QListWidget(self.centralwidget)
        self.Newcard_List.setGeometry(QtCore.QRect(980, 50, 131, 131))
        self.Newcard_List.setObjectName("Newcard_List")
        self.DeleteOpe_Button = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteOpe_Button.setGeometry(QtCore.QRect(1130, 540, 141, 28))
        self.DeleteOpe_Button.setObjectName("DeleteOpe_Button")
        self.CopyOpe_Button = QtWidgets.QPushButton(self.centralwidget)
        self.CopyOpe_Button.setGeometry(QtCore.QRect(1130, 570, 141, 28))
        self.CopyOpe_Button.setObjectName("CopyOpe_Button")
        self.MoveOpe_Button = QtWidgets.QPushButton(self.centralwidget)
        self.MoveOpe_Button.setGeometry(QtCore.QRect(1130, 600, 141, 28))
        self.MoveOpe_Button.setObjectName("MoveOpe_Button")
        self.LPTarget_Box = QtWidgets.QComboBox(self.centralwidget)
        self.LPTarget_Box.setGeometry(QtCore.QRect(990, 450, 131, 22))
        self.LPTarget_Box.setObjectName("LPTarget_Box")
        self.LPTarget_Box.addItem("")
        self.LPTarget_Box.addItem("")
        self.LP_line = QtWidgets.QLineEdit(self.centralwidget)
        self.LP_line.setGeometry(QtCore.QRect(990, 480, 131, 21))
        self.LP_line.setObjectName("LP_line")
        self.AddLP_Button = QtWidgets.QPushButton(self.centralwidget)
        self.AddLP_Button.setGeometry(QtCore.QRect(990, 510, 131, 28))
        self.AddLP_Button.setObjectName("AddLP_Button")
        self.DecLP_Button = QtWidgets.QPushButton(self.centralwidget)
        self.DecLP_Button.setGeometry(QtCore.QRect(990, 540, 131, 28))
        self.DecLP_Button.setObjectName("DecLP_Button")
        self.CgeLP_Button = QtWidgets.QPushButton(self.centralwidget)
        self.CgeLP_Button.setGeometry(QtCore.QRect(990, 570, 131, 28))
        self.CgeLP_Button.setObjectName("CgeLP_Button")
        self.HalLP_Button = QtWidgets.QPushButton(self.centralwidget)
        self.HalLP_Button.setGeometry(QtCore.QRect(990, 600, 131, 28))
        self.HalLP_Button.setObjectName("HalLP_Button")
        self.NewCard_Rename = QtWidgets.QLineEdit(self.centralwidget)
        self.NewCard_Rename.setGeometry(QtCore.QRect(830, 570, 141, 21))
        self.NewCard_Rename.setObjectName("NewCard_Rename")
        self.NewCard_Rename_Button = QtWidgets.QPushButton(self.centralwidget)
        self.NewCard_Rename_Button.setGeometry(QtCore.QRect(830, 600, 141, 28))
        self.NewCard_Rename_Button.setObjectName("NewCard_Rename_Button")
        self.Comment_Line = QtWidgets.QLineEdit(self.centralwidget)
        self.Comment_Line.setGeometry(QtCore.QRect(980, 350, 131, 21))
        self.Comment_Line.setObjectName("Comment_Line")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __init__(self):
        self.idx_represent_str = ["己方手卡", "己方魔陷_1", "己方魔陷_2", "己方魔陷_3", "己方魔陷_4", "己方魔陷_5", "己方场地", "己方灵摆_1", "己方灵摆_2", "己方怪兽_1", "己方怪兽_2", "己方怪兽_3", "己方怪兽_4", "己方怪兽_5", "己方墓地", "己方除外", "己方额外", "对方手卡", "对方魔陷_1", "对方魔陷_2", "对方魔陷_3", "对方魔陷_4", "对方魔陷_5", "对方场地", "对方灵摆_1", "对方灵摆_2", "对方怪兽_1", "对方怪兽_2", "对方怪兽_3", "对方怪兽_4", "对方怪兽_5", "对方墓地", "对方除外", "对方额外", "额外怪兽区_1", "额外怪兽区_2"]
        super(Ui_MainWindow, self).__init__()
        self.init_frame()

        self.card_names = []
        try:
            if not os.path.exists("cards.cdb"):
                a+=1
            sql_conn = sqlite3.connect('cards.cdb')
            cur = sql_conn.cursor()
            sel = cur.execute("select * from texts;")
            for row in sel:
                self.card_names.append(row[1])
            sql_conn.close()
        except Exception as e:
            self.Newcard_List.addItem("无数据库")
            self.Newcard_List.setEnabled(False)

        self.idx_represent_field = [self.Self_Hand, self.Self_S1, self.Self_S2, self.Self_S3, self.Self_S4, self.Self_S5, self.Self_Field, self.Self_P1, self.Self_P2, self.Self_M1, self.Self_M2, self.Self_M3, self.Self_M4, self.Self_M5, self.Self_Grave, self.Self_Banish, self.Self_Ex, self.Enemy_Hand, self.Enemy_S1, self.Enemy_S2, self.Enemy_S3, self.Enemy_S4, self.Enemy_S5, self.Enemy_Field, self.Enemy_P1, self.Enemy_P2, self.Enemy_M1, self.Enemy_M2, self.Enemy_M3, self.Enemy_M4, self.Enemy_M5, self.Enemy_Grave, self.Enemy_Banish, self.Enemy_Ex, self.ExM_1, self.ExM_2]
        self.operators = {"cardindex":0, "cards":{}, "operations":[]}
        self.fields = {0:{"locations":{}, "desp":{}, "LP":[0,0]}}
        self.targets = []

        self.Open_Buttom.clicked.connect(self.openfile)
        self.Save_Buttom.clicked.connect(self.savefile)

        self.Delete_target.clicked.connect(self.remove_from_targets)
        self.Target_list.clicked.connect(self.click_target_list)

        self.Operator_list.clicked.connect(self.click_operation_list)

        self.CreateCard_Button.clicked.connect(self.create_card)

        self.AddLP_Button.clicked.connect(self.ope_LPAdd)
        self.DecLP_Button.clicked.connect(self.ope_LPDec)
        self.CgeLP_Button.clicked.connect(self.ope_LPCge)
        self.HalLP_Button.clicked.connect(self.ope_LPHal)

        self.Comment_Button.clicked.connect(self.ope_addcomment)
        self.CommentCard_Button.clicked.connect(self.ope_addcarddesp)

        self.NewCard_line.textChanged.connect(self.search_card)
        self.Newcard_List.doubleClicked.connect(self.fix_cardname)

        self.DeleteOpe_Button.clicked.connect(self.remove_operator)

        for field_id in range(len(self.idx_represent_field)):
            self.idx_represent_field[field_id].clicked.connect(partial(self.select_field, field_id))
            self.idx_represent_field[field_id].doubleClicked.connect(partial(self.target_field, field_id))

        self.MoveCard_Button.clicked.connect(self.ope_movecards)

        self.NewCard_Rename_Button.clicked.connect(self.card_rename)

        # TODO
        self.CopyOpe_Button.setEnabled(False)
        self.MoveOpe_Button.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DuelEditor"))
        __sortingEnabled = self.Operator_list.isSortingEnabled()
        self.Operator_list.setSortingEnabled(False)

        self.Operator_list.setSortingEnabled(__sortingEnabled)
        self.label_ope.setText(_translate("MainWindow", "操作"))
        self.label_target.setText(_translate("MainWindow", "操作对象"))
        self.Delete_target.setText(_translate("MainWindow", "列表中删除"))
        self.CreateCard_Button.setText(_translate("MainWindow", "←创建卡片"))
        self.MoveCard_Button.setText(_translate("MainWindow", "移动卡片"))
        self.CommentCard_Button.setText(_translate("MainWindow", "卡片注释"))
        self.Comment_Button.setText(_translate("MainWindow", "操作注释"))
        self.label_self_hands.setText(_translate("MainWindow", "己方额外"))
        self.label_self_hands_2.setText(_translate("MainWindow", "己方手卡"))
        self.label_self_hands_3.setText(_translate("MainWindow", "己方右灵摆"))
        self.label_self_hands_9.setText(_translate("MainWindow", "己方左灵摆"))
        self.label_self_hands_10.setText(_translate("MainWindow", "己方场地"))
        self.label_self_hands_11.setText(_translate("MainWindow", "己方基本分"))
        self.label_self_hands_14.setText(_translate("MainWindow", "己方墓地"))
        self.label_self_hands_15.setText(_translate("MainWindow", "己方除外"))
        self.label_self_hands_16.setText(_translate("MainWindow", "对方右灵摆"))
        self.label_self_hands_18.setText(_translate("MainWindow", "对方场地"))
        self.label_self_hands_19.setText(_translate("MainWindow", "对方左灵摆"))
        self.label_self_hands_21.setText(_translate("MainWindow", "对方基本分"))
        self.label_self_hands_17.setText(_translate("MainWindow", "对方墓地"))
        self.label_self_hands_4.setText(_translate("MainWindow", "对方手卡"))
        self.label_self_hands_12.setText(_translate("MainWindow", "对方额外"))
        self.label_self_hands_20.setText(_translate("MainWindow", "对方除外"))
        self.Open_Buttom.setText(_translate("MainWindow", "打开"))
        self.Save_Buttom.setText(_translate("MainWindow", "保存"))
        self.EraseCard_Button.setText(_translate("MainWindow", "删除卡片"))
        for idx in range(len(self.idx_represent_str)):
            self.Dest_Box.setItemText(idx, _translate("MainWindow", self.idx_represent_str[idx]))
        self.label_target_2.setText(_translate("MainWindow", "新建列表"))
        self.DeleteOpe_Button.setText(_translate("MainWindow", "删除操作"))
        self.CopyOpe_Button.setText(_translate("MainWindow", "复制操作"))
        self.MoveOpe_Button.setText(_translate("MainWindow", "移动操作"))
        self.LPTarget_Box.setItemText(0, _translate("MainWindow", "己方"))
        self.LPTarget_Box.setItemText(1, _translate("MainWindow", "对方"))
        self.AddLP_Button.setText(_translate("MainWindow", "增加基本分"))
        self.DecLP_Button.setText(_translate("MainWindow", "减少基本分"))
        self.CgeLP_Button.setText(_translate("MainWindow", "变成基本分"))
        self.HalLP_Button.setText(_translate("MainWindow", "基本分减半"))
        self.NewCard_Rename_Button.setText(_translate("MainWindow", "重命名"))

    def openfile(self):
        fullname = str(QFileDialog.getOpenFileName(self, '选择打开的文件',filter="*.json")[0])
        if len(fullname) == 0:
            return
        with open(fullname,'r') as f:
            json_data = f.read()
            dict_data = json.loads(json_data)
            self.operators = dict_data
            self.update_operationlist()
            self.make_fields()
            self.Operator_list.setCurrentRow(len(self.operators["operations"])-1)
            self.refresh_field()
    
    def savefile(self):
        fullname = str(QFileDialog.getSaveFileName(self,'保存为', "Untitle.json","*.json")[0])
        if len(fullname) == 0:
            return
        json_data = json.dumps(self.operators,indent=2,)
        with open(fullname,'w') as f:
            f.write(json_data)

    def make_fields(self):
        '''根据操作生成各操作的场地'''
        self.fields.clear()
        lastest_field = {"locations":{}, "desp":{}, "LP":[8000,8000]}
        for idx in range(len(self.operators["operations"])):
            '''type(str), args(list of int), dest(int), desp(str)'''
            operation = self.operators["operations"][idx]
            if operation["type"] == "move":
                for card_idx in operation["args"]:
                    lastest_field["locations"][card_idx] = operation["dest"]
            elif operation["type"] == "carddesp":
                for card_idx in operation["args"]:
                    lastest_field["desp"][card_idx] = operation["desp"]
            elif operation["type"] == "LPAdd":
                lastest_field["LP"][operation["args"][0]] += operation["args"][1]
            elif operation["type"] == "LPDec":
                lastest_field["LP"][operation["args"][0]] -= operation["args"][1]
            elif operation["type"] == "LPCge":
                lastest_field["LP"][operation["args"][0]] = operation["args"][1]
            elif operation["type"] == "LPHal":
                lastest_field["LP"][operation["args"][0]] = (lastest_field["LP"][operation["args"][0]] + 1) // 2
            self.fields[idx] = copy.deepcopy(lastest_field)

    def get_last_location(self, card_id, ope_id):
        '''获取卡片的上一个位置'''
        if ope_id == 0:
            return "未知"
        field = self.fields[ope_id-1]
        if card_id in field["locations"]:
            return self.idx_represent_str[field["locations"][card_id]]
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
        self.make_fields()
        self.update_operationlist()
        self.Operator_list.setCurrentRow(ope_id)
        self.refresh_field()
        self.show_opeinfo()

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
            card_locat = self.idx_represent_str[field["locations"][card_id]]
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
                first_card = False
                card_name += self.operators["cards"][card_idx]["Name"]
            result = "%s 移到%s"%(card_name, self.idx_represent_str[operation["dest"]])
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
        idx = idx[0].row()
        del self.operators["operations"][idx]
        self.make_fields()
        self.update_operationlist()
        self.Operator_list.setCurrentRow(idx-1)
        self.refresh_field()
        self.show_opeinfo()

    def click_target_list(self, qindex):
        idx = qindex.row()
        if idx < 0:
            return
        for lst in self.idx_represent_field:
            lst.clearSelection()
        card_id = self.targets[idx]
        self.show_cardinfo(card_id)

    def click_operation_list(self, qindex):
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
                result = "%s 移到%s"%(card_name, self.idx_represent_str[operation["dest"]])
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

    def refresh_field(self):
        '''刷新场地'''
        for cardlist in self.idx_represent_field:
            cardlist.clear()
        field = self.get_current_field()
        self.Self_LP.setText("%d"%field["LP"][0])
        self.Enemy_LP.setText("%d"%field["LP"][1])
        for card_id in field['locations'].keys():
            list_id = field["locations"][card_id]
            show_list = self.idx_represent_field[list_id]
            card_name = self.operators["cards"][card_id]["Name"]
            show_list.addItem(card_name)
    
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
        self.update_operationlist()
    
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
        self.update_operationlist()
    
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
        self.update_operationlist()

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

    def select_field(self, field_id):
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
                    self.targets.append(card_id)
                    self.update_targetlist()
                selected -= 1

    def search_card(self):
        if not self.Newcard_List.isEnabled():
            return
        text = self.NewCard_line.text()
        if len(text) == 0:
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
        self.make_fields()
        self.update_operationlist()
        self.update_targetlist()
        self.Operator_list.setCurrentRow(ope_idx)
        self.refresh_field()
        self.show_cardinfo(self.showing_card_id)
        self.show_opeinfo()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = Ui_MainWindow()

    m_window.show()
    sys.exit(app.exec_())