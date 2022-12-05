from tkinter import *
from story import StoryTeller

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "等线"
FONT_BOLD = "黑体"
bot_name = "ChatGBT"

config = {
    "Authorization": "<API-KEY>",  # This is optional
    "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..MISh5V60Gcipu31t.t3f0RfS2WtIovZ5zPxGQfxz25V4ZmfsbLsYNoIJ8OU9ErlCbgjBFm7VkHOhg0wKQk08t99g-ka2UtRcNP6q4hOCO8D15GwtrY5mah4n_6uh90Lo_912DDD_IrXX5GU89ce3aMRDae8CRxVeXhOHRX1zOARL6KxClNdVaWIPCWtNeUvSrxxQEesu9bSb2jBTqU5MSqFUrkLjyYRr6H8Ucc-S_4uJVt8Rul0MYTe8gRRRehuAQOoy85UnCTS-0InWJEpwQFgL8d5XfY2R-RjG6rj-W-QrKAd49QyTm7XoGUXZ7unRn7rnxQAT5ROvIkUzbtR0fTc0zRjjhfJyPMPJnBIx7cOvmdj4LzW2SdId3HzfLbvGG4IXCaf0eIi3J8Q6IjcSbdvo5uY4gg6XJ65JEf-w0rVHY-2wBy70oQ4eRZwsyqSkI8Xt8-KdgW5Xs6HTrVEiOYy_saJy2qMPuZ8lW8ic8yK3THsMT-wCOpzEZvwwVeUhoJi9ZW4n9SsUBgiQh3pEqJ_Bm6QuARhSR2OxDRVXgXP71k9vFvyT2t0XkXZmC-x1S_ppGf9Y2g0YtFad7j4MQMGzlvACcb6I_5rdiBdxUsbE_U63g7c8t9S8d38WWuQKSC3wUi9TT5HcUdjLrEdYUawB39Eg7Gu6VvUacNXeEARlY0CSuSeiRkyk9b9P_-fMyhrRMWz_Yf_rneDM9OmRtaTIEW2XSBHmLN3FRylpLi-gQhIh-O2HCGlmpNyiOMuRuT0V1hrlEAnoFKiR4fHiIVK30jM-zhZ4Yi5XdM5h2fCrS-gpH4zYdP-1fJwFMG5cbElhTZJ9-Vjf4UsYfYdDS0pIBMXwQNu9s4xxn-McnORiWXpaniqRzDbUezlmvVFgeNmZYuBBryiyUKqrllfbmQjYV8sRCAqnUq2Dgzo3SqsxyVQoeadIWLkrVUDeXn8c2aDaWDmU03QYFgRd3Ga3-sD3qz5-7AW0YXnhZnIKfB63MRzD2wG6ycH8D1UEKJN9IcwdQcMuwbtMydDj2gQjh0g3eabC9dBXzvyaORW2QLMw2Uj7KbIPwRneUxpNaTQMb2b3gfD_q3I_gZ_Qn-sETmUjPtk90YzAtnFrKA3Lldr9rAiKBUoWz7oqoknG1i2q9yMiScWN3S43fwspEb0woGp-qqcJMHyTPltZMwUiT1LZqU3PlpVF1fHCv4WXTsBgjSYjXY-F5BlQRCo0AC4y1kOwoKn8QfewqbfIBRzrlgOKemuXqweCOFbDmleVWI8zXn45guO-PvAoD9G6E6qlOHGw6tGHMhRL4wXcKQQ9f8VuK26VR5exlrARtbf_UQRCTeSl70LRyAcltwIth9VTTbjfRCheSk-MNp-gee1w9tGDtlt-iL7BzQ5SFnRgTAIS_9hzAT1ry6Bvk0e2RUBMqy0P9u5zFklFDpk9rRvz0H8oDtJp9u6V5b3P0FdRyC6p-1J_ugLJrfLreu5GrpCKrLbn1BxQHoH80pGLrbFU_d34bg3RJZr04Ky-1b3LE1nGF4Wn2d24ny1ERL9Bii8XbaeHk40367xOKaaxS4mvNRCleFYQOxG5P1ofwojtR2JkZbw1VQjrdU8f55WoSSrXnB8ovW-UB5EJxT4G3XgDAPSfTcPojHInw4stw3W4XEqBpFKAvS89Aif8GxgCmEU56CNFOI6KoNlte0Y8tpAMpP9B1TmOjON2_Fzhvd0Qy5cSTyKO3HV6_f4XxsXljcFy19_2o-mDZ1K5tZFKEkqfJwYQYzBQHIvxopA6_pZxNdx_J1up6HpfCoOK0-g-Ah_kIM-vu97w0LyWV000BZe48QtF3Rx5DO8KzzbJHAt6M2u7tXHNYELzASlthVplpef5xZ_nvtzp3DWz7yFOskz1b-Ov89ihdpXIF7UZ79j4vMud_24TgS5eGVS4IkWRyLPp_W9IJzpQRXxCnQZKfhk3vO4eDjfQ-AdU0s00b7iN7pz95-VlvMQ-NoFHovDfk0eNZHiCClaTFxGcNTK6yb9jKl-oem7dh21rES1dAkX8P1Pf5JASkXkD5O2iLRdIOS4ivpkRSFw.vSeayrACGp3DiZvhWuflXQ"
}

story_background = "辛迪加大陆分为托雷省，尼莱省和穆拉省，其中生活着矮人，精灵，人类三个种族以及无数的怪物。你是一个来自托雷的人类男性魔法师，今年21岁。你左手持着火焰法杖，右手拿着魔法书，背包里装着能支撑一周的口粮，进入了莱肯斯雨林进行冒险。"


class ChatApplication:

    def __init__(self, story_teller, background):
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
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.87, rely=0.008, relheight=0.06, relwidth=0.12)
        self._init_background(self.background)

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
        self._insert_message(msg, "你")

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
