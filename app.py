from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.messagebox
import tkinter.simpledialog
from story import StoryTeller
from config import config
import threading
import time

# Local
from Classes import auth as Auth

# Fancy stuff
import colorama
from colorama import Fore

colorama.init(autoreset=True)


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "等线"
FONT_BOLD = "黑体"
bot_name = "故事"

story_background = "辛迪加大陆分为托雷省，尼莱省和穆拉省，其中生活着矮人，精灵，人类三个种族以及无数的怪物。你是一个来自托雷的人类男性魔法师，今年21岁。你左手持着火焰法杖，右手拿着魔法书，背包里装着能支撑一周的口粮，进入了莱肯斯雨林进行冒险。"
login_msg = "辛迪加大陆分为托雷省，尼莱省和穆拉省，其中生活着矮人，精灵，人类三个种族以及无数的怪物。你是一个来自托雷的人类男性魔法师，今年21岁。你左手持着火焰法杖，右手拿着魔法书，背包里装着能支撑一周的口粮，进入了莱肯斯雨林进行冒险。"


def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护进程
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

    def __init__(self, story_teller, background):
        self.bar = None
        self.wait_window = None
        self.story_teller = story_teller
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
        self.check_cred()

    def _on_return(self, event):
        thread_it(self._on_enter_pressed, None)

    def show_login_window(self):
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
                                command=lambda: thread_it(self._on_login, None))
        self.login_btn.grid(row=3, column=0)
        self.cancel_btn = Button(
            self.login, text="使用默认token(可能无法运行)", command=self._on_cancel_login)
        self.cancel_btn.grid(row=3, column=1)
    
    def _on_cancel_login(self):
        self.close_login_window()
        self.register_storyteller()

    def close_login_window(self):
        if self.login is not None:
            self.login.destroy()

        self.login = None

    def show_background_window(self):
        result = tkinter.simpledialog.askstring(
            title='输入背景故事', prompt='请输入背景故事（或者使用默认的）', initialvalue=self.background, parent=self.window)
        if result:
            self.background = result

    def check_cred(self):
        threading.Thread(
            target=self.start_toplevel_window("正在检查当前token是否有效")).start()
        self.expired_creds = Auth.expired_creds()
        if self.expired_creds:
            self.close_toplevel_window()
            tkinter.messagebox.showerror(
                title="token已过期", message="请输入在OpenAI注册的邮箱和密码来自动获取新的token。")
            self.show_login_window()
        else:
            self.close_toplevel_window()
            self.register_storyteller()

    # press login
    def _on_login(self, event):
        email = self.input_email.get()
        password = self.input_pwd.get()
        threading.Thread(
            target=self.start_toplevel_window("正在登陆获取token")).start()
        open_ai_auth = Auth.OpenAIAuth(email_address=email, password=password)
        print(f"{Fore.GREEN}>> Credentials have been refreshed.")
        open_ai_auth.begin()
        time.sleep(3)
        is_still_expired = Auth.expired_creds()
        self.close_toplevel_window()
        if is_still_expired:
            tkinter.messagebox.showerror(
                title="获取token失败", message="请检查邮箱和密码。")
        else:
            self.close_login_window()
            tkinter.messagebox.showinfo(
                title="获取token成功!", message="关闭此窗口并开始你的AI地牢之旅!")
            self.register_storyteller()

    def register_storyteller(self):
        self.show_background_window()
        self._init_background(self.background)
        access_token = Auth.get_access_token()
        config["session_token"] = access_token
        self.story_teller = StoryTeller(config, self.background)

    def start_toplevel_window(self, msg):
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
        if self.wait_window is not None:
            self.wait_window.destroy()

        self.wait_window = None
        self.bar = None

    def _init_background(self, background):
        if not background:
            return
        self.msg_entry.delete(0, END)
        msg1 = f">{background}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        threading.Thread(target=self.start_toplevel_window(
            "正在获取ChatGPT回复")).start()
        self._insert_message(msg, "你")
        self.close_toplevel_window()

    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        msg1 = f">{sender}{msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        self.story_teller.action(msg)
        msg2 = f"{bot_name}: {self.story_teller.response}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    story_teller = StoryTeller(config, story_background)
    app = ChatApplication(story_teller, story_background)
    app.run()
