import toga

def incorrect_cert(window: toga.Window): 
    return window.info_dialog("登录失败", "错误的学工号/统一身份认证号或密码")

def invaild_chaptcha(window: toga.Window):
    return window.info_dialog("登录失败", "错误的验证码")

def unknown_error(window: toga.Window, msg: str):
    return window.info_dialog("和服务器通讯中的未知错误", msg)

def require_error(window: toga.Window, msg: str):
    return window.info_dialog("网络错误", msg)