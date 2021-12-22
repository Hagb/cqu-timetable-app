import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, JUSTIFY
from . import dialogs
from . import app
from .captcha_input_win import CaptchaWindow
from mycqu.auth import login, is_logined, NeedCaptcha, IncorrectLoginCredentials
from mycqu.auth import UnknownAuthserverException, InvaildCaptcha
from mycqu.mycqu import access_mycqu
from mycqu.user import User


def try_login(win, username, password, force_relogin: bool = False):
    result = False
    captcha_exception: NeedCaptcha

    def success_login():
        nonlocal result
        access_mycqu(app.session)
        app.record.user_info = User.fetch_self(app.session)
        app.record.username = username
        app.record.password = password
        app.record.write()
        result = True

    def captcha_intput_callback(captcha: str):
        if captcha:
            try:
                captcha_exception.after_captcha(captcha)
            except IncorrectLoginCredentials:
                dialogs.incorrect_cert(win)
            except UnknownAuthserverException as e:
                dialogs.unknown_error(win, str(e))
            except InvaildCaptcha:
                dialogs.invaild_chaptcha(win)
            else:
                success_login()

    try:
        login(app.session, username, password, force_relogin=force_relogin)
    except IncorrectLoginCredentials:
        dialogs.incorrect_cert(win)
    except UnknownAuthserverException as e:
        dialogs.unknown_error(win, str(e))
    except NeedCaptcha as e:
        captcha_exception = e
        captcha_win = CaptchaWindow(e.image, captcha_intput_callback)
        app.app.windows.add(captcha_win)
        captcha_win.show()
    else:
        success_login()

    return result


class LoginWindow(toga.Window):
    def login_event(self, widget):
        if not self.id_input.value:
            self.info_dialog("缺少登录信息", "请输入学号或统一身份认证号")
            return
        if not self.passwd_input.value:
            self.info_dialog("缺少登录信息", "请输入密码")
            return
        if try_login(self, self.id_input.value, self.passwd_input.value, True):
            self.success = True
            self.close()
            if self.parent:
                user = app.record.user_info
                roles = {"student": "同学", "instructor": "老师"}
                self.parent.info_dialog(
                    "登录成功", f"欢迎 {user.name} {roles.get(user.role, user.role)}")
        else:
            self.success = False

    def on_close(self, widget):
        self.callback(self.success)

    def __init__(self, parent, callable):
        super().__init__()
        self.title = "登录"
        self.parent = parent
        self.callback = callable
        self.success = is_logined(app.session)
        app.app.paths.cache.mkdir(parents=True, exist_ok=True)
        main_box = toga.Box(style=Pack(
            direction=COLUMN, alignment="center", padding=5, flex=1))

        label_style = Pack(padding=5, text_align=JUSTIFY)

        id_label = toga.Label('学号或统一认证号：', style=label_style)
        self.id_input = toga.TextInput(style=Pack(flex=1))
        id_box = toga.Box(style=Pack(direction=ROW, padding=5))
        id_box.add(id_label, self.id_input)
        self.id_input.value = app.record.username

        passwd_box = toga.Box(style=Pack(direction=ROW, padding=5))
        passwd_label = toga.Label('统一身份认证密码：', style=label_style)
        self.passwd_input = toga.PasswordInput(style=Pack(flex=1))
        passwd_box.add(passwd_label, self.passwd_input)
        self.passwd_input.value = app.record.password

        button = toga.Button(
            '登录',
            on_press=self.login_event,
            style=Pack(padding=5),
        )

        main_box.add(id_box, passwd_box, button)
        self.content = main_box
