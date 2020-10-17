import sqlite3
from Errors import ErrorMessage as em

class ItemDatabase:
    def __init__(self):
        self.db = sqlite3.connect("dependencies/database/itemsdb.db")
        self.createTable()
        self.dbCursor=self.db.cursor()

    def createTable(self):
        try:
            self.db.execute('''CREATE TABLE ITEMS
                    (
                            ITEM CHAR(255) PRIMARY KEY NOT NULL,
                            PRICE INT NOT NULL);
                    ''')
            return
        except:
            return


    def checkTable(self):
        try:
            self.dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ITEMS';")
        except Exception as ex:
            return False

        if(self.dbCursor.fetchone() is not None):
            return True
        else:
            return False


    def insertData(self, item_name, price):
        if(self.checkTable() is True):
            try:
                self.db.execute("INSERT INTO ITEMS(ITEM, PRICE) \
                            VALUES(?, ?)", (item_name, price)
                           );
                self.db.commit()
                return True
            except:
                return False

        else:
            self.createTable()
            self.insertData(item_name, price)

    def getItems(self):
        self.itemList = []
        if(self.checkTable() is True):
            for records in (self.db.execute("SELECT * FROM ITEMS")):
                self.itemList.append(records[0])
            return self.itemList
        else:
            return False


    def getPrice(self):
        self.priceList = []
        if(self.checkTable() is True):
            for records in (self.db.execute("SELECT * FROM ITEMS")):
                self.priceList.append(str(records[1]))
            return self.priceList
        else:
            return False

    def deleteItem(self, item_name):
        if(self.checkTable() is True):
            self.db.execute(("DELETE FROM ITEMS WHERE ITEM = ?"), (item_name,));
            self.db.commit()
        else:
            return False

    def deleteAllItems(self):
        if(self.checkTable() is True):
            self.db.execute("DELETE FROM ITEMS");
            self.db.commit()
        else:
            return False

    def countEntries(self):
        if(self.checkTable() is True):
            self.dbCursor.execute("SELECT COUNT(*) FROM ITEMS")
            return (self.dbCursor.fetchone()[0])
        else:
            return False


class SalesDatabase:
    def __init__(self):
        self.db = sqlite3.connect("dependencies/database/salesdb.db")
        self.dbCursor=self.db.cursor()


    def createTable(self, table_name):
        if(self.checkTable(table_name) is True):
            self.connectTable(table_name)
        else:
            self.tableName = table_name
            self.query =  """
            CREATE TABLE {}(
            SALES_ID INT NOT NULL,
            ITEM_SOLD TEXT NOT NULL, 
            TOTAL_PRICE INT NOT NULL);
            """.format(table_name)
            try:
                self.db.execute(self.query)
                return
            except Exception as ex:
                em(None, ex)
                return

    def connectTable(self, table_name):
        self.tableName=table_name
        return

    def countEntries(self):
        if(self.checkTable(self.tableName) is True):
            self.query = "SELECT COUNT(*) FROM {}".format(self.tableName)
            self.dbCursor.execute(self.query)
            return (self.dbCursor.fetchone()[0])
        else:
            return False


    def checkTable(self, table_name):
        try:
            self.query= "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name)
            self.dbCursor.execute(self.query);
        except Exception as ex:
            return False

        if(self.dbCursor.fetchone() is not None):
            return True
        else:
            return False


    def getTablelist(self):
        self.tableList=[]
        self.query= """
            SELECT 
            name
            FROM 
            sqlite_master 
            WHERE 
            type ='table' AND 
            name NOT LIKE 'sqlite_%';
        """
        try:
            self.dbCursor.execute(self.query)
            for data in self.dbCursor.fetchall():
                self.tableList.append(data[0])
            return self.tableList
        except Exception as ex:
            em(None, ex)

    def insertData(self, sale_id, item_name, total_price):
        if(self.checkTable(self.tableName) is True):
            self.query = """
                INSERT INTO {} (SALES_ID, ITEM_SOLD, TOTAL_PRICE)
                VALUES(?, ?, ?)""".format(self.tableName)
            try:
                self.db.execute(self.query, (sale_id, item_name, total_price));
                self.db.commit()
                return True
            except:
                return False


    def getData(self):
        self.sales_id=[]
        self.item=[]
        self.totalPrice=[]
        if(self.checkTable(self.tableName) is True):
            self.query = " SELECT * FROM {}" .format(self.tableName)
            for data in self.db.execute(self.query):
                self.sales_id.append(data[0])
                self.item.append(data[1])
                self.totalPrice.append(data[2])
        else:
            return False
        if len(self.sales_id) == 0:
            return False

        self.data={
            'sales_id': self.sales_id,
            'item': self.item,
            'total_price': self.totalPrice
        }
        return self.data


