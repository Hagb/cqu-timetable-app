import toga
from toga.style.pack import Pack
from mycqu.exam import Exam
from requests import RequestException
from datetime import datetime
from .. import app
from .. import dialogs


class CalWin(toga.Window):
    def set_cal_list(self, _=None):
        self.python_cal.cals.clear()
        self.java_cal.getCalendars()
        self.cal_list.data.clear()
        for cal_id, title, account in self.python_cal.cals:
            self.cal_list.data.append(
                icon=None,
                title=title,
                subtitle=account,
                pk=cal_id
            )

    def cal_selected(self, _, row):
        cal_id = row.pk
        try:
            exams = Exam.fetch(app.record.username)
        except RequestException as e:
            dialogs.require_error(self, str(e))
            return
        for event_id in app.record.event_ids:
            self.java_cal.delEvent(event_id)
        app.record.event_ids.clear()
        for exam in exams:
            app.record.event_ids.append(
                self.java_cal.addEvent(
                    cal_id,  # calId
                    exam.course.name,  # title
                    exam.room,  # location
                    exam.course.name + "考试",  # description
                    int(
                        datetime.combine(exam.date, exam.start_time).timestamp()*1000),  # dtstart
                    int(
                        datetime.combine(exam.date, exam.end_time).timestamp()*1000),  # dtend
                    False,  # all_day
                    "",  # rrule
                )
            )
        app.record.write()
        self.close()
        app.app.main_window.info_dialog("导入成功", "成功导入考表至 " + row.title)

    def __init__(self, python_cal, java_cal):
        super().__init__(title="选择要导入考表的日历")
        self.python_cal = python_cal
        self.java_cal = java_cal
        main_box = toga.Box()
        self.cal_list = toga.DetailedList(
            on_refresh=self.set_cal_list,
            on_select=self.cal_selected,
            style=Pack(flex=1)
        )
        main_box.add(self.cal_list)
        self.content = main_box
        self.set_cal_list()
