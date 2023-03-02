import copy
from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.messagebox
import tkinter.simpledialog
from typing import Callable

from story_rewrite import StoryTeller
from config import config
import threading
from concurrent import futures


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "等线"
FONT_BOLD = "黑体"

story_background = "辛迪加大陆分为托雷省，尼莱省和穆拉省，其中生活着矮人，精灵，人类三个种族以及无数的怪物。你是一个来自托雷的人类男性魔法师，今年21岁。你左手持着火焰法杖，右手拿着魔法书，背包里装着能支撑一周的口粮，进入了莱肯斯雨林进行冒险。"


def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护进程
    t.daemon = True
    t.setDaemon(True)
    # 启动
    t.start()
    # t.join()


def format_form(form, width, height):
    """设置居中显示"""
    # 得到屏幕宽度
    win_width = form.winfo_screenwidth()
    # 得到屏幕高度
    win_height = form.winfo_screenheight()

    # 计算偏移量
    width_adjust = (win_width - width) / 2
    height_adjust = (win_height - height) / 2

    form.geometry("%dx%d+%d+%d" % (width, height, width_adjust, height_adjust))


class ChatApplication:

    def __init__(self, background):
        self.type = None  # 0 for api token (official api) or 1 for openai account (free api)
        self.api_key = None  # api_key
        self.api_entry = None  # api输入框
        self.api_window = None  # api输入弹窗
        self.login = None
        self.bar = None
        self.wait_window = None
        self.story_teller = None
        self.background = background
        self.window = Tk()
        self._setup_main_window()
        self.expired_creds = None

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("AI地牢")
        self.window.resizable(width=False, height=False)
        format_form(self.window, 470, 550)
        self.window.configure(bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="AI地牢", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=0.98, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.window)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # ">你"
        self.pre_text = Label(bottom_label, font=FONT, bg="#2C3E50", text=">你")
        self.pre_text.config(fg='white', anchor="center", cursor="arrow")
        self.pre_text.place(relwidth=0.10, relheight=0.06, rely=0.008)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50",
                               fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06,
                             rely=0.008, relx=0.111)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_return)

        # send button
        send_button = Button(bottom_label, text="发送", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: thread_it(self._on_enter_pressed, None))
        send_button.place(relx=0.87, rely=0.008, relheight=0.06, relwidth=0.12)
        self.before_start()

    def _on_return(self, event):
        """
        After enter <Return> in text entry.
        """
        thread_it(self._on_enter_pressed, None)

    def show_login_window(self):
        """
        Show login window.
        """
        self.login = Toplevel()
        self.login.resizable(width=False, height=False)
        format_form(self.login, 300, 100)
        self.login.title("登陆")
        self.login.wm_attributes("-topmost", True)
        self.login.protocol("WM_DELETE_WINDOW", self._on_cancel_login)

        # email input
        self.email = Label(self.login, text="邮箱：")
        self.email.grid(row=1, column=0)
        self.input_email = Entry(self.login)
        self.input_email.grid(row=1, column=1)

        # pwd input
        self.pwd = Label(self.login, text="密码：")
        self.pwd.grid(row=2, column=0)
        self.input_pwd = Entry(self.login)
        self.input_pwd.grid(row=2, column=1)

        # login and cancel
        self.login_btn = Button(self.login, text="登陆",
                                command=self._on_login)
        self.login_btn.grid(row=3, column=0)
        self.cancel_btn = Button(
            self.login, text="使用api_keys", command=self._on_cancel_login)
        self.cancel_btn.grid(row=3, column=1)

    def _on_cancel_login(self):
        """
        Cancel login and use default session token.
        """
        self.close_login_window()
        self.show_api_window()

    def show_api_window(self):
        # 创建一个窗口
        self.api_window = Toplevel()
        self.api_window.resizable(width=False, height=False)
        format_form(self.api_window, 300, 100)

        # 关闭则弹出登录窗口
        self.api_window.protocol("WM_DELETE_WINDOW", self.show_login_window)

        # 创建一个标签
        label = Label(self.api_window, text="请输入您的api_key：")

        # 创建一个输入框
        self.api_entry = Entry(self.api_window)

        button = Button(self.api_window, text="确定", command=self.on_api_confirm)

        # 将标签和输入框放置在窗口上
        label.pack()
        self.api_entry.pack()
        button.pack()

        # 启动窗口的主循环
        self.api_window.mainloop()

    def on_api_confirm(self):
        self.api_key = self.api_entry.get()
        self.close_api_window()
        self.register_storyteller(use_default=True)

    def close_api_window(self):
        if self.api_window is not None:
            self.api_window.destroy()

        self.api_window = None

    def close_login_window(self):
        """
        Close login window
        """
        if self.login is not None:
            self.login.destroy()

        self.login = None

    def show_background_window(self):
        """
        Show background story window.
        """
        result = tkinter.simpledialog.askstring(
            title='输入背景故事', prompt='请输入背景故事（或者使用默认的）', initialvalue=self.background,
            parent=self.window)
        if result:
            self.background = result
        self._init_background(self.background)

    def before_start(self):
        """
        Check if access token is expired.
        """
        # self.expired_creds = OpenAI.token_expired()
        tkinter.messagebox.showerror(
            title="官方API已发布", message="请优先使用api_key方式登录，使用帐号密码有封号风险！")
        self.show_login_window()

    def _on_login(self):
        """
        After press login button.
        """
        self.email = self.input_email.get()
        self.password = self.input_pwd.get()
        self.close_login_window()
        self.register_storyteller(use_default=False)
        # self.open_ai_auth = OpenAI.Auth(email_address=email, password=password)
        # thread_it(self.start_toplevel_window, "正在登陆获取token")
        # thread_pool = futures.ThreadPoolExecutor()
        # self.future = thread_pool.submit(self.get_token)
        # self.check_event(self.after_get_token)

    def after_get_token(self, result):
        """
        Login线程回调函数
        """
        self.close_toplevel_window()
        if isinstance(result, bool) and result:
            print(f">> Credentials have been refreshed.")
            self.close_login_window()
            self.register_storyteller(use_default=False)
        else:
            tkinter.messagebox.showerror(
                title="获取token失败", message="请检查邮箱和密码。")

    def check_event(self, callback: Callable):
        """
        轮询
        """
        if self.future.done():
            callback(self.future.result())
        else:
            self.window.after(100, self.check_event, callback)

    def get_token(self):
        """
        获取token的进程
        """
        try:
            self.open_ai_auth.create_token()
        except:
            return False
        else:
            return True

    def register_storyteller(self, use_default):
        """
        Init background and register a storyteller
        :param use_default: Whether user use default session token in config.py. If not, use access token.
        """
        self.show_background_window()
        if use_default:
            _config_2 = {'api_key': self.api_key}
            self.type = 0
        else:
            self.type = 1
            _config_2 = {
                "email": self.email,
                "password": self.password,
                # "conversation_id": "",
                # "parent_id": "",
                # "proxy": "",
                "paid": False
            }
        print(_config_2)
        self.story_teller = StoryTeller(self.background)
        self.story_teller.type = self.type
        self.story_teller.login(_config_2)

    def start_toplevel_window(self, msg):
        """
        Start a toplevel window when waiting for response.
        :param msg: Window title
        """

        # toplevel
        self.wait_window = Toplevel()
        self.wait_window.resizable(width=False, height=False)
        format_form(self.wait_window, 300, 50)
        self.wait_window.title(msg)
        self.wait_window.wm_attributes("-topmost", True)

        # progressbar
        self.bar = Progressbar(self.wait_window, length=250, mode="indeterminate",
                               orient=HORIZONTAL)
        self.bar.pack(expand=True)
        self.bar.start(10)

    def close_toplevel_window(self):
        """
        Close toplevel window.
        """
        if self.wait_window is not None:
            self.wait_window.destroy()

        self.wait_window = None
        self.bar = None

    def _init_background(self, background):
        """
        Put background story into dialog window.
        """
        if not background:
            return
        self.msg_entry.delete(0, END)
        msg1 = f">{background}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

    def _on_enter_pressed(self, event):
        """
        After enter <Send>.
        """
        msg = self.msg_entry.get()
        thread_it(self.start_toplevel_window, "正在获取ChatGPT回复")
        self._insert_message(msg, "你")
        self.close_toplevel_window()

    def _insert_message(self, msg, sender):
        """
        Try to get message from ChatGPT and insert into dialog window.
        """
        if not msg:
            return
        self.msg_entry.delete(0, END)
        msg1 = f">{sender}{msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        res = self.story_teller.action(msg)
        msg2 = f"{res}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    app = ChatApplication(story_background)
    app.run()
