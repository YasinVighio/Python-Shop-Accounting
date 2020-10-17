from PyQt5.QtWidgets import QMessageBox
from datetime import datetime


class ErrorMessage():
    def __init__(self, errorId, exc):
        self.writelog(exc)
        self.showErrorDialog(errorId)

    def showErrorDialog(self, errorId):
        self.msg = QMessageBox()
        if errorId == 1:
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setWindowTitle("Critical Error")
            self.msg.setText("An error occured")
            self.msg.setInformativeText("Files essential for program to run are missing or corrupted")
            self.msg.setDetailedText("See the log.txt in installation folder")
            self.msg.exec_()
        elif errorId == 2:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error Message")
            self.msg.setText("An error occured")
            self.msg.setInformativeText("Please retry. Perhaps input type in not correct")
            self.msg.setDetailedText("Input should be a number and see the log file in installation folder for more details")
            self.msg.exec_()

        elif errorId == 3:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error Message")
            self.msg.setText("An error occured")
            self.msg.setInformativeText("Please Enter Date. If entered, enter in required format")
            self.msg.setDetailedText("Please enter date the in required format")
            self.msg.exec_()

        elif errorId == 4:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error Message")
            self.msg.setText("An error occured")
            self.msg.setInformativeText("Please enter correct item index")
            self.msg.setDetailedText("Item does not exist or index number is not of correct type. See log.txt for more info")
            self.msg.exec_()

        elif errorId == 5:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error Message")
            self.msg.setText("An error occured")
            self.msg.setInformativeText("Invalid input")
            self.msg.setDetailedText("Item table does not exist or retype 'YES'. See log.txt for more info")
            self.msg.exec_()

        elif errorId == 6:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error Message")
            self.msg.setText("An error occured")
            self.msg.setInformativeText("There is an error in CSV File values")
            self.msg.setDetailedText("Please check the CSV file and log.txt")
            self.msg.exec_()

        elif errorId == 7:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error Message")
            self.msg.setText("An error occured")
            self.msg.setInformativeText("Please enter correct input type")
            self.msg.setDetailedText("Maybe input type is not correct. Please check log.txt")
            self.msg.exec_()

        elif errorId == None:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error Message")
            self.msg.setText("An unknown error occured")
            self.msg.setInformativeText("Please see the log file")
            self.msg.setDetailedText("Goto installation folder and see log.txt")
            self.msg.exec_()

    def writelog(self, exc):
        self.logfile = open("log.txt", "a")
        self.now = datetime.now()
        self.logfile.write(str(self.now) + ":\t" + str(exc) + "\n\n")
        self.logfile.close()