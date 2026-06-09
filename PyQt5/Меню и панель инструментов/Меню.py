import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menu_1 = QtWidgets.QMenu(self.menubar)
        self.menu_1.setObjectName("menu_1")
        self.menu_2 = QtWidgets.QMenu(self.menu_1)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_1 = QtWidgets.QAction(MainWindow)
        self.action_1.setObjectName("action_1")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtWidgets.QAction(MainWindow)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(MainWindow)
        self.action_7.setObjectName("action_7")
        self.menu_2.addAction(self.action_3)
        self.menu_1.addAction(self.action_1)
        self.menu_1.addAction(self.menu_2.menuAction())
        self.menu_1.addSeparator()
        self.menu_1.addAction(self.action_5)
        self.menu_3.addAction(self.action_6)
        self.menu_3.addAction(self.action_7)
        self.menubar.addAction(self.menu_1.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_1.setTitle(_translate("MainWindow", "кнопка 1"))
        self.menu_2.setTitle(_translate("MainWindow", "подкнопка 2"))
        self.menu_3.setTitle(_translate("MainWindow", "кнопка 2"))
        self.action_1.setText(_translate("MainWindow", "подкнопка 1"))
        self.action_3.setText(_translate("MainWindow", "подподкнопка 1"))
        self.action_4.setText(_translate("MainWindow", "подкопка 3"))
        self.action_5.setText(_translate("MainWindow", "подкнопка 3"))
        self.action_6.setText(_translate("MainWindow", "подкнопка 1"))
        self.action_7.setText(_translate("MainWindow", "подкнопка 2"))


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Шаблон")
        self.action_1.triggered.connect(self.test)

    def test(self):
        print(1)

def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    application()