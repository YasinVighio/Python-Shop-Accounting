from SalesUIFile import SalesUIComponent as UICS
from ExpenseUI import ExpenseUIComponent as UICE
from ReportUI import ReportUIComponent as UICR

class UIComponents(UICS, UICE, UICR):
    def __init__(self, date):
        UICS.__init__(self, date)
        UICE.__init__(self, date)
        UICR.__init__(self, date)