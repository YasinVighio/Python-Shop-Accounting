# Python-Shop-Accounting
Python version = Python 3.8
PyQt5 version = 5
Sqlite3
DEPENDENCIES TO BE INSTALLED
pip install PyQt5
if you want to build as exe for windows or for linux you need to 
pip uninstall PyQt5-sip
and then
pip install PyQt5-sip

To run create a virtual environment install PyQt5 in it and add all these files into the virtual env.

This software is simple accounting for small businesses and shops.
The app name can be changed by editing the config.ini file in /dependencies/configfiles/
Also the shop name can be changed by editing config.ini.
When the software starts it prompts the user to enter date in specified format (Software won't start if date not in correct format)
Also the software checks that dependencies folder exists or not. If it does not exists software does not start. 
Dependencies folder contains config files, icons and databases.
When the software starts there are three tabs [ITEMS, EXPENSES, REPORTS]
There are 4 databases in total:
  1. Item DB
  2. Sales DB
  3. Expense DB
  4. Report DB
In item db you can add/delete items. 
you can also add items by using csv file
Sales db is auto created when transaction occurs.
Expense db is also auto created when expense is added.
Report Db has the records of days, total sales, total expense and profit/loss markup.
In items tab items are shown and can be added or deleted.
Items can be added into invoice by [+] beside them.
If [+] is pressed, system will ask for quantity and after quantity is entered in correct format, system will add item to invoice and invoice window will be opened.
There is confirm order button in invoice window.
If button is pressed items in invoice along with their total price and quantity will be added to Sales DB.
In sales DB for every date a table is created with date as name.
In Expenses tab expenses can be added/deleted for the day.
As expense is added it is added to expense db.
Expense db also creates table for every date.
When sales or expense db is updated, report db is automatically updated.
In report tab the old sales data and present sales data from sales db tables can be shown. 
Expense data (old and present) is also shown in report tab. 
Old and present report is also there. User can see Report of previous months as well.
In reports db there is table for month of every date entered.
In monhtly table of report db, total sales, expense and profit/loss markup is shown.
There is drop down list for sales, expense and report tables in report tab.
Total profit margin of month is shown at top oof report tab.
