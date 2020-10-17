from PyQt5.QtWidgets import QMainWindow, QWidget, QInputDialog, QTabWidget, QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from UIComponent import *
import sys, re
from configparser import ConfigParser
from Errors import ErrorMessage


class AppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        cp = ConfigParser()
        cp.read("dependencies/configfiles/config.ini")
        self.appName = cp.get("APP_VARS", "APP_NAME")
        self.setWindowIcon(QIcon("dependencies/images/logo.png"))
        self.date=self.getDate()
        if(self.date==""):
            sys.exit(0)
        try:
            self.checkDate()
        except Exception as ex:
            ErrorMessage(3, ex)
            sys.exit(0)
        try:
            self.initUI(self.date)
        except Exception as ex:
            ErrorMessage(None, ex)
            sys.exit(0)



    def checkDate(self):
        self.datePattern=r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
        self.regDate = re.search(self.datePattern, self.date)

        if "/" in self.date:
            self.dateDay = self.date.split("/")[0]
            self.dateMonth = self.date.split("/")[1]
            self.dateYear = self.date.split("/")[2]
            self.date = self.date.replace("/", "-")

        if "." in self.date:
            self.dateDay = self.date.split(".")[0]
            self.dateMonth = self.date.split(".")[1]
            self.dateYear = self.date.split(".")[2]
            self.date = self.date.replace(".", "-")

        if "-" in self.date:
            self.dateDay =  self.date.split("-")[0]
            self.dateMonth = self.date.split("-")[1]
            self.dateYear = self.date.split("-")[2]


        if((self.regDate is None) or (len(self.dateDay) != 2) or (len(self.dateMonth) != 2) or (len(self.dateYear) != 4)):
            raise Exception("Date is incorrect or is in incorrect format")

    def initUI(self, date):
        self.setWindowTitle(self.appName)
        self.setStyleSheet("QMainWindow{background-color: rgb(204, 213, 240)};")
        self.tabs=Tabs(self, date)
        self.setCentralWidget(self.tabs)
        self.setGeometry(350, 30, 850, 650)
        self.setFixedSize(QSize(950, 680))
        self.show()

    def getDate(self):
        self.date, self.ok = QInputDialog.getText(self, "Date", "Please Enter Date in format (DD-MM-YYYY):")
        return self.date

class Tabs(QWidget):
    def __init__(self, window, date):
        super(QWidget, self).__init__()
        self.layout=QVBoxLayout()
        self.tabList=QTabWidget(window)

        self.tabList.setStyleSheet("border: none;")

        self.tabSales=QWidget() #TAB FOR SALES (UI COMPONENTS WILL BE ADDED)
        self.tabSales.setStyleSheet("background-color:rgb(93, 107, 153)")
        # self.tabSales.setStyleSheet("background-color:Yellow")

        # self.tabSales2 =  QWidget()
        # self.tabSales2.setStyleSheet("background-color:rgb(93, 107, 153)")

        self.tabExp=QWidget() #TAB FOR EXPENSE (UI COMPONENTS WILL BE ADDED)
        self.tabExp.setStyleSheet("background-color:rgb(93, 107, 153)")

        self.tabRep = QWidget() #TAB FOR REPORT (UI COMPONENTS WILL BE ADDED)
        self.tabRep.setStyleSheet("background-color:rgb(93, 107, 153)")

        self.tabList.addTab(self.tabSales, "ITEMS")
        # self.tabList.addTab(self.tabSales2, "SALES")
        self.tabList.addTab(self.tabExp, "EXPENSES")
        self.tabList.addTab(self.tabRep, "REPORT")

        self.initUIComponent=UIComponents(date)

        self.initUIComponent.SalesUI(self.tabSales)
        self.initUIComponent.ExpUI(self.tabExp)
        self.initUIComponent.RepUI(self.tabRep)


        self.layout.addWidget(self.tabList)
        self.setLayout(self.layout)
