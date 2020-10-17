from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from functools import partial
import csv
from DBDriver import ItemDatabase, SalesDatabase, ReportDb
from Errors import ErrorMessage
from configparser import ConfigParser


class SalesUIComponent():
    def __init__(self, date):
        self.reformatDate(date)
        self.setReportName1()
        self.itemdb = ItemDatabase()
        self.salesdb =  SalesDatabase()
        self.rep1 = ReportDb()
        self.rep1.createTable(self.reportName1)
        self.currentSalesName = "Sales_"+self.date
        self.salesdb.createTable(self.currentSalesName)
        self.salesData=self.salesdb.getData()
        try:
            self.totalrev=sum(self.salesData.get('total_price'))
        except:
            self.totalrev=0
        self.totalPrice = 0
        self.itemSoldList = []
        self.itemSoldPrice = []
        self.itemTotalSoldPrice=[]
        self.itemSoldQty = []
        self.itemTableStyle = """
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

        self.invoiceTableStyle = """
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
        padding: 7px
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

        self.addToListButtonStyle = """
        QPushButton
        {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(238, 238, 238), stop: 1 white, stop: 2 skyblue);
            padding: 0px;
            margin: 0px;
            border: 1px solid cyan;
            border-radius: none;
        }
        QPushButton:pressed
        {
        background-color: rgb(238, 238, 238);
        }
        """

    def reformatDate(self, date):
        self.date1=date
        self.date = date.replace("-", "_")

    def setReportName1(self):
        monthList=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = monthList[int(self.date.split("_")[1])-1]
        self.reportName1 = "Rep_"+month +"_"+self.date.split("_")[2]

    def SalesUI(self, salesTab):
        salesTab.layout = QVBoxLayout()  # Main Tab for item list, invoice and button

        self.infobox = QLabel()

        self.infobox.setStyleSheet("color: white; font-family: Comic Sans MS; font-size: 13px; font-weight:bold; margin-left: 3px;")

        self.infobox.setText("Date: "+self.date1 + "\t"*8 + "Total Earning Today: " + str(self.totalrev))

        self.infobox.setObjectName("info-box")

        self.itemArea = QWidget()  # Frame for item list
        self.itemArea.setStyleSheet("background-color: white; border-radius: 15px; ")
        self.itemArea.setFixedWidth(910)
        self.itemArea.setFixedHeight(530)

        self.itemArea.setObjectName("item-area")


        self.buttonArea = QWidget()  # Frame for buttons
        self.buttonArea.setFixedHeight(50)
        self.buttonArea.setStyleSheet(
            "background-color: transparent; margin: 0px;")

        self.setItemArea()
        self.setButtonArea()


        # Adding itemlist and button frame in main tab
        salesTab.layout.addWidget(self.infobox)
        salesTab.layout.addWidget(self.itemArea)
        salesTab.layout.addWidget(self.buttonArea)
        salesTab.setLayout(salesTab.layout)
        self.tab = salesTab
        self.tab.layout = salesTab.layout

    def setItemArea(self):

        self.itemsTable = QTableWidget(self.itemArea)
        self.itemsTable.setObjectName("item-table")
        self.itemsTable.setStyleSheet(self.itemTableStyle)

        self.itemsTable.setFixedWidth(890)
        self.itemsTable.setFixedHeight(520)

        self.itemsTable.setColumnCount(3)
        self.tableVHead = self.itemsTable.verticalHeader()
        self.tableVHead.setVisible(False)

        self.itemsTable.setHorizontalHeaderLabels(["Items", "Cost", "Add"])
        self.tableheader = self.itemsTable.horizontalHeader()
        self.tableheader.setStyleSheet("padding:0px; font-weight: bold")
        self.tableheader.setDefaultAlignment(Qt.AlignCenter)
        self.tableheader.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableheader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableheader.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.setItemData()

    def setInvoice(self):

        self.invoice = QWidget()  # Frame for invoice
        self.invoice.setWindowIcon(QIcon("dependencies/images/logo.png"))
        self.invoice.setFixedHeight(580)

        self.invoice.setWindowTitle("Invoice")

        self.invoiceLabelStyle = """
        font-weight:bold; 
        color: purple; 
        font-family: Comic Sans MS;
        font-size: 15px;
        """
        self.invoice.layout = QVBoxLayout()
        self.invoiceheading = QLabel()
        cp = ConfigParser()
        cp.read("dependencies/configfiles/config.ini")
        self.shopName = cp.get("APP_VARS", "SHOP_NAME")
        self.invoiceheading.setText("\t"+self.shopName+"\nInvoice")
        self.invoiceheading.setStyleSheet(self.invoiceLabelStyle)
        self.invoiceheading.setAlignment(Qt.AlignCenter)

        self.invoiceList = QTableWidget()

        self.invoiceList.setFixedWidth(400)

        self.invoiceList.setColumnCount(4)

        self.totalPriceBox = QLabel()
        self.totalPriceBox.setText("Total Price: 0")
        self.totalPriceBox.setAlignment(Qt.AlignCenter)
        self.totalPriceBox.setStyleSheet(self.invoiceLabelStyle)
        self.totalPriceBox.setAlignment(Qt.AlignCenter)

        self.invoiceExitBt = QPushButton()
        self.invoiceExitBt.setText("Cancel")
        #self.invoiceExitBt.setStyleSheet("border: 1px solid black; background-color: rgb(238, 238, 238); padding: 10px")

        self.invoiceExitBt.clicked.connect(self.closeInvoice)

        self.confirmbt = QPushButton()
        self.confirmbt.setText("Confirm Order")
        self.confirmbt.clicked.connect(self.confirmOrder)

        self.invoice.layout.addWidget(self.invoiceheading)
        self.invoice.layout.addWidget(self.invoiceList)
        self.invoice.layout.addWidget(self.totalPriceBox)
        self.invoice.layout.addWidget(self.invoiceExitBt)
        self.invoice.layout.addWidget(self.confirmbt)


        self.invoice.layout.setAlignment(Qt.AlignCenter)
        self.invoice.setLayout(self.invoice.layout)
        self.invtableVHead = self.invoiceList.verticalHeader()
        self.invtableVHead.setVisible(False)
        self.invoiceList.setHorizontalHeaderLabels(["Items", "Unit Cost", "Qty", "Total Price"])
        self.invtableVHead = self.invoiceList.horizontalHeader()
        self.invtableVHead.setStyleSheet("padding:0px; font-weight: bold")
        self.invtableVHead.setDefaultAlignment(Qt.AlignCenter)
        self.invtableVHead.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.invtableVHead.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.invoiceList.setStyleSheet(self.invoiceTableStyle)

        self.invoice.show()

    def confirmOrder(self):
        try:
            self.existingSaleId = self.salesdb.getData().get("sales_id")
            self.saleid = self.existingSaleId[len(self.existingSaleId)-1]
            self.saleid += 1
        except:
            self.saleid=1
        finally:
            try:
                soldList=""
                self.counter2=0
                for soldItems in self.itemSoldList:
                    soldList+=soldItems + " x" + str(self.itemSoldQty[self.counter2]) + "\n"
                    self.counter2 += 1
                self.salesdb.insertData(self.saleid, soldList, self.totalPrice)
            except Exception as ex:
                print(ex)

            try:
                self.closeInvoice()
            except Exception as ex:
                print(ex)

    def updateReport(self):
        try:
            self.rep1.insertDatafromSales(date=self.date1, t_sales=self.totalrev, profit=100)
            self.setReportTable(self.reportName1)
        except:
            expense=self.rep1.getEntry(self.date1)[2]
            if self.totalrev>expense:
                profit = self.totalrev - expense
                if(expense == 0):
                    pp=100
                else:
                    pp = (profit/expense)*100
                self.rep1.updateData(fd=self.date1, ts=self.totalrev, te=0, pp=pp, lp=0)
            else:
                if self.totalrev == 0:
                    lp=100
                else:
                    loss = expense - self.totalrev
                    lp = (loss/self.totalrev)*100
                self.rep1.updateData(fd=self.date1, ts=self.totalrev, te=0, pp=0, lp=lp)
            self.setReportTable(self.reportName1)

    def closeInvoice(self):
        self.salesData=self.salesdb.getData()
        self.totalrev=sum(self.salesData.get('total_price'))
        self.updateReport()

        try:
            self.info = self.tab.findChild(QLabel, "info-box")
            self.info.setText("Date: "+self.date1 + "\t"*7 + "Total Earning Today: " + str(self.totalrev))
        except Exception as ex:
            print(ex)
        self.SalesUI(self.tab)
        self.totalPrice = 0
        self.itemSoldList = []
        self.itemSoldPrice = []
        self.itemSoldQty = []
        self.itemTotalSoldPrice = []
        self.invoice.close()

    def setItemData(self):
        self.itemList = self.itemdb.getItems()
        self.priceList = self.itemdb.getPrice()
        self.itemCount = len(self.itemList)
        self.itemsTable.setRowCount(self.itemCount)


        self.tableItemlist=[]
        self.counter0=1
        for it in self.itemList:
            self.tableItemlist.append(str(self.counter0) + "\t" + it+"\t")
            self.counter0 += 1

        self.itemTableData = {"Items": self.tableItemlist,
                              "Price": self.priceList
                              }

        for n, key in enumerate(self.itemTableData):
            for m, item in enumerate(self.itemTableData[key]):
                self.newitem = QTableWidgetItem(item)
                self.newitem.setFlags(Qt.ItemIsEnabled)
                self.newitem.setTextAlignment(Qt.AlignCenter)
                self.itemsTable.setItem(m, n, self.newitem)

        self.itemAddButtons = []
        for i in range(0, self.itemCount):
            self.addButtonWidget = QWidget()
            self.hbox = QHBoxLayout()

            self.itemAddButton = QPushButton()
            self.itemAddButton.setText("+")
            self.itemAddButton.setFixedWidth(30)
            self.itemAddButton.setFixedHeight(25)
            self.itemAddButton.setStyleSheet(self.addToListButtonStyle)
            self.itemAddButton.clicked.connect(partial(self.addItem, i))
            self.itemAddButtons.append(self.itemAddButton)

            self.hbox.addWidget(self.itemAddButton)
            self.hbox.setAlignment(Qt.AlignCenter)
            self.hbox.setContentsMargins(0, 0, 0, 0)

            self.addButtonWidget.setLayout(self.hbox)
            self.itemsTable.setCellWidget(i, 2, self.addButtonWidget)

    def addItem(self, itemId):
        self.qty, self.ok = QInputDialog.getText(self.itemAddButton, "Quantity", "Enter quantity:")
        if (self.ok):
            try:
                self.qty = int(self.qty)
                self.setInvoice()
                self.itemSoldList.append(self.itemList[itemId])
                self.itemSoldPrice.append(self.priceList[itemId])
                self.itemTotalSoldPrice.append(int(self.priceList[itemId]) * self.qty)
                self.itemSoldQty.append(self.qty)
                self.invoiceList.setRowCount(len(self.itemList))

                self.counter = 0
                self.totalPrice = 0
                for prices in self.itemSoldPrice:
                    self.totalPrice += (int(prices)) * (self.itemSoldQty[self.counter])
                    self.counter += 1

                self.soldItems = {"Item": self.itemSoldList,
                                  "Price": self.itemSoldPrice}

                for n, key in enumerate(self.soldItems):
                    for m, item in enumerate(self.soldItems[key]):
                        self.soldItem = QTableWidgetItem(item)
                        self.soldItem.setFlags(Qt.ItemIsEnabled)
                        self.soldItem.setTextAlignment(Qt.AlignCenter)
                        self.invoiceList.setItem(m, n, self.soldItem)

                self.counter = 0
                for qtys in self.itemSoldQty:
                    self.itemqty = QLabel()
                    self.itemqty.setText(str(qtys))
                    self.invoiceList.setCellWidget(self.counter, 2, self.itemqty)
                    self.counter += 1

                self.counter4 = 0
                for tps in self.itemTotalSoldPrice:
                    self.itemTp = QLabel()
                    self.itemTp.setText(str(tps))
                    self.invoiceList.setCellWidget(self.counter4, 3, self.itemTp)
                    self.counter4 += 1

                self.totalPriceBox.setText("Total Price: " + str(self.totalPrice))

            except Exception as ex:
                em = ErrorMessage(2, ex)



    def setButtonArea(self):
        self.buttonArea.layout = QHBoxLayout()

        self.addProductBt = QPushButton()

        self.importCSV = QPushButton()

        self.delProductBt = QPushButton()

        self.delAllProductBt=QPushButton()

        self.addProductBt.setText("Add Item")
        self.importCSV.setText("Add Items From CSV")
        self.delProductBt.setText("Delete Item")
        self.delAllProductBt.setText("Delete All Items")

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

        self.addProductBt.setStyleSheet(self.buttonAreastyle)
        self.delProductBt.setStyleSheet(self.buttonAreastyle)
        self.delAllProductBt.setStyleSheet(self.buttonAreastyle)
        self.importCSV.setStyleSheet(self.buttonAreastyle)

        self.addProductBt.setFixedWidth(200)
        self.delProductBt.setFixedWidth(200)
        self.delAllProductBt.setFixedWidth(200)
        self.importCSV.setFixedWidth(200)

        self.addProductBt.clicked.connect(self.addItemToDb)
        self.delProductBt.clicked.connect(self.deleteItemfromDb)
        self.delAllProductBt.clicked.connect(self.deleteAllItemsfromDb)
        self.importCSV.clicked.connect(self.addItemsfromCSV)

        self.addProductBt.setFixedHeight(50)
        self.importCSV.setFixedHeight(50)
        self.delProductBt.setFixedHeight(50)
        self.delAllProductBt.setFixedHeight(50)

        self.buttonArea.layout.addWidget(self.addProductBt)
        self.buttonArea.layout.addWidget(self.importCSV)
        self.buttonArea.layout.addWidget(self.delProductBt)
        self.buttonArea.layout.addWidget(self.delAllProductBt)

        self.buttonArea.setLayout(self.buttonArea.layout)

    def addItemToDb(self):
        self.itemName, self.ok = QInputDialog.getText(self.itemArea, "Item Name", "Enter name of item:")
        if (self.ok):
            try:
                self.itemPrice, self.ok = QInputDialog.getText(self.itemArea, "Item Price", "Enter price of item:")
                if(self.ok):
                    self.itemPrice = int(self.itemPrice)
                    self.itemdb.insertData(self.itemName, self.itemPrice)
                    self.setItemData()
            except Exception as ex:
                ErrorMessage(7, ex)

    def deleteItemfromDb(self):
        self.itemIndex, self.ok = QInputDialog.getText(self.itemArea, "Delete Item", "Enter number of item:")
        if(self.ok):
            try:
                self.itemIndex =  int(self.itemIndex)
                self.itemdb.deleteItem(self.itemList[self.itemIndex-1])
                self.setItemData()
            except Exception as ex:
                ErrorMessage(4, ex)

    def deleteAllItemsfromDb(self):
        self.sure, self.ok = QInputDialog.getText(self.itemArea, "Delete All Item", "Are you sure that you want to delete all items? \nThis can not be undone\nType 'YES' to confirm:")
        if(self.ok):
            try:
                if(self.sure == "YES"):
                    self.itemdb.deleteAllItems()
                    self.setItemData()
                else:
                    ex = "Invalid input"
                    ErrorMessage(5, ex)
            except Exception as ex:
                ErrorMessage(5, ex)

    def addItemsfromCSV(self):
        try:
            self.options = QFileDialog.Options()
            self.fileName, _ = QFileDialog.getOpenFileName(QWidget(), "Import CSV", "","CSV Files (*.csv)", options=self.options)
            if(self.fileName):
                self.readCSV(self.fileName)
        except Exception as ex:
            ErrorMessage(None, ex)

    def readCSV(self, file):
        try:
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for data in csv_reader:
                    self.itemdb.insertData(data[0], int(data[1]))
            self.setItemData()
        except Exception as ex:
            ErrorMessage(6, ex)

