from typing import List, Tuple
from rubicon.java import JavaInterface, JavaClass
from rubicon.java.jni import java
from .cal_win import CalWin
from .. import app


class PythonCal(JavaInterface("name/hagb/cqutimetable/IPythonCal")):
    cals: List[Tuple[int, str, str]]

    def __init__(self):
        super().__init__()
        self.cals = []

    def addCal(self, calId, displayName, accountName):
        self.cals.append((calId, displayName, accountName))


JavaCal = JavaClass("name/hagb/cqutimetable/HagbCalendar")


def cal_command(_):
    python_cal = PythonCal()
    java_cal = JavaCal(__jni__=java.NewGlobalRef(JavaCal(python_cal)))
    if java_cal.requirePermission():
        cal_win = CalWin(python_cal, java_cal)
        app.app.windows.add(cal_win)
        cal_win.show()
