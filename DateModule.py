from PyQt5.QtWidgets import QApplication,QWidget, QInputDialog
import sys

class Date(QWidget):
    def __init__(self):
        super().__init__()
        self.getDate()
        self.show()
        self.close()

    def getDate(self):
        self.date, self.ok = QInputDialog.getText(self, "Date", "Please Enter Date in format (DD-MM-YYYY):")
        if(self.ok)
            return self.date



app = QApplication(sys.argv)
ex = Date()
app.exec_()
app.quit()