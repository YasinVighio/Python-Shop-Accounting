from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QPushButton, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from DBDriver import ExpenseDb, ReportDb
from Errors import ErrorMessage

class ExpenseUIComponent():

    def __init__(self, date):
        self.Showndate=date
        self.reformatDate(date)
        self.expdb = ExpenseDb()
        self.rep2 = ReportDb()
        self.currentExpName = "Exp_"+self.date
        self.expdb.createTable(self.currentExpName)
        self.setReportName2()
        self.rep2.createTable(self.reportName2)
        self.todaysExpense=[]
        try:
            for expenses in self.expdb.getData().get("Cost"):
                self.todaysExpense.append(int(expenses))
            self.totalExpenseToday = sum(self.todaysExpense)
        except:
            self.totalExpenseToday=0
        self.expTableStyle = """
        *
        {
        background-color: white; 
        border-radius: 15px;
        padding: 0px;
        padding-left: 10px;
        margin: 0px;
        padding-top: 10px;
        padding-bottom: 16px;
        font-family: Comic Sans MS;
        font-weight: bold;
        font-size: 13px;
        color: purple;
        }

        QTableWidget::item 
        { 
        padding: 0px
        }

        ::section
        {
        background-color:rgb(93, 107, 153);
        color: white;
        border-radius:30px;
        margin-bottom: 15px;
        }

        QScrollBar:vertical {
            border: 0px solid #999999;
            background:white;
            width:20px; 
            border-radius: 15px;    
            margin: 10px 0px 10px 0px;
        }
        QScrollBar::handle:vertical {         

            min-height: 0px;
          	border: 0px solid red;
			border-radius: 4px;
			background-color: red;
        }
        QScrollBar::add-line:vertical {       
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
                """

    def reformatDate(self, date):
        self.date = date.replace("-", "_")

    def setReportName2(self):
        monthList=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = monthList[int(self.date.split("_")[1])-1]
        self.reportName2 = "Rep_"+month +"_"+self.date.split("_")[2]

    def ExpUI(self, expTab):
        expTab.layout=QVBoxLayout()

        self.infobox = QLabel()

        self.infobox.setStyleSheet(
            "color: white; font-family: Comic Sans MS; font-size: 13px; font-weight:bold; margin-left: 3px;")

        self.infobox.setText("Date: " + self.Showndate + "\t" * 8 + "Total Expense Today: " + str(self.totalExpenseToday))

        self.infobox.setObjectName("info-box")

        self.expenseArea = QWidget()  # Frame for item list
        self.expenseArea.setStyleSheet("background-color: white; border-radius: 15px; ")
        self.expenseArea.setFixedWidth(910)
        self.expenseArea.setFixedHeight(530)

        self.setExpArea()

        self.buttonArea2 = QWidget()  # Frame for buttons
        self.buttonArea2.setFixedHeight(50)
        self.buttonArea2.setStyleSheet(
            "background-color: transparent; margin: 0px; border-radius: 15px")

        self.setButtonArea2()

        expTab.layout.addWidget(self.infobox)
        expTab.layout.addWidget(self.expenseArea)
        expTab.layout.addWidget(self.buttonArea2)
        expTab.setLayout(expTab.layout)
        self.tab1 = expTab



    def setinfoArea(self):
        self.todaysExpense=[]
        try:
            for expenses in self.expdb.getData().get("Cost"):
                self.todaysExpense.append(int(expenses))
            self.totalExpenseToday = sum(self.todaysExpense)
        except:
            self.totalExpenseToday=0
        try:
            self.infoArea = self.tab1.findChild(QLabel, "info-box")
        except:
            return
        self.infoArea.setText("Date: " + self.Showndate + "\t" * 8 + "Total Expense Today: " + str(self.totalExpenseToday))

    def setExpArea(self):
        self.expTable = QTableWidget(self.expenseArea)
        self.expTable.setStyleSheet(self.expTableStyle)

        self.expTable.setFixedWidth(890)
        self.expTable.setFixedHeight(520)

        self.expTable.setColumnCount(2)
        self.tableVHead = self.expTable.verticalHeader()
        self.tableVHead.setVisible(False)

        self.expTable.setHorizontalHeaderLabels(["Expense Description", "Cost Incurred"])
        self.tableheader = self.expTable.horizontalHeader()
        self.tableheader.setStyleSheet("padding:0px; font-weight: bold")
        self.tableheader.setDefaultAlignment(Qt.AlignCenter)
        self.tableheader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableheader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.setExpenseData()

    def setExpenseData(self):
        self.rowNum =  self.expdb.countEntries()
        if self.rowNum == 0:
            self.expTable.setRowCount(self.rowNum)
            self.setinfoArea()
            return
        else:
            self.expTable.setRowCount(self.rowNum)
            self.expensesList = []
            self.counter_0=1
            for expenses in self.expdb.getData().get("Exp"):
                self.expensesList.append(str(self.counter_0) +"\t"+expenses+"\t")
                self.counter_0+=1

            self.expTableData = {
                "Exp": self.expensesList,
                "Cost": self.expdb.getData().get("Cost")
            }


            for n, key in enumerate(self.expTableData):
                for m, item in enumerate(self.expTableData[key]):
                    self.newitem = QTableWidgetItem(item)
                    self.newitem.setFlags(Qt.ItemIsEnabled)
                    self.newitem.setTextAlignment(Qt.AlignCenter)
                    self.expTable.setItem(m, n, self.newitem)

            self.setinfoArea()

    def setButtonArea2(self):
        self.buttonArea2.layout = QHBoxLayout()

        self.addExpenseBt = QPushButton()

        self.delExpenseBt = QPushButton()

        self.delAllExpensetBt=QPushButton()

        self.addExpenseBt.setText("Add Expense")
        self.delExpenseBt.setText("Delete Expense")
        self.delAllExpensetBt.setText("Delete All Expenses")

        self.buttonAreastyle= """
        QPushButton
        {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(238, 238, 238), stop: 1 white, stop: 2 skyblue);
            padding: 0px;
            margin: 5px;
            border-radius: none;
            margin-bottom: 20px;
            color: purple;
            font-family: Comic Sans MS;
            font: 15px;
        }
        QPushButton:pressed
        {
        background-color: rgb(238, 238, 238);
        }
        """

        self.delExpenseBt.setStyleSheet(self.buttonAreastyle)
        self.delAllExpensetBt.setStyleSheet(self.buttonAreastyle)
        self.addExpenseBt.setStyleSheet(self.buttonAreastyle)

        self.delExpenseBt.setFixedWidth(200)
        self.delAllExpensetBt.setFixedWidth(200)
        self.addExpenseBt.setFixedWidth(200)

        self.addExpenseBt.clicked.connect(self.addExpToDb)
        self.delExpenseBt.clicked.connect(self.deleteExpfromDb)
        self.delAllExpensetBt.clicked.connect(self.deleteAllExpfromDb)

        self.addExpenseBt.setFixedHeight(50)
        self.delExpenseBt.setFixedHeight(50)
        self.delAllExpensetBt.setFixedHeight(50)

        self.buttonArea2.layout.addWidget(self.addExpenseBt)
        self.buttonArea2.layout.addWidget(self.delExpenseBt)
        self.buttonArea2.layout.addWidget(self.delAllExpensetBt)

        self.buttonArea2.setLayout(self.buttonArea2.layout)

    def addExpToDb(self):
        self.expName, self.ok = QInputDialog.getText(self.expenseArea, "Expense Description", "Enter description of expense:")
        if (self.ok):
            try:
                self.expCost, self.ok = QInputDialog.getText(self.expenseArea, "Cost", "Enter cost incurred on expense:")
                if (self.ok):
                    self.expCost = int(self.expCost)
                    self.expdb.insertData(self.expName, self.expCost)
                    self.setExpenseData()
                    self.updateReportfromExpense()
            except Exception as ex:
                ErrorMessage(7, ex)


    def deleteExpfromDb(self):
        self.expIndex, self.ok = QInputDialog.getText(self.expenseArea, "Delete Expense", "Enter expense number:")
        if(self.ok):
            try:
                self.expList =  self.expdb.getData().get("Exp")
                self.expIndex =  int(self.expIndex)
                self.expdb.deleteExp(self.expList[self.expIndex-1])
                self.totalExpenseToday=0
                try:
                    for exps in self.expdb.getData().get("Cost"):
                        self.totalExpenseToday+=int(exps)
                except Exception as ex:
                    print(ex)
                    self.totalExpenseToday=0
                self.updateReportfromExpense()
                self.setExpenseData()
                self.setinfoArea()
            except Exception as ex:
                ErrorMessage(4, ex)

    def deleteAllExpfromDb(self):
        self.sure, self.ok = QInputDialog.getText(self.expenseArea, "Delete All Item", "Are you sure that you want to delete all expenses? \nThis can not be undone\nType 'YES' to confirm:")
        if(self.ok):
            try:
                if(self.sure == "YES"):
                    self.expdb.deleteAllItems()
                    self.setExpenseData()
                    self.totalExpenseToday=0
                    self.updateReportfromExpense()
                else:
                    ex = "Invalid input"
                    raise Exception(ex)
            except Exception as ex:
                ErrorMessage(5, ex)

    def updateReportfromExpense(self):
        try:
            self.rep2.insertDatafromExpense(date=self.Showndate, t_expense=self.totalExpenseToday, loss=100)
            self.setReportTable(self.reportName2)
        except:
            totalrev=self.rep2.getEntry(self.Showndate)[1]
            if self.totalExpenseToday>totalrev:
                loss = self.totalExpenseToday - totalrev
                if(totalrev == 0):
                    lp=100
                else:
                    lp = (loss/self.totalExpenseToday)*100
                self.rep2.updateData(fd=self.Showndate, ts=0, te=self.totalExpenseToday, pp=0, lp=lp)

            else:
                profit = totalrev - self.totalExpenseToday
                if self.totalExpenseToday == 0:
                    pp=100
                else:
                    pp = (profit/self.totalExpenseToday)*100
                self.rep2.updateData(fd=self.Showndate, ts=totalrev, te=self.totalExpenseToday, pp=pp, lp=0)
            self.setReportTable(self.reportName2)