class ExpenseDb:
    def __init__(self):
        self.db = sqlite3.connect("dependencies/database/expensedb.db")
        self.dbCursor=self.db.cursor()


    def createTable(self, table_name):
        if(self.checkTable(table_name) is True):
            self.connectTable(table_name)
        else:
            self.tableName = table_name
            self.query =  """
            CREATE TABLE {}(
            EXP_DESC TEXT NOT NULL, 
            COST_INC INT NOT NULL);
            """.format(table_name)
            try:
                self.db.execute(self.query)
                return True
            except Exception as ex:
                em(None, ex)
                return False

    def connectTable(self, table_name):
        self.tableName=table_name
        return

    def getTablelist(self):
        self.tableList=[]
        self.query= """
            SELECT 
            name
            FROM 
            sqlite_master 
            WHERE 
            type ='table' AND 
            name NOT LIKE 'sqlite_%';
        """
        try:
            self.dbCursor.execute(self.query)
            for data in self.dbCursor.fetchall():
                self.tableList.append(data[0])
            return self.tableList
        except Exception as ex:
            em(None, ex)


    def checkTable(self, table_name):
        try:
            self.query= "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name)
            self.dbCursor.execute(self.query);
        except Exception as ex:
            return False

        if(self.dbCursor.fetchone() is not None):
            return True
        else:
            return False


    def insertData(self, exp_desc, cost_inc):
        if(self.checkTable(self.tableName) is True):
            self.query = """
                INSERT INTO {} (EXP_DESC, COST_INC)
                VALUES(?, ?)""".format(self.tableName)
            try:
                self.db.execute(self.query, (exp_desc, cost_inc))
                self.db.commit()
            except Exception as ex:
                em(None, ex)


    def countEntries(self):
        if(self.checkTable(self.tableName) is True):
            self.query = "SELECT COUNT(*) FROM {}".format(self.tableName)
            self.dbCursor.execute(self.query)
            return (self.dbCursor.fetchone()[0])
        else:
            return False


    def deleteExp(self, exp_d):
        if(self.checkTable(self.tableName) is True):
            self.query="DELETE FROM {} WHERE EXP_DESC = ?".format(self.tableName)
            self.db.execute(self.query, (exp_d,));
            self.db.commit()
        else:
            return False

    def deleteAllItems(self):
        if(self.checkTable(self.tableName) is True):
            self.query = "DELETE FROM {}".format(self.tableName)
            self.db.execute(self.query);
            self.db.commit()
        else:
            return False


    def getData(self):
        self.exp=[]
        self.cost=[]
        if(self.checkTable(self.tableName) is True):
            self.query = " SELECT * FROM {}" .format(self.tableName)
            for data in self.db.execute(self.query):
                self.exp.append(data[0])
                self.cost.append(str(data[1]))
            self.datadict = {
                "Exp": self.exp,
                "Cost": self.cost
            }
            if len(self.exp) == 0:
                return False
            else:
                return self.datadict
        else:
            return False

