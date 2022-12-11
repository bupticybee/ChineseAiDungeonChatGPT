from revChatGPT.revChatGPT import Chatbot
from config import config
from app import ChatApplication
from utils import print_logo, print_warp, error, input_option
from colorama import Fore

PYCHATGPT_AVAILABLE = True

try:
    from pychatgpt import Chat, Options, OpenAI
except:
    error("你的Python版本低于3.9或没有安装pychatgpt，无法使用登陆功能，将使用默认token。\n\n\n")
    PYCHATGPT_AVAILABLE = False


class StoryTeller:
    def __init__(self, background):
        """
        Setup chatbot based on type and config.
        Config has different format base on type.
        if type = 0:
            config = {
                "session_token": str,
            }
        if type = 1:
            config = {
                "email": str,
                "password": str,
                "options": {
                    "log": bool,
                    "track": bool,
                    "proxies": str,
                    # optional, pass a file path to save the conversation
                    "chat_log": str,
                    "id_log": str
                },
                "previous_convo_id": str # resume a conversation
            }
        """
        self.background = background
        self.type = None  # 0: revChatGPT 1: PyChatGPT
        self.config = None
        self.chatbot = None
        self.first_interact = True

    def login_by_token(self):
        self.chatbot = Chatbot(self.config, conversation_id=None)
        self.chatbot.reset_chat()  # Forgets conversation
        self.chatbot.refresh_session()  # Uses the session_token to get a new bearer token

    def login_by_account(self):
        previous_convo_id = None
        options = Options()
        options.log = self.config['options']['log']
        options.track = self.config['options']['track']
        if 'proxies' in self.config['options'].keys():
            options.proxies = self.config['options']['proxies']
        if 'previous_convo_id' in self.config['options'].keys():
            previous_convo_id = self.config['options']['previous_convo_id']
        self.chatbot = Chat(email=self.config['email'], password=self.config['password'], options=options,
                            previous_convo_id=previous_convo_id)

    def config_by_token(self):
        self.type = 0
        expired_creds = OpenAI.token_expired()
        expired_creds = True

        if expired_creds:
            print("access_token过期，请选择登陆(y)或者使用默认的session_token(n)。请输入(y/n):")
            _input = input()
            if _input == 'y':
                email = input("邮箱：")
                pwd = input("密码：")
                open_ai_auth = OpenAI.Auth(email_address=email, password=pwd)
                try:
                    open_ai_auth.create_token()
                except:
                    print("登陆失败！请检查邮箱和密码。将使用默认session_token进入。")
                    return config
                else:
                    access_token = OpenAI.get_access_token()
                    _config = {"Authorization": access_token[0]}
                    return _config
            else:
                return config
        else:
            access_token = OpenAI.get_access_token()
            _config = {"Authorization": access_token[0]}
            return _config

    def config_by_account(self):
        _config = {
            "email": "",
            "password": "",
            "options": {
                "log": True,
                "track": True,
                # optional, pass a file path to save the conversation
                # "chat_log": None,
                # "id_log": None
            },
            "previous_convo_id": str  # resume a conversation
        }
        self.type = 1
        print("请输入邮箱密码。")
        _config["email"] = input("邮箱:")
        _config["password"] = input("密码:")
        _config["options"]["log"] = input_option("是否开启log:", 'y', 'n', 'y')
        _config["options"]["track"] = input_option("是否进行对话追踪:", 'y', 'n', 'y')
        prox = input("若使用代理，请输入代理url。不使用则直接回车。")
        if prox:
            _config["options"]["proxies"] = prox
        return _config

    def setup_chatbot(self):
        self.config = self.get_config()
        if self.type:
            self.login_by_account()
        else:
            self.login_by_token()

        print("请输入背景故事。置空则使用默认背景故事。")
        background = input()
        if background:
            self.background = background
        print("\n\n\n")

    def get_config(self):
        if PYCHATGPT_AVAILABLE:
            print(
                "请选择使用方式：\n y:登陆使用。(需要OpenAI账号。能够使用代理，继续故事等功能) \n n:不登陆使用。(使用之前获取的access_token或者默认的session_token运行)")
            res = input()
            if res == 'y':
                return self.config_by_account()
            else:
                return self.config_by_token()
        else:
            self.type = 0
            return config

    def start_cli(self):
        print_logo()
        self.setup_chatbot()
        self.interactive()

    def start_app(self):
        app = ChatApplication(self.background)
        app.run()

    def action(self, user_action):
        if user_action[-1] != "。":
            user_action = user_action + "。"
        if self.first_interact:
            prompt = """现在来充当一个冒险文字游戏，描述时候注意节奏，不要太快，仔细描述各个人物的心情和周边环境。一次只需写四到六句话。
            开头是，""" + self.background + """ 你""" + user_action
            self.first_interact = False
        else:
            prompt = """继续，一次只需要续写四到六句话，总共就只讲5分钟内发生的事情。
            你""" + user_action
        if self.type:
            response, _, _ = self.chatbot.ask(prompt)
        else:
            resp = self.chatbot.get_chat_response(prompt)  # Sends a request to the API and returns the response by
            # OpenAI
            response = resp["message"]
        return response

    def interactive(self):
        # os.system('clear')
        print_warp(self.background)
        while True:
            action = input(Fore.GREEN + "> 你")
            self.action(action)
            print_warp(self.action(action))
