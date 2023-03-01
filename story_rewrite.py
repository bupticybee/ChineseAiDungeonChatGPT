from config import config
# from app import ChatApplication
from utils import print_logo, print_warp, error, input_option
from colorama import Fore

PYCHATGPT_AVAILABLE = True
try:
    from revChatGPT.V1 import Chatbot
except:
    error("你没有安装revChatGPT，无法使用。\n\n\n")
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
            }
        """
        self.background = background
        self.type = None  # session token or openai account
        self.config = None
        self.chatbot = None
        self.first_interact = True

    def _login(self, _config):
        self.chatbot = Chatbot(_config)

    def config_by_token(self):
        """
        Config by session token
        """
        self.type = 0

        session_token = config["session_token"]
        print(session_token)
        _config = {"session_token": session_token}
        return _config

    def config_by_account(self):
        """
        Config by Openai account
        """
        _config = {
            "email": "",
            "password": "",
            # "conversation_id": "",
            # "parent_id": "",
            # "proxy": "",
            "paid": False
        }
        self.type = 1
        print("请输入OpenAI帐号的邮箱及密码。")
        _config["email"] = input("邮箱:")
        _config["password"] = input("密码:")
        prox = input("若使用代理，请输入代理url。不使用则直接回车。")
        if prox:
            _config["proxy"] = prox

        paid = input_option("你是否为付费用户？", 'y', 'n', 'n')
        if paid:
            _config["paid"] = True
        try:
            with open('id_log.txt', 'r') as f:
                lines = f.readlines()
                last_line = lines[-1]
                if last_line:
                    resume = input_option("发现之前的冒险。是否继续冒险:", 'y', 'n', 'y')
                    if resume:
                        self.first_interact = False
                        _config["parent_id"] = last_line
        except:
            pass

        return _config

    def setup_chatbot(self):
        self.config = self.get_config()
        self._login(self.config)

        if self.first_interact:
            print("请输入背景故事。置空则使用默认背景故事。")
            background = input()
            if background:
                self.background = background
        else:
            try:
                with open('chat_log.txt', 'r') as f:
                    lines = f.readlines()
                    last_line = lines[-1]
                    if last_line:
                        self.background = last_line
            except:
                self.background = ""
        print("\n\n\n")

    def get_config(self):
        # if PYCHATGPT_AVAILABLE:
        #     print("请选择使用方式：\n y:登陆使用。(需要OpenAI账号) \n n:不登陆使用。("
        #           "使用默认的session_token运行，可能无法运行)")
        #     res = input()
        #     if res == 'y':
        #         return self.config_by_account()
        #     else:
        #         return self.config_by_token()
        # else:
        #     self.type = 0
        #     return config
        return self.config_by_account()

    def start_cli(self):
        print_logo()
        self.setup_chatbot()
        self.interactive()

    # def start_app(self):
    #     app = ChatApplication(self.background)
    #     app.run()

    def save_conversation_id(self, conv_id):
        with open('id_log.txt', 'w') as f:
            f.writelines(conv_id)

    def save_conversations(self, res):
        with open('chat_log.txt', 'w') as f:
            f.writelines(res)

    def action(self, user_action):
        if user_action[-1] != "。":
            user_action = user_action + "。"
        if self.first_interact:
            prompt = """现在来充当一个冒险文字游戏，描述时候注意节奏，不要太快，仔细描述各个人物的心情和周边环境。一次只需写四到六句话。
            开头是，""" + self.background + """ 你""" + user_action
        else:
            prompt = """继续，一次只需要续写四到六句话，总共就只讲5分钟内发生的事情。
            你""" + user_action
        response = ""

        for data in self.chatbot.ask(
            prompt
        ):
            response = data["message"]

        self.save_conversations(response)

        if self.first_interact:
            self.first_interact = False
            self.save_conversation_id(self.chatbot.get_conversations()[0]['id'])

        return response

    def interactive(self):
        # os.system('clear')
        print_warp(self.background)
        while True:
            action = input(Fore.GREEN + "> 你")
            print_warp(self.action(action))
