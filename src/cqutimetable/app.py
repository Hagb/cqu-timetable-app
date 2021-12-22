from datetime import date
import toga
import toga.style.pack
from toga.style.pack import Pack
from .record import Record
from requests import Session
from pathlib import Path
from .login_win import LoginWindow, try_login
from mycqu.mycqu import access_mycqu
from mycqu.exam import Exam
import sys

session: Session
app: toga.App
cache_path: Path
data_path: Path
record: Record


# Rely on `sys.getandroidapilevel`, which only exists on Android; see
# https://github.com/beeware/Python-Android-support/issues/8
if hasattr(sys, 'getandroidapilevel'):
    current_platform = 'android'
else:
    current_platform = sys.platform


class MainApp(toga.App):
    week = ['一', '二', '三', '四', '五', '六', '日']

    def set_exam_list(self, _=None):
        print("set_exam_list")
        exams = Exam.fetch(record.username)
        # access_mycqu(session)
        self.exam_list.data.clear()
        for exam in exams[::-1]:
            self.exam_list.data.append(
                icon=toga.Icon(
                    "resources/cqutimetable.png") if exam.date >= date.today() else None,
                title=f"{exam.course.name}考试 位于 {exam.room}",
                subtitle=f'{exam.date.strftime("%Y-%m-%d")} 第 {exam.week} 周周{self.week[exam.weekday]} '
                f'{exam.start_time.strftime("%H:%M")} ~ {exam.end_time.strftime("%H:%M")}'
            )

    def refresh_after_login(self):
        self.main_window.title = f"考表 - {record.user_info.name} {record.user_info.code}"
        self.set_exam_list()

    def login_callback(self, success):
        if success:
            self.refresh_after_login()

    def login_window(self):
        login = LoginWindow(self.main_window, self.login_callback)
        self.windows.add(login)
        login.show()

    def startup(self):
        global app, cache_path, data_path, record, session
        app = self

        cache_path = self.paths.cache
        data_path = self.paths.data
        record = Record.read()
        session = record.session

        main_window = toga.MainWindow(title="考表")
        self.commands.add(toga.Command(lambda _: self.login_window(), "登录"))
        if current_platform == "android":
            from .android import cal
            self.commands.add(toga.Command(cal.cal_command, "日历"))

        self.exam_list = toga.DetailedList(
            on_refresh=self.set_exam_list, style=Pack(flex=1))

        exam_list_box = toga.Box(style=Pack(
            flex=1, direction="column", padding=10))
        exam_list_box.add(self.exam_list)

        main_window.content = exam_list_box
        self.main_window = main_window
        self.main_window.show()

        if record.username and record.password:
            if try_login(main_window, record.username, record.password):
                self.refresh_after_login()
            else:
                main_window.info_dialog("登录失败", "请重新登录")
                self.login_window()
        else:
            self.login_window()


def main():
    return MainApp()
