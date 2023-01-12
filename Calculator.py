from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(308, 392)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 300, 50))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(219, 255, 236);\n"
"color: rgb(255, 85, 0);")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 280, 150, 90))
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 50, 239, 112))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 0, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 1, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 2, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 1, 2, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 2, 1, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 190, 239, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_12 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_2.addWidget(self.pushButton_12, 0, 0, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout_2.addWidget(self.pushButton_14, 0, 2, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_2.addWidget(self.pushButton_13, 0, 1, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout_2.addWidget(self.pushButton_15, 1, 0, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout_2.addWidget(self.pushButton_16, 1, 1, 1, 1)
        self.pushButton_17 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout_2.addWidget(self.pushButton_17, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calculator"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_2.setText(_translate("MainWindow", "="))
        self.pushButton_5.setText(_translate("MainWindow", "3"))
        self.pushButton_4.setText(_translate("MainWindow", "2"))
        self.pushButton_3.setText(_translate("MainWindow", "1"))
        self.pushButton_6.setText(_translate("MainWindow", "4"))
        self.pushButton_7.setText(_translate("MainWindow", "5"))
        self.pushButton_9.setText(_translate("MainWindow", "7"))
        self.pushButton_8.setText(_translate("MainWindow", "6"))
        self.pushButton_10.setText(_translate("MainWindow", "8"))
        self.pushButton_11.setText(_translate("MainWindow", "9"))
        self.pushButton.setText(_translate("MainWindow", "0"))
        self.pushButton_12.setText(_translate("MainWindow", "+"))
        self.pushButton_14.setText(_translate("MainWindow", "*"))
        self.pushButton_13.setText(_translate("MainWindow", "-"))
        self.pushButton_15.setText(_translate("MainWindow", "/"))
        self.pushButton_16.setText(_translate("MainWindow", "^2"))
        self.pushButton_17.setText(_translate("MainWindow", "C"))
        self.label.setText('0')

    def add_functions(self):
        self.pushButton.clicked.connect(lambda: self.write_number(self.pushButton.text()))
        self.pushButton_2.clicked.connect(lambda: self.results())
        self.pushButton_3.clicked.connect(lambda: self.write_number(self.pushButton_3.text()))
        self.pushButton_4.clicked.connect(lambda: self.write_number(self.pushButton_4.text()))
        self.pushButton_5.clicked.connect(lambda: self.write_number(self.pushButton_5.text()))
        self.pushButton_6.clicked.connect(lambda: self.write_number(self.pushButton_6.text()))
        self.pushButton_7.clicked.connect(lambda: self.write_number(self.pushButton_7.text()))
        self.pushButton_8.clicked.connect(lambda: self.write_number(self.pushButton_8.text()))
        self.pushButton_9.clicked.connect(lambda: self.write_number(self.pushButton_9.text()))
        self.pushButton_10.clicked.connect(lambda: self.write_number(self.pushButton_10.text()))
        self.pushButton_11.clicked.connect(lambda: self.write_number(self.pushButton_11.text()))
        self.pushButton_12.clicked.connect(lambda: self.operat(self.pushButton_12.text()))
        self.pushButton_13.clicked.connect(lambda: self.operat(self.pushButton_13.text()))
        self.pushButton_14.clicked.connect(lambda: self.operat(self.pushButton_14.text()))
        self.pushButton_15.clicked.connect(lambda: self.operat(self.pushButton_15.text()))
        self.pushButton_16.clicked.connect(lambda: self.results_s())
        self.pushButton_17.clicked.connect(lambda: self.clr())


    x = False

    def write_number(self, number):
        if self.label.text() == '0' or self.x == True:
            self.label.setText(number)
            self.x = False
        else:
            self.label.setText(self.label.text() + number)


    def operat(self, number):
        if self.label.text() == '0':
            self.label.setText(number)
            self.x = False
        else:
            self.label.setText(self.label.text() + number)
            self.x = False

    def results(self):
        res = eval(self.label.text())
        self.label.setText(str(res))
        self.x = True

    def results_s(self):
        res = eval(self.label.text())
        self.label.setText(str(res**2))
        self.x = True

    def clr(self):
        self.label.setText('0')
        self.x = False


import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
