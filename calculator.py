#encoding:utf-8
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QListWidget, QTextBrowser, QLabel
from PyQt5.QtCore import QRegExp, QRect
from PyQt5.QtGui import QRegExpValidator, QColor
import sys

class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.setWindowTitle("Calculator")
        self.resize(400, 286)
        self.setFixedSize(400, 286)
        self.name_line = QLineEdit(self)
        self.name_line.setGeometry(QRect(240, 10, 151, 21))
        self.card_list = QListWidget(self)
        self.card_list.setGeometry(QRect(10, 10, 151, 261))
        self.atk_line = QTextBrowser(self)
        self.atk_line.setGeometry(QRect(240, 40, 151, 21))
        self.def_line = QTextBrowser(self)
        self.def_line.setGeometry(QRect(240, 70, 151, 21))
        self.num_a_line = QLineEdit(self)
        self.num_a_line.setGeometry(QRect(240, 100, 151, 21))
        self.num_b_line = QLineEdit(self)
        self.num_b_line.setGeometry(QRect(240, 130, 151, 21))
        self.add_line = QTextBrowser(self)
        self.add_line.setGeometry(QRect(240, 160, 151, 21))
        self.sub_line = QTextBrowser(self)
        self.sub_line.setGeometry(QRect(240, 190, 151, 21))
        self.mul_line = QTextBrowser(self)
        self.mul_line.setGeometry(QRect(240, 220, 151, 21))
        self.div_line = QTextBrowser(self)
        self.div_line.setGeometry(QRect(240, 250, 151, 21))

        self.label = QLabel(self)
        self.label.setGeometry(QRect(170, 10, 41, 16))
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(170, 40, 61, 20))
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(170, 70, 61, 20))
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(170, 100, 61, 20))
        self.label_5 = QLabel(self)
        self.label_5.setGeometry(QRect(170, 130, 61, 20))
        self.label_6 = QLabel(self)
        self.label_6.setGeometry(QRect(170, 160, 61, 20))
        self.label_7 = QLabel(self)
        self.label_7.setGeometry(QRect(170, 190, 61, 20))
        self.label_8 = QLabel(self)
        self.label_8.setGeometry(QRect(170, 220, 61, 20))
        self.label_9 = QLabel(self)
        self.label_9.setGeometry(QRect(170, 250, 61, 20))
        self.label.setText("卡名")
        self.label_2.setText("攻击力")
        self.label_3.setText("防御力")
        self.label_4.setText("a")
        self.label_5.setText("b")
        self.label_6.setText("a+b")
        self.label_7.setText("a-b")
        self.label_8.setText("a*b")
        self.label_9.setText("a/b")

        # set regex for numeric
        regx = QRegExp("^[0-9]{15}$")
        for num_line in [self.num_a_line, self.num_b_line]:
            validator = QRegExpValidator(regx, num_line)
            num_line.setValidator(validator)

        self.name_line.setPlaceholderText("输入卡名")
        self.num_a_line.setPlaceholderText("输入非负整数")
        self.num_b_line.setPlaceholderText("输入非负整数")

        # hide scroll bar
        for bar in [self.atk_line, self.def_line, self.add_line, self.sub_line, self.mul_line, self.div_line]:
            bar.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            bar.setTextColor(QColor('green'))

        # connect
        self.name_line.textChanged.connect(self.search_card)
        self.card_list.itemSelectionChanged.connect(self.show_ad)
        self.num_a_line.textChanged.connect(self.cal)
        self.num_b_line.textChanged.connect(self.cal)

    def setdatas(self, data):
        self.card_data = data
        a = {}
        if len(self.card_data) == 0:
            self.name_line.setEnabled(False)
            self.card_list.clear()
            self.card_list.addItem("无数据库")
            self.name_line.setPlaceholderText("无数据库")
            self.card_list.setEnabled(False)
        else:
            self.card_list.clear()
    
    def cal(self):
        # get number
        num_a_str = self.num_a_line.text()
        num_b_str = self.num_b_line.text()
        try:
            num_a = int(num_a_str)
            num_b = int(num_b_str)
        except:
            return

        # calculate
        add_result = num_a + num_b
        sub_result = num_a - num_b
        mul_result = num_a * num_b
        if num_b != 0:
            div_result = num_a // num_b
        else:
            div_result = 0
        
        # show
        self.add_line.setText(str(add_result))
        self.sub_line.setText(str(sub_result))
        self.mul_line.setText(str(mul_result))
        self.div_line.setText(str(div_result))
    
    def search_card(self):
        # 判断是否有名字
        text = self.name_line.text()
        if not self.name_line.isEnabled():
            return
        if len(text) == 0:
            self.name_line.clear()
            return
        self.card_list.clear()
        # 名字相同的优先
        if text in self.card_data.keys():
            self.card_list.addItem(text)
        # 遍历搜索符合条件的卡片
        for cardname in self.card_data.keys():
            if text in cardname and text != cardname:
                self.card_list.addItem(cardname)
    
    def show_ad(self):
        idx = self.card_list.selectedIndexes()
        if len(idx) < 1:
            return
        cardname = self.card_list.item(idx[0].row()).text()
        if cardname in self.card_data:
            args = self.card_data[cardname]
            self.atk_line.setText(str(args[0]))
            self.def_line.setText(str(args[1]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = Calculator()

    m_window.show()
    sys.exit(app.exec_())