class ReportDb:
    def __init__(self):
        self.db = sqlite3.connect("dependencies/database/reportdb.db")
        self.dbCursor=self.db.cursor()


    def checkTable(self, table_name):
        try:
            self.query= "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name)
            self.dbCursor.execute(self.query);
        except:
            return False
        if(self.dbCursor.fetchone() is not None):
            return True
        else:
            return False

    def createTable(self, table_name):
        if(self.checkTable(table_name) is True):
            self.connectTable(table_name)
        else:
            self.tableName=table_name
            self.query =  """
            CREATE TABLE {}(
            FOR_DATE CHAR(255) PRIMARY KEY NOT NULL,
            TOTAL_SALES INT NOT NULL, 
            TOTAL_EXPENSE INT NOT NULL,
            PROFIT_PERCENT INT NOT NULL,
            LOSS_PERCENT INT NOT NULL)
            """.format(table_name)
            try:
                self.db.execute(self.query)
                return True
            except Exception as ex:
                em(None, ex)
                return False

    def connectTable(self, table_name):
        self.tableName = table_name
        return

    def getTablelist(self):
        self.tableList=[]
        self.query= """
            SELECT 
            name
            FROM 
            sqlite_master 
            WHERE 
            type ='table' AND 
            name NOT LIKE 'sqlite_%';
        """
        try:
            self.dbCursor.execute(self.query)
            for data in self.dbCursor.fetchall():
                self.tableList.append(data[0])
            return self.tableList
        except Exception as ex:
            em(None, ex)

    def insertDatafromSales(self, date, t_sales, profit):
        if(self.checkTable(self.tableName) is True):
            self.query = """
                INSERT INTO {} (FOR_DATE, TOTAL_SALES, TOTAL_EXPENSE, PROFIT_PERCENT, LOSS_PERCENT)
                VALUES(?, ?, ?, ?, ?)""".format(self.tableName)
            self.db.execute(self.query, (date, t_sales, 0, profit, 0));
            self.db.commit()


    def insertDatafromExpense(self, date, t_expense, loss):
        if(self.checkTable(self.tableName) is True):
            self.query = """
                INSERT INTO {} (FOR_DATE, TOTAL_SALES, TOTAL_EXPENSE, PROFIT_PERCENT, LOSS_PERCENT)
                VALUES(?, ?, ?, ?, ?)""".format(self.tableName)
            self.db.execute(self.query, (date, 0, t_expense, 0, loss));
            self.db.commit()

    def updateData(self, fd, ts=0, te=0, pp=0, lp=0):
        if(self.checkTable(self.tableName) is True):
            if(ts==0):
                datalist=self.getEntry(fd)
                ts=datalist[1]
            if(te==0):
                datalist=self.getEntry(fd)
                te=datalist[2]

            self.query = """UPDATE {} 
            SET TOTAL_SALES={}, TOTAL_EXPENSE={}, PROFIT_PERCENT={}, LOSS_PERCENT={} 
            WHERE FOR_DATE='{}'""".format(self.tableName, ts, te, pp, lp, fd)
            try:
                self.db.execute(self.query);
                self.db.commit()
            except Exception as ex:
                print(ex)

    def getEntry(self, date):
        datalist=[]
        if(self.checkTable(self.tableName) is True):
            self.query = "SELECT * FROM {} WHERE FOR_DATE = '{}'" .format(self.tableName, date)
            for data in self.db.execute(self.query):
                datalist.append(data)
            return datalist[0]

    def getData(self):
        datelist=[]
        totalsaleslist=[]
        totalexpenselist=[]
        profitlist=[]
        losslist=[]
        if(self.checkTable(self.tableName) is True):
            self.query = " SELECT * FROM {}" .format(self.tableName)
            for data in self.db.execute(self.query):
                datelist.append(data[0])
                totalsaleslist.append(data[1])
                totalexpenselist.append(data[2])
                profitlist.append(data[3])
                losslist.append(data[4])
        else:
            return False
        if len(datelist) == 0:
            return False

        self.reportData={
            'dates': datelist,
            'total_sales': totalsaleslist,
            'total_expense': totalexpenselist,
            'profits': profitlist,
            'losses': losslist
        }
        return self.reportData


# obj = SalesDatabase()
# print(obj.getData())
# print(obj.getTablelist())

# obj=ItemDatabase()
# for i in range(1, 300):
#     obj.insertData("Dish"+str(i), 300)



# obj=ExpenseDb()
# obj.createTable("Exp_12_12_2000")
# print(obj.getData())
# print(obj.getTablelist())

# try:
#     for i in range(1, 100):
#         obj.insertData("Sold Fish " + str(i), i)
# except Exception as ex:
#     em(None, ex)

# obj=SalesDatabase()
# obj.createTable("T1")
# obj.createTable("T2")
# obj.createTable("T3")
# obj.createTable("T4")
# obj.createTable("T5")
#
# try:
#     obj2=ReportDb()
#     obj2.createTable("T1")
#     obj2.createTable("T2")
#     obj2.createTable("T3")
#     obj2.createTable("T4")
#     obj2.createTable("T5")
# except Exception as ex:
#     print(ex)
#
# obj3=ExpenseDb()
# obj3.createTable("T1")
# obj3.createTable("T2")
# obj3.createTable("T3")
# obj3.createTable("T4")
# obj3.createTable("T5")
#
# obj=ReportDb()
# obj.createTable("Re")
# obj.insertDatafromSales("12-12-2000", 7, 9)
# obj.updateData(fd="12-12-2000", ts=66, te=99, pp=100, lp=0)
# obj.updateData(fd="12-12-2000", ts=0, te=0, pp=6, lp=10)
# print(obj.getEntry("12-12-2000"))
# print(obj.getData())


