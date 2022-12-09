from revChatGPT.revChatGPT import Chatbot
from pychatgpt import OpenAI
import textwrap


def print_warp(instr):
    for i in textwrap.wrap(instr, width=50):
        print(i)


def login(config):
    expired_creds = OpenAI.token_expired()
    expired_creds = True

    if expired_creds:
        print_warp("access_token过期，请选择登陆(y)或者使用默认的session_token(n)。请输入(y/n):")
        _input = input()
        if _input == 'y':
            email = input("邮箱：")
            pwd = input("密码：")
            open_ai_auth = OpenAI.Auth(email_address=email, password=pwd)
            try:
                open_ai_auth.create_token()
            except:
                print_warp("登陆失败！请检查邮箱和密码。将使用默认session_token进入。")
                print("\n\n\n")
                return config
            else:
                access_token = OpenAI.get_access_token()
                config = {"Authorization": access_token[0]}
                print("\n\n\n")
                return config
        else:
            print("\n\n\n")
            return config
    else:
        access_token = OpenAI.get_access_token()
        config = {"Authorization": access_token[0]}
        return config



class StoryTeller():
    def __init__(self, config, story):
        self.chatbot = Chatbot(config, conversation_id=None)
        self.chatbot.reset_chat()  # Forgets conversation
        self.chatbot.refresh_session()  # Uses the session_token to get a new bearer token
        self.first_interact = True
        self.story = story

    def reset(self):
        self.chatbot.reset_chat()
        self.first_interact = True

    def action(self, user_action):
        if user_action[-1] != "。":
            user_action = user_action + "。"
        if self.first_interact:
            prompt = """现在来充当一个冒险文字游戏，描述时候注意节奏，不要太快，仔细描述各个人物的心情和周边环境。一次只需写四到六句话。
            开头是，""" + self.story + """ 你""" + user_action
            self.first_interact = False
        else:
            prompt = """继续，一次只需要续写四到六句话，总共就只讲5分钟内发生的事情。
            你""" + user_action
        resp = self.chatbot.get_chat_response(prompt)  # Sends a request to the API and returns the response by OpenAI
        self.response = resp["message"]

    def interactive(self):
        print_warp(self.story)
        while True:
            action = input("> 你")
            self.action(action)
            print_warp(self.response)
