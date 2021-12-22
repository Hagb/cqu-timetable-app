from typing import Callable, Any
from . import app
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, JUSTIFY, CENTER


class CaptchaWindow(toga.Window):
    def __init__(self, image: bytes, callback: Callable[[str], Any]):
        super().__init__(title="需要输入验证码")

        app.cache_path.mkdir(parents=True, exist_ok=True)
        with open(app.cache_path.joinpath('captcha.jpg'), 'wb') as file:
            file.write(image)
        main_box = toga.Box(
            style=Pack(direction=COLUMN, alignment=CENTER,
                       flex=1, padding=40)
        )

        image_view = toga.ImageView(
            toga.Image(str(app.cache_path.joinpath('captcha.jpg'))),
            style=Pack(
                width=app.app.main_window.size[0]*3//4, height=app.app.main_window.size[1]/3, flex=1)
        )
        main_box.add(image_view)

        input_box = toga.Box(style=Pack(direction=ROW, padding=5))
        input_view = toga.TextInput(style=Pack(flex=1))
        label = toga.Label(
            '请输入验证码：',
            style= Pack(padding=5, text_align=JUSTIFY)
        )
        input_box.add(label)
        input_box.add(input_view)

        self.ok = False

        def ok_press(_):
            if not input_view.value:
                self.info_dialog("请输入验证码", "验证码不能留空")
                return
            else:
                self.ok = True
                self.close()

        def cancel_press(_):
            self.close()

        def on_close(_):
            if not self.ok:
                callback("")
            else:
                callback(input_view.value)

        button_cancel = toga.Button(
            "取消", on_press=cancel_press, style=Pack(padding=5))
        button_ok = toga.Button(
            '确定', on_press=ok_press, style=Pack(padding=5))
        button_box = toga.Box(style=Pack(
            direction=ROW, padding=5, alignment=CENTER))
        button_box.add(button_cancel)
        button_box.add(button_ok)
        main_box.add(input_box)
        main_box.add(button_box)
        self.on_close = on_close
        self.content = main_box
