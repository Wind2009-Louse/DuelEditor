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

class Ui_MainWindow(QWidget):
    def labelset(self):
        '''初始化label'''
        self.label_target_list = QLabel(self.centralwidget)
        self.label_target_list.setGeometry(QRect(830, 0, 181, 20))
        self.label_target_list.setAlignment(Qt.AlignCenter)
        self.label_cardsearch = QLabel(self.centralwidget)
        self.label_cardsearch.setGeometry(QRect(1020, 0, 181, 20))
        self.label_cardsearch.setAlignment(Qt.AlignCenter)
        self.label_operation_list = QLabel(self.centralwidget)
        self.label_operation_list.setGeometry(QRect(1210, 0, 181, 16))
        self.label_operation_list.setAlignment(Qt.AlignCenter)

        self.label_self_ex = QLabel(self.DuelFrame)
        self.label_self_ex.setGeometry(QRect(10, 470, 141, 20))
        self.label_self_ex.setAlignment(Qt.AlignCenter)
        self.label_self_hand = QLabel(self.DuelFrame)
        self.label_self_hand.setGeometry(QRect(220, 470, 141, 20))
        self.label_self_hand.setAlignment(Qt.AlignCenter)
        self.label_self_rpen = QLabel(self.DuelFrame)
        self.label_self_rpen.setGeometry(QRect(710, 390, 81, 20))
        self.label_self_lpen = QLabel(self.DuelFrame)
        self.label_self_lpen.setGeometry(QRect(30, 390, 81, 20))
        self.label_self_field = QLabel(self.DuelFrame)
        self.label_self_field.setGeometry(QRect(30, 310, 81, 20))
        self.label_self_lp = QLabel(self.DuelFrame)
        self.label_self_lp.setGeometry(QRect(710, 330, 81, 20))
        self.label_self_grave = QLabel(self.DuelFrame)
        self.label_self_grave.setGeometry(QRect(440, 470, 141, 20))
        self.label_self_grave.setAlignment(Qt.AlignCenter)
        self.label_self_banish = QLabel(self.DuelFrame)
        self.label_self_banish.setGeometry(QRect(650, 470, 141, 20))
        self.label_self_banish.setAlignment(Qt.AlignCenter)
        self.label_enemy_rpen = QLabel(self.DuelFrame)
        self.label_enemy_rpen.setGeometry(QRect(30, 160, 81, 20))
        self.label_enemy_field = QLabel(self.DuelFrame)
        self.label_enemy_field.setGeometry(QRect(710, 240, 81, 20))
        self.label_enemy_grave = QLabel(self.DuelFrame)
        self.label_enemy_grave.setGeometry(QRect(440, 10, 141, 20))
        self.label_enemy_grave.setAlignment(Qt.AlignCenter)
        self.label_enemy_hand = QLabel(self.DuelFrame)
        self.label_enemy_hand.setGeometry(QRect(220, 10, 141, 20))
        self.label_enemy_hand.setAlignment(Qt.AlignCenter)
        self.label_enemy_ex = QLabel(self.DuelFrame)
        self.label_enemy_ex.setGeometry(QRect(10, 10, 141, 20))
        self.label_enemy_ex.setAlignment(Qt.AlignCenter)
        self.label_enemy_banish = QLabel(self.DuelFrame)
        self.label_enemy_banish.setGeometry(QRect(650, 10, 141, 20))
        self.label_enemy_banish.setAlignment(Qt.AlignCenter)
        self.label_enemy_lpen = QLabel(self.DuelFrame)
        self.label_enemy_lpen.setGeometry(QRect(710, 160, 81, 20))
        self.label_enemy_lp = QLabel(self.DuelFrame)
        self.label_enemy_lp.setGeometry(QRect(30, 240, 81, 20))

    def init_frame(self):
        '''初始化UI'''
        self.setObjectName("MainWindow")
        self.resize(1396, 639)
        self.setFixedSize(1396, 639)
        self.centralwidget = QWidget(self)

        self.DuelFrame = QWidget(self.centralwidget)
        self.DuelFrame.setGeometry(QRect(10, 0, 811, 631))
        self.labelset()

        self.Target_list = QListWidget(self.centralwidget)
        self.Target_list.setGeometry(QRect(830, 20, 181, 251))
        self.Delete_target = QPushButton(self.centralwidget)
        self.Delete_target.setGeometry(QRect(830, 280, 181, 28))
        self.Dest_Box = QComboBox(self.centralwidget)
        self.Dest_Box.setGeometry(QRect(830, 320, 181, 22))
        for i in range(36):
            self.Dest_Box.addItem("")
        self.MoveCard_Button = QPushButton(self.centralwidget)
        self.MoveCard_Button.setGeometry(QRect(830, 350, 181, 28))
        self.EraseCard_Button = QPushButton(self.centralwidget)
        self.EraseCard_Button.setGeometry(QRect(830, 380, 181, 28))
        self.Target_detail = QTextBrowser(self.centralwidget)
        self.Target_detail.setGeometry(QRect(830, 420, 181, 208))

        self.NewCard_line = QLineEdit(self.centralwidget)
        self.NewCard_line.setGeometry(QRect(1020, 20, 181, 21))
        self.Newcard_List = QListWidget(self.centralwidget)
        self.Newcard_List.setGeometry(QRect(1020, 50, 181, 221))
        self.CreateCard_Button = QPushButton(self.centralwidget)
        self.CreateCard_Button.setGeometry(QRect(1020, 280, 181, 28))
        self.NewCard_Rename_Button = QPushButton(self.centralwidget)
        self.NewCard_Rename_Button.setGeometry(QRect(1020, 320, 181, 28))
        self.Comment_Line = QLineEdit(self.centralwidget)
        self.Comment_Line.setGeometry(QRect(1020, 353, 181, 21))
        self.CommentCard_Button = QPushButton(self.centralwidget)
        self.CommentCard_Button.setGeometry(QRect(1020, 380, 181, 28))
        self.Comment_Button = QPushButton(self.centralwidget)
        self.Comment_Button.setGeometry(QRect(1020, 410, 181, 28))
        self.LPTarget_Box = QComboBox(self.centralwidget)
        self.LPTarget_Box.setGeometry(QRect(1020, 450, 181, 22))
        self.LPTarget_Box.addItem("")
        self.LPTarget_Box.addItem("")
        self.LP_line = QLineEdit(self.centralwidget)
        self.LP_line.setGeometry(QRect(1020, 480, 181, 21))
        regx = QRegExp("^[0-9]{15}$")
        validator = QRegExpValidator(regx, self.LP_line)
        self.LP_line.setValidator(validator)
        self.AddLP_Button = QPushButton(self.centralwidget)
        self.AddLP_Button.setGeometry(QRect(1020, 510, 181, 28))
        self.DecLP_Button = QPushButton(self.centralwidget)
        self.DecLP_Button.setGeometry(QRect(1020, 540, 181, 28))
        self.CgeLP_Button = QPushButton(self.centralwidget)
        self.CgeLP_Button.setGeometry(QRect(1020, 570, 181, 28))
        self.HalLP_Button = QPushButton(self.centralwidget)
        self.HalLP_Button.setGeometry(QRect(1020, 600, 181, 28))

        self.Operator_list = QListWidget(self.centralwidget)
        self.Operator_list.setGeometry(QRect(1210, 20, 181, 440))
        self.DeleteOpe_Button = QPushButton(self.centralwidget)
        self.DeleteOpe_Button.setGeometry(QRect(1210, 470, 181, 28))
        self.SelectedOpe_list = QListWidget(self.centralwidget)
        self.SelectedOpe_list.setGeometry(QRect(1210, 510, 181, 51))
        self.CopyOpe_Button = QPushButton(self.centralwidget)
        self.CopyOpe_Button.setGeometry(QRect(1210, 570, 181, 28))
        self.MoveOpe_Button = QPushButton(self.centralwidget)
        self.MoveOpe_Button.setGeometry(QRect(1210, 600, 181, 28))

        self.Self_Ex = QListWidget(self.DuelFrame)
        self.Self_Ex.setGeometry(QRect(10, 500, 141, 121))
        self.Self_Hand = QListWidget(self.DuelFrame)
        self.Self_Hand.setGeometry(QRect(220, 500, 141, 121))
        self.Self_S1 = QListWidget(self.DuelFrame)
        self.Self_S1.setGeometry(QRect(130, 410, 111, 51))
        self.Self_S2 = QListWidget(self.DuelFrame)
        self.Self_S2.setGeometry(QRect(240, 410, 111, 51))
        self.Self_S3 = QListWidget(self.DuelFrame)
        self.Self_S3.setGeometry(QRect(350, 410, 111, 51))
        self.Self_S4 = QListWidget(self.DuelFrame)
        self.Self_S4.setGeometry(QRect(460, 410, 111, 51))
        self.Self_S5 = QListWidget(self.DuelFrame)
        self.Self_S5.setGeometry(QRect(570, 410, 111, 51))
        self.Self_P2 = QListWidget(self.DuelFrame)
        self.Self_P2.setGeometry(QRect(690, 420, 111, 41))
        self.Self_P1 = QListWidget(self.DuelFrame)
        self.Self_P1.setGeometry(QRect(10, 420, 111, 41))
        self.Self_Field = QListWidget(self.DuelFrame)
        self.Self_Field.setGeometry(QRect(10, 340, 111, 41))
        self.Self_LP = QLineEdit(self.DuelFrame)
        self.Self_LP.setText("8000")
        self.Self_LP.setEnabled(False)
        self.Self_LP.setGeometry(QRect(690, 360, 111, 21))
        self.Self_M5 = QListWidget(self.DuelFrame)
        self.Self_M5.setGeometry(QRect(570, 360, 111, 51))
        self.Self_M1 = QListWidget(self.DuelFrame)
        self.Self_M1.setGeometry(QRect(130, 360, 111, 51))
        self.Self_M2 = QListWidget(self.DuelFrame)
        self.Self_M2.setGeometry(QRect(240, 360, 111, 51))
        self.Self_M4 = QListWidget(self.DuelFrame)
        self.Self_M4.setGeometry(QRect(460, 360, 111, 51))
        self.Self_M3 = QListWidget(self.DuelFrame)
        self.Self_M3.setGeometry(QRect(350, 360, 111, 51))
        self.Self_Grave = QListWidget(self.DuelFrame)
        self.Self_Grave.setGeometry(QRect(440, 500, 141, 121))
        self.Self_Banish = QListWidget(self.DuelFrame)
        self.Self_Banish.setGeometry(QRect(650, 500, 141, 121))
        self.Enemy_P1 = QListWidget(self.DuelFrame)
        self.Enemy_P1.setGeometry(QRect(690, 190, 111, 41))
        self.Enemy_M4 = QListWidget(self.DuelFrame)
        self.Enemy_M4.setGeometry(QRect(240, 240, 111, 51))
        self.Enemy_S3 = QListWidget(self.DuelFrame)
        self.Enemy_S3.setGeometry(QRect(350, 190, 111, 51))

        self.ExM_2 = QListWidget(self.DuelFrame)
        self.ExM_2.setGeometry(QRect(460, 300, 111, 51))
        self.ExM_1 = QListWidget(self.DuelFrame)
        self.ExM_1.setGeometry(QRect(240, 300, 111, 51))

        self.Enemy_LP = QLineEdit(self.DuelFrame)
        self.Enemy_LP.setGeometry(QRect(10, 270, 111, 21))
        self.Enemy_LP.setText("8000")
        self.Enemy_LP.setEnabled(False)
        self.Enemy_Field = QListWidget(self.DuelFrame)
        self.Enemy_Field.setGeometry(QRect(690, 270, 111, 41))
        self.Enemy_P2 = QListWidget(self.DuelFrame)
        self.Enemy_P2.setGeometry(QRect(10, 190, 111, 41))
        self.Enemy_S2 = QListWidget(self.DuelFrame)
        self.Enemy_S2.setGeometry(QRect(460, 190, 111, 51))
        self.Enemy_M2 = QListWidget(self.DuelFrame)
        self.Enemy_M2.setGeometry(QRect(460, 240, 111, 51))
        self.Enemy_M1 = QListWidget(self.DuelFrame)
        self.Enemy_M1.setGeometry(QRect(570, 240, 111, 51))
        self.Enemy_S4 = QListWidget(self.DuelFrame)
        self.Enemy_S4.setGeometry(QRect(240, 190, 111, 51))
        self.Enemy_S1 = QListWidget(self.DuelFrame)
        self.Enemy_S1.setGeometry(QRect(570, 190, 111, 51))
        self.Enemy_S5 = QListWidget(self.DuelFrame)
        self.Enemy_S5.setGeometry(QRect(130, 190, 111, 51))
        self.Enemy_M5 = QListWidget(self.DuelFrame)
        self.Enemy_M5.setGeometry(QRect(130, 240, 111, 51))
        self.Enemy_M3 = QListWidget(self.DuelFrame)
        self.Enemy_M3.setGeometry(QRect(350, 240, 111, 51))
        self.Enemy_Banish = QListWidget(self.DuelFrame)
        self.Enemy_Banish.setGeometry(QRect(650, 40, 141, 121))
        self.Enemy_Ex = QListWidget(self.DuelFrame)
        self.Enemy_Ex.setGeometry(QRect(10, 40, 141, 121))
        self.Enemy_Hand = QListWidget(self.DuelFrame)
        self.Enemy_Hand.setGeometry(QRect(220, 40, 141, 121))
        self.Enemy_Grave = QListWidget(self.DuelFrame)
        self.Enemy_Grave.setGeometry(QRect(440, 40, 141, 121))
        self.Open_Buttom = QPushButton(self.DuelFrame)
        self.Open_Buttom.setGeometry(QRect(140, 310, 91, 28))
        self.Save_Buttom = QPushButton(self.DuelFrame)
        self.Save_Buttom.setGeometry(QRect(580, 310, 91, 28))

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
        self.idx_represent_field = [
            self.Self_Hand, self.Self_S1, self.Self_S2, self.Self_S3, self.Self_S4, self.Self_S5,
            self.Self_Field, self.Self_P1, self.Self_P2, self.Self_M1, self.Self_M2, self.Self_M3, self.Self_M4, self.Self_M5,
            self.Self_Grave, self.Self_Banish, self.Self_Ex,
            self.Enemy_Hand, self.Enemy_S1, self.Enemy_S2, self.Enemy_S3, self.Enemy_S4, self.Enemy_S5,
            self.Enemy_Field, self.Enemy_P1, self.Enemy_P2, self.Enemy_M1, self.Enemy_M2, self.Enemy_M3, self.Enemy_M4, self.Enemy_M5,
            self.Enemy_Grave, self.Enemy_Banish, self.Enemy_Ex, self.ExM_1, self.ExM_2
        ]
        self.operators = {"cardindex":0, "cards":{}, "operations":[]}
        self.fields = {0:{"locations":{}, "desp":{}, "LP":[0,0]}}
        self.targets = []
        self.filename = "Untitle.json"
        self.last_text = ""
        self.unsave_changed = False

        # 打开/保存文件
        self.Open_Buttom.clicked.connect(self.openfile)
        self.Save_Buttom.clicked.connect(self.savefile)

        # 操作部分
        self.copying_operation = {}
        self.Operator_list.itemSelectionChanged.connect(self.operation_index_changed)
        self.DeleteOpe_Button.clicked.connect(self.remove_operator)
        self.Operator_list.doubleClicked.connect(self.copy_ope)
        self.CopyOpe_Button.clicked.connect(self.copy_ope)
        self.SelectedOpe_list.itemSelectionChanged.connect(self.select_copying)
        self.MoveOpe_Button.clicked.connect(self.move_operator)
        self.SelectedOpe_list.addItem("无操作")
        self.SelectedOpe_list.setEnabled(False)
        self.MoveOpe_Button.setEnabled(False)

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
        '''键盘事件响应'''
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            # Ctrl+S=保存
            if event.key() == Qt.Key_S:
                self.savefile()
            # Ctrl+O=打开
            elif event.key() == Qt.Key_O:
                self.openfile()
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

    def closeEvent(self, event):
        '''重写关闭窗口事件
        
        用于退出前确认保存更改'''
        if self.unsave_confirm():
            event.ignore()
        else:
            event.accept()

    def comment_enter(self):
        '''在注释栏回车时触发的事件
        
        根据目标数量确定为为卡片添加注释，或是添加操作备注'''
        if len(self.targets) > 0:
            self.ope_addcarddesp()
        else:
            self.ope_addcomment()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("DuelEditor")
        __sortingEnabled = self.Operator_list.isSortingEnabled()
        self.Operator_list.setSortingEnabled(False)

        self.Operator_list.setSortingEnabled(__sortingEnabled)
        self.label_operation_list.setText("操作列表")
        self.label_target_list.setText("操作对象")
        self.Delete_target.setText("对象中删除")
        self.CreateCard_Button.setText("←添加到对象")
        self.MoveCard_Button.setText("移动对象")
        self.CommentCard_Button.setText("对象注释")
        self.Comment_Button.setText("操作注释")
        self.label_self_ex.setText("己方额外")
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
        self.label_enemy_grave.setText("对方墓地")
        self.label_enemy_hand.setText("对方手卡")
        self.label_enemy_ex.setText("对方额外")
        self.label_enemy_banish.setText("对方除外")
        self.Open_Buttom.setText("打开(O)")
        self.Save_Buttom.setText("保存(S)")
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

    def maketitle(self):
        '''根据当前正在打开的文件修改窗口标题'''
        title_name = "DuelEditor - %s"%self.filename
        if self.unsave_changed:
            title_name += "*"
        self.setWindowTitle(title_name)

    def openfile(self):
        '''打开文件'''
        if self.unsave_confirm():
            return
        fullname = str(QFileDialog.getOpenFileName(self, '选择打开的文件',filter="*.json")[0])
        if len(fullname) == 0:
            return
        self.filename = os.path.split(fullname)[-1]
        self.unsave_changed = False
        self.maketitle()
        try:
            with open(fullname,'r') as f:
                json_data = f.read()
                dict_data = loads(json_data)
                self.operators = dict_data
                self.make_fields()
                self.update_operationlist()
                self.Operator_list.setCurrentRow(len(self.operators["operations"])-1)
                return
        # 出错时尝试使用utf-8编码打开文件
        except:
            with open(fullname,'r',encoding='utf-8') as f:
                json_data = f.read()
                dict_data = loads(json_data)
                self.operators = dict_data
                self.make_fields()
                self.update_operationlist()
                self.Operator_list.setCurrentRow(len(self.operators["operations"])-1)
                return
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
            lastest_field = {"locations":{}, "desp":{}, "LP":[8000,8000], "fields":[]}
            for t in range(len(idx_represent_str)):
                lastest_field["fields"].append([])
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
        '''显示指定操作详情\n\nidx为空时，显示选定操作的详情'''
        # 获取操作
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
                    card_name += "、"
                last_location = self.get_last_location(card_idx,idx)
                first_card = False
                card_name += "[%s]%s"%(last_location,self.operators["cards"][card_idx]["Name"])
            result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
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
        self.Operator_list.setCurrentRow(idx-1)
        self.show_opeinfo()

    def move_operator(self):
        '''粘贴操作'''
        if self.copying_operation == {}:
            return
        self.insert_operation(self.copying_operation)
        self.copying_operation = {}
        self.draw_copying()

    def copy_ope(self):
        '''复制操作'''
        idx = self.Operator_list.selectedIndexes()
        if len(idx) < 1:
            return
        idx = idx[0].row()
        ope = deepcopy(self.operators["operations"][idx])
        self.copying_operation = ope
        self.draw_copying()
    
    def draw_copying(self):
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
                        card_name += "、"
                    first_card = False
                    card_name += "%s"%(self.operators["cards"][card_idx]["Name"])
                result = "%s 移到%s"%(card_name, idx_represent_str[operation["dest"]])
            elif operation["type"] == "carddesp":
                card_name = ""
                first_card = True
                for card_idx in operation["args"]:
                    if not first_card:
                        card_name += "、"
                    first_card = False
                    card_name += "%s"%(self.operators["cards"][card_idx]["Name"])
                result = "%s %s"%(card_name, operation["desp"])
            elif operation["type"] == "erase":
                card_name = ""
                first_card = True
                for card_idx in operation["args"]:
                    if not first_card:
                        card_name += "、"
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

    def update_targetlist(self):
        '''更新对象列表'''
        ope_id = self.Operator_list.selectedIndexes()
        if len(ope_id) == 0:
            ope_id = 0
        else:
            ope_id = ope_id[0].row()
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
        
        # 数量标注
        self.label_enemy_ex.setText("对方额外(%d)"%self.Enemy_Ex.count())
        self.label_enemy_hand.setText("对方手卡(%d)"%self.Enemy_Hand.count())
        self.label_enemy_grave.setText("对方墓地(%d)"%self.Enemy_Grave.count())
        self.label_enemy_banish.setText("对方除外(%d)"%self.Enemy_Banish.count())
        self.label_self_ex.setText("己方额外(%d)"%self.Self_Ex.count())
        self.label_self_hand.setText("己方手卡(%d)"%self.Self_Hand.count())
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
        # 遍历搜索符合条件的卡片
        for cardname in self.card_names:
            if text in cardname:
                self.Newcard_List.addItem(cardname)
    
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
        reply = QMessageBox.warning(self, '提示', "是否要把这张卡片重命名为%s？"%text, QMessageBox.Yes | QMessageBox.No)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = Ui_MainWindow()

    m_window.show()
    sys.exit(app.exec_())