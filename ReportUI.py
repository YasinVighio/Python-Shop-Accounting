from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from DBDriver import *
from Errors import ErrorMessage as em

class ReportUIComponent():

    def __init__(self, date):

        self.dateShown=date
        self.setDate(date)
        self.setReportName()
        self.sales = SalesDatabase()
        self.expense = ExpenseDb()
        self.reportdb = ReportDb()
        self.reportdb.createTable(self.reportName)
        self.reportTableStyle = """
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

        self.selectbtStyle = """
        QPushButton
        {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(238, 238, 238), stop: 1 white, stop: 2 skyblue);
            color: purple;
            font-family: Comic Sans MS;
            padding: 5px;
            font-weight:bold;
            font: 12px;
        }
        QPushButton:pressed
        {
        background-color: rgb(238, 238, 238);
        }
        """

    def setReportName(self):
        self.monthList=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.month = self.monthList[int(self.databaseDate.split("_")[1])-1]
        self.reportName = "Rep_"+self.month +"_"+self.databaseDate.split("_")[2]


    def setDate(self, date):
        self.databaseDate = date.replace("-", "_")

    def RepUI(self, repTab):
        self.tab2 = repTab
        repTab.layout = QVBoxLayout()

        self.infobox = QLabel()

        self.infobox.setStyleSheet(
            "color: white; font-family: Comic Sans MS; font-size: 13px; font-weight:bold; margin-left: 3px;")

        self.setProfitInfo()


        self.infobox.setObjectName("info-box")

        self.reportArea = QWidget()  # Frame for item list
        self.reportArea.setStyleSheet("background-color: white; border-radius: 15px; ")
        self.reportArea.setFixedWidth(910)
        self.reportArea.setFixedHeight(530)


        self.selectReport = QWidget()  # Frame for buttons
        self.selectReport.setFixedHeight(50)
        self.selectReport.setStyleSheet("background-color: transparent;")
        repTab.layout.addWidget(self.infobox)
        repTab.layout.addWidget(self.reportArea)
        repTab.layout.addWidget(self.selectReport)
        repTab.setLayout(repTab.layout)

        self.setSelectReport()
        self.setReportArea()
        self.setReportTable(self.reportName)

    def setProfitInfo(self):
        try:
            sales = self.reportdb.getData().get("total_sales")
            exps = self.reportdb.getData().get("total_expense")
            total_exp = sum(exps)  # cogs
            total_sale = sum(sales)  # revenue

            if (total_sale > total_exp):
                gp = total_sale - total_exp
                profit_margin = (gp / total_sale) * 100
                self.infobox.setText("Date Today: " + self.dateShown + "\t\tSales in Month: " + str(total_sale) + "\t\tExpense in Month: " + str(total_exp) + "\t     Profit Margin: " + str(profit_margin)[0:5] + "%")
            else:
                self.infobox.setText("Date Today: " + self.dateShown + "\t\tSales in Month: " + str(total_sale) + "\t\tExpense in Month: " + str(total_exp) + "\t     No Profit")
        except:
            self.infobox.setText("Date Today: " + self.dateShown + "\t" * 7 + "No Data")

    def setExpenseTable(self, table_name):
        self.repTable.setColumnCount(2)
        self.reptableVHead = self.repTable.verticalHeader()
        self.reptableVHead.setVisible(False)

        self.repTable.setHorizontalHeaderLabels(["Expense Description", "Cost Incurred"])
        self.tableheader = self.repTable.horizontalHeader()
        self.tableheader.setStyleSheet("padding:0px; font-weight: bold")
        self.tableheader.setDefaultAlignment(Qt.AlignCenter)
        self.tableheader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableheader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.setExpenseData2(table_name)

    def setExpenseData2(self, table_name):
        self.repTable.setRowCount(0)
        self.expense.connectTable(table_name)
        self.rowNum2 = self.expense.countEntries()
        if self.rowNum2 == 0:
            self.repTable.setRowCount(self.rowNum2)
            self.infobox.setText("Date Today: " + self.dateShown + "\t" * 8 + "No Data")
            return
        else:
            self.repTable.setRowCount(self.rowNum2)
            self.expensesList2 = []
            self.counter_0 = 1
            for expenses in self.expense.getData().get("Exp"):
                self.expensesList2.append(str(self.counter_0) + "\t" + expenses + "\t")
                self.counter_0 += 1

            self.expTableData2 = {
                "Exp": self.expensesList2,
                "Cost": self.expense.getData().get("Cost")
            }

            for n, key in enumerate(self.expTableData2):
                for m, item in enumerate(self.expTableData2[key]):
                    self.newitem2 = QTableWidgetItem(item)
                    self.newitem2.setFlags(Qt.ItemIsEnabled)
                    self.newitem2.setTextAlignment(Qt.AlignCenter)
                    self.repTable.setItem(m, n, self.newitem2)

            totalCost=0
            for costs in self.expense.getData().get("Cost"):
                totalCost+=int(costs)
            self.infobox.setText("Date Today: " + self.dateShown + "\t" * 8 + "Total Expense: " + str(totalCost))

    def setReportTable(self, table_name):
        self.colnum = 5
        self.repTable.setColumnCount(self.colnum)
        self.repTable.setHorizontalHeaderLabels(["DATE", "SALES", "EXPENSE", "PROFIT", "LOSS"])
        self.reptableheader = self.repTable.horizontalHeader()
        self.reptableheader.setStyleSheet("padding:0px; font-weight: bold")
        self.reptableheader.setDefaultAlignment(Qt.AlignCenter)
        self.reptableheader.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.reptableheader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.reptableheader.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.reptableheader.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.reptableheader.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        self.setReportData(table_name)
        self.infobox = self.tab2.findChild(QLabel, "info-box")
        self.setProfitInfo()


    def setReportData(self, table_name):
        self.reportdb.connectTable(table_name)
        self.setProfitInfo()
        self.repData = self.reportdb.getData()
        if(self.repData is False):
            self.repTable.setRowCount(0)
            return
        self.rowNum = len(self.repData.get("dates"))
        self.repTable.setRowCount(len(self.repData.get("dates")))
        counter=0
        for i in range(0, self.rowNum):
            datacol1 = QLabel(str(self.repData.get("dates")[counter]))
            datacol1.setStyleSheet("margin:0px; padding:0px")
            datacol1.setAlignment(Qt.AlignCenter)
            datacol2 = QLabel(str(self.repData.get("total_sales")[counter]))
            datacol2.setStyleSheet("margin:0px; padding:0px")
            datacol2.setAlignment(Qt.AlignCenter)
            datacol3 = QLabel(str(self.repData.get("total_expense")[counter]))
            datacol3.setStyleSheet("margin:0px; padding:0px")
            datacol3.setAlignment(Qt.AlignCenter)
            datacol4 = QLabel(str(self.repData.get("profits")[counter]))
            datacol4.setStyleSheet("margin:0px; padding:0px")
            datacol4.setAlignment(Qt.AlignCenter)
            datacol5 = QLabel(str(self.repData.get("losses")[counter]))
            datacol5.setStyleSheet("margin:0px; padding:0px")
            datacol5.setAlignment(Qt.AlignCenter)
            self.repTable.setCellWidget(i, 0, datacol1)
            self.repTable.setCellWidget(i, 1, datacol2)
            self.repTable.setCellWidget(i, 2, datacol3)
            self.repTable.setCellWidget(i, 3, datacol4)
            self.repTable.setCellWidget(i, 4, datacol5)
            counter+=1

    def setReportArea(self):
        self.repTable = QTableWidget(self.reportArea)
        self.repTable.setStyleSheet(self.reportTableStyle)

        self.repTable.setObjectName("report-table")

        self.repTable.setFixedWidth(890)
        self.repTable.setFixedHeight(520)

        self.reptableVHead = self.repTable.verticalHeader()
        self.reptableVHead.setVisible(False)


    def setSalesTable(self):
        self.repTable.setColumnCount(3)
        self.repTable.setHorizontalHeaderLabels(["SALES ID", "ITEM SOLD", "TOTAL PRICE"])
        self.reptableheader = self.repTable.horizontalHeader()
        self.repTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.reptableheader.setStyleSheet("padding:0px; font-weight: bold")
        self.reptableheader.setDefaultAlignment(Qt.AlignCenter)
        self.reptableheader.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.reptableheader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.reptableheader.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)



    def setSalesData(self, table_name):
        self.sales.connectTable(table_name)
        self.salesData = self.sales.getData()
        self.rows =  self.sales.countEntries()
        self.repTable.setRowCount(self.rows)
        counter=0
        for i in range(0, self.rows):
            sale_id = QLabel(str(self.salesData.get("sales_id")[counter]))
            sale_id.setStyleSheet("margin:0px; padding:0px")
            sale_id.setAlignment(Qt.AlignCenter)
            sold_item = QLabel(str(self.salesData.get("item")[counter]))
            sold_item.setStyleSheet("margin:0px; padding:0px")
            sold_item.setAlignment(Qt.AlignCenter)
            totalprice = QLabel(str(self.salesData.get("total_price")[counter]))
            totalprice.setStyleSheet("margin:0px; padding:0px")
            totalprice.setAlignment(Qt.AlignCenter)
            self.repTable.setCellWidget(i, 0, sale_id)
            self.repTable.setCellWidget(i, 1, sold_item)
            self.repTable.setCellWidget(i, 2, totalprice)
            counter+=1

        if self.rows==0:
            totalSales = 0
        else:
            totalSales = sum(self.salesData.get("total_price"))
        self.infobox = self.tab2.findChild(QLabel, "info-box")
        self.infobox.setText("Date Today: " + self.dateShown + "\t" * 8 + "Total Sales: " + str(totalSales))

    def setSelectReport(self):

        self.selectReport.layout = QHBoxLayout()

        self.selectSales = QComboBox()
        self.selectSales.setStyleSheet("QComboBox{ background-color: white; color: purple; padding: 5px;}")
        self.selectSales.setObjectName("saleslist")


        self.selectExps = QComboBox()
        self.selectExps.setStyleSheet("QComboBox{ background-color: white; color: purple;padding: 5px;}")
        self.selectExps.setObjectName("exps-list")


        self.selectReportData = QComboBox()
        self.selectReport.setStyleSheet("QComboBox{ background-color: white; color: purple; padding: 5px;}")
        self.selectReportData.setObjectName("rep-list")

        self.selectSalesbt = QPushButton()
        self.selectSalesbt.setStyleSheet(self.selectbtStyle)
        self.selectSalesbt.setText("Select Sales Data")
        self.selectSalesbt.clicked.connect(self.getSalesList)

        self.selectExpsbt = QPushButton()
        self.selectExpsbt.setStyleSheet(self.selectbtStyle)
        self.selectExpsbt.setText("Select Expense Data")
        self.selectExpsbt.clicked.connect(self.getExpenseList)

        self.selectReportbt = QPushButton()
        self.selectReportbt.setStyleSheet(self.selectbtStyle)
        self.selectReportbt.setText("Select Report")
        self.selectReportbt.clicked.connect(self.getReportList)


        self.selectReport.layout.addWidget(self.selectSales)
        self.selectReport.layout.addWidget(self.selectSalesbt)

        self.selectReport.layout.addWidget(self.selectExps)
        self.selectReport.layout.addWidget(self.selectExpsbt)

        self.selectReport.layout.addWidget(self.selectReportData)
        self.selectReport.layout.addWidget(self.selectReportbt)

        self.selectReport.setLayout(self.selectReport.layout)

        self.setSalesList()
        self.setExpenseList()
        self.setReportList()



    def setSalesList(self):
        self.salesList = self.tab2.findChild(QComboBox, "saleslist")
        self.salesTables =  self.sales.getTablelist()
        for tabs in self.salesTables:
            tabs=tabs.replace("_", "-")
            self.salesList.addItem(tabs)


    def setExpenseList(self):
        self.expsList = self.tab2.findChild(QComboBox, "exps-list")
        self.expTables =  self.expense.getTablelist()
        for tabs in self.expTables:
            tabs = tabs.replace("_", "-")
            self.expsList.addItem(tabs)

    def setReportList(self):
        self.repList = self.tab2.findChild(QComboBox, "rep-list")
        self.repTables =  self.reportdb.getTablelist()
        for tabs in self.repTables:
            tabs = tabs.replace("_", "-")
            self.repList.addItem(tabs)

    def getSalesList(self):
        self.salesList = self.tab2.findChild(QComboBox, "saleslist")
        try:
            self.salesListName = str(self.salesList.currentText())
            self.salesListName=self.salesListName.replace("-", "_")
            self.setSalesTable()
            self.setSalesData(self.salesListName)
        except Exception as ex:
            print(ex)

    def getExpenseList(self):
        self.expenseList = self.tab2.findChild(QComboBox, "exps-list")
        try:
            self.expenseListName = str(self.expenseList.currentText())
            self.expenseListName=self.expenseListName.replace("-", "_")
            self.setExpenseTable(self.expenseListName)
        except Exception as ex:
            print(ex)

    def getReportList(self):
        self.reportList = self.tab2.findChild(QComboBox, "rep-list")
        try:
            self.reportListName = str(self.reportList.currentText())
            self.reportListName=self.reportListName.replace("-", "_")
            self.setReportTable(self.reportListName)
        except Exception as ex:
            print(ex)