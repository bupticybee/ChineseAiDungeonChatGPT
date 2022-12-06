from tkinter import *
from tkinter.ttk import Progressbar
from story import StoryTeller
import threading

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "等线"
FONT_BOLD = "黑体"
bot_name = "ChatGBT"

config = {
    "Authorization": "<API-KEY>",  # This is optional
    "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..G1DA27klUIERIXs8.-ewpFWYSrJvoByWvJdx6OtjdVneHZsvHP7oVhLNoJh5K5tOYXvHB0IFczhgsBzei2MRx43Yi4uRyGpxIArMGgaJ7i1cKvoZJ0259UapG10IS21R5tTB-oLdhP_9-fI19Q_jJyn2vNHyf0Efe0jSMhbPbbTltZWP-xkyDuKqfY1wi_K1L5ysJ8FlJ5hLyN4s87OpELm_KgsyPCLJxWA8unFfGmFUUV0-o5P_q6y-iTO1_9EA9y9I98xxJ9qorwbTF4_DoqluFRvMkl4W0i9IJlOEMRTay-xqfof4wnPEhH2xqGEeBfeuV_dKputPIkpZ6FEUdbu47FuPGxQFig3AblUM0J57QcV5MfJLgs0umxWK49DIcRwjceSpa6iYkeLjTtV1VbVPiodwjBNRrnnpE7wtq3-2r3pSiexQUo0DuOqpNbZRr3A37cvUuiZFgM--G0_3QIcqy7blz5DMSA-thpPEhIQu3aoaS78M4wa-wuVYRFxC3IqI3iXiortmLpKAhoh2zVSTyuwNw-unm3J70rbgic3diBUrvi9K4vOLSLNVQUqZvyCsDSCTDoFWcGZGNdYqboOA1nll22wTc_CoTtbRGObP3N3BiH4OjZmQ11ZCBGySQz5EXoWgzNxjLVtehWneaFKar6gFAEW-_m7oF9-9DldHHMAb3Gk6RTn6X0oAaWCvNk-X3sNoEBzBVMnTADEpE-Stu3f7UEQ7IssyAIasQEpt43fyXvr-kSLM_G8IDs-8PyWYScoBJtIFANdAD9hdrm7X9jt21IXJ8WcLHxcIF2g0T0OnA_t7s1nIOi1TK1-Db79UrGGxFT3kk08VyB3zx_s2XSjGGZG6YL1TryTfFZINaFhfcymiwZO_9eYMc8vAn5NPY1DcZo7CzcYu3OvcdUyYewf3Ktao75qJeMt5xWvYyre_wdICExxJBj4HCj-hwv4xakeP5X1laVyfBlsTtAnySyIDORU3vJosKqfPdKg_4pXfHFLz-I-uEogy2Ywy_GKRnQwTOGS5UmAeuclDDedqeUY5F0fzOTZigSchRSjb6RCQT2fafAiMbxyx7ix6AKVpiPVDpNTg7rP-DoxQaLnJS4z3DMzTFmcr_ey8xQsBAZv94YAJ1EKGz0DayhEjfqIfR_S-hWZjezTZb1hMFf5fXlyq49F4nImM1ETdgVvLXd4XljwaSDr68h_wRsG8UlxLuN1hbM0bQIsXd0tubCkhf8r8dMAq5TfWEsBG1diNRJXG26UneOoHi83O_YuidW9OO0mwuov1eTBWSA0b06AAPjxxRriuceIOJs33Ofz9rl2rDm7USn_nmVH5BgfScY1SU1-ODRol4TYap-OLjfi9-3dwsqQc_lzAsf1dQFtsGLJv10CgXdgj5jXh6M2ttRHiBOW5yj-csLHzTdUAa1fB5Al1exHIX94u_mHIVafItFD-TXwZFCHlIuc5AqPUrGpR3tJtIeNvWFgmgN1KDMLd0l_ryzL_t-alSIMNg4sTrVNdwhY-k2l3EdlsoChFkkfLQykoIT832tci_aIO1n2RoCNayQGFXxbbOQGmD9bIHSq6sLdae0C5zb08K_6ioXy6EnnYd0V1QzsHDpwUyxQO8D3w1gPq_tBXXso0MYzCwSMBfIpdi7QkZw62-AguRl1pRW0nQZsBeyhL9McUqNxeyokGYxGt1gt6_0Re3cdzqC7AoLMv9s2pPBx-jdVbC38n71mzmYdCcFUDUJYPFWkY2aXmDo57lZsf77TpbIoSAwPmQ7FrOL1gru2Q8vOtLfFTwBLDOerOVLhYemTsIpueSF0Qb0FFbwvJy5a-QfF13yHQ-8mG-utt5wamYqjRD-8Emh6fkvj4OJPeGk-dQzf68jI_1VY75TXaDyT5EijYY4AAZ1BSQ-4NyWM44h1Trhog2EIdsSMNIrZdAzm7rZrzMFUAHaeTnnBDYnA1c-kO5HKqht_lhvP3-cfO9gzI3EU-ix4xQIalI2xZ3EdmWBcfI5GexxDR7S48pO1zfBRPUVw4wk7pltcUyv7uaJP4Q8CSfHSfP1IiQh6ZU9YRjf1Cplw.bLXZLMTt2uyt4Ri1LpFd3A"
}

story_background = "辛迪加大陆分为托雷省，尼莱省和穆拉省，其中生活着矮人，精灵，人类三个种族以及无数的怪物。你是一个来自托雷的人类男性魔法师，今年21岁。你左手持着火焰法杖，右手拿着魔法书，背包里装着能支撑一周的口粮，进入了莱肯斯雨林进行冒险。"


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

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("AI地牢")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

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
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.111)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="发送", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: thread_it(self._on_enter_pressed, None))
        send_button.place(relx=0.87, rely=0.008, relheight=0.06, relwidth=0.12)
        self._init_background(self.background)
        # self.start_toplevel_window()

    def start_toplevel_window(self):
        # toplevel
        self.wait_window = Toplevel()
        self.wait_window.resizable(width=False, height=False)
        format_form(self.wait_window, 300, 50)
        self.wait_window.title("正在获取ChatGPT回复")
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
        threading.Thread(target=self.start_toplevel_window()).start()
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
