from PyQt5.QtWidgets import QApplication
from Errors import ErrorMessage
import os.path as osp


if __name__ == '__main__':
    try:
        from App import *
        app=QApplication(sys.argv)
        if (osp.isdir("dependencies/invoice") or osp.isdir("dependencies/images") or osp.isdir("dependencies/database")):
            mainWindow=AppUI()
        else:
            raise Exception("Dependency files are missing")
        app.exec_()
        app.quit()
    except Exception as ex:
        ErrorMessage(1, ex)
