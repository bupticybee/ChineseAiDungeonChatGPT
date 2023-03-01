from colorama import Fore, Back, Style
import textwrap


def print_warp(instr):
    for i in textwrap.wrap(instr, width=50):
        print(Style.BRIGHT + i)


def error(msg):
    print(Style.BRIGHT + Fore.RED + msg)
    print(Style.RESET_ALL)


def input_option(prompt, true_option, false_option, default_option):
    res = input(prompt + f"({true_option}/{false_option}, default {default_option})")
    if res == true_option:
        return True
    elif res == false_option:
        return False
    else:
        if default_option == true_option:
            return True
        else:
            return False


def print_logo():
    print(Fore.GREEN + """
        ▄████▄   ██░ ██  ██▓ ███▄    █ ▓█████   ██████ ▓█████      
       ▒██▀ ▀█  ▓██░ ██▒▓██▒ ██ ▀█   █ ▓█   ▀ ▒██    ▒ ▓█   ▀      
       ▒▓█    ▄ ▒██▀▀██░▒██▒▓██  ▀█ ██▒▒███   ░ ▓██▄   ▒███        
       ▒▓▓▄ ▄██▒░▓█ ░██ ░██░▓██▒  ▐▌██▒▒▓█  ▄   ▒   ██▒▒▓█  ▄      
       ▒ ▓███▀ ░░▓█▒░██▓░██░▒██░   ▓██░░▒████▒▒██████▒▒░▒████▒     
       ░ ░▒ ▒  ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░░░ ▒░ ░     
         ░  ▒    ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░ ░ ░  ░░ ░▒  ░ ░ ░ ░  ░     
       ░         ░  ░░ ░ ▒ ░ ▄▄▄   ░ ░ ██▓░   ░  ░  ░     ░        
       ░ ░       ░  ░  ░ ░  ▒████▄   ░▓██▒░  ░      ░     ░  ░     
       ░                    ▒██  ▀█▄  ▒██▒                         
                            ░██▄▄▄▄██ ░██░                         
                             ▓█   ▓██▒░██░                         
                             ▒▒   ▓▒█░░▓                           
                              ▒   ▒▒ ░ ▒ ░                         
                              ░   ▒    ▒ ░                         
    ▓█████▄  █    ██  ███▄    █   ▄████░▓█████  ▒█████   ███▄    █ 
    ▒██▀ ██▌ ██  ▓██▒ ██ ▀█   █  ██▒ ▀█▒▓█   ▀ ▒██▒  ██▒ ██ ▀█   █ 
    ░██   █▌▓██  ▒██░▓██  ▀█ ██▒▒██░▄▄▄░▒███   ▒██░  ██▒▓██  ▀█ ██▒
    ░▓█▄   ▌▓▓█  ░██░▓██▒  ▐▌██▒░▓█  ██▓▒▓█  ▄ ▒██   ██░▓██▒  ▐▌██▒
    ░▒████▓ ▒▒█████▓ ▒██░   ▓██░░▒▓███▀▒░▒████▒░ ████▓▒░▒██░   ▓██░
     ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ░▒   ▒ ░░ ▒░ ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
     ░ ▒  ▒ ░░▒░ ░ ░ ░ ░░   ░ ▒░  ░   ░  ░ ░  ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
     ░ ░  ░  ░░░ ░ ░    ░   ░ ░ ░ ░   ░    ░   ░ ░ ░ ▒     ░   ░ ░ 
       ░       ░              ░       ░    ░  ░    ░ ░           ░ 
    """)
    print(Style.BRIGHT + "           欢迎使用中文AI地牢，一个基于ChatGPT的中文文字冒险游戏")
    print(Style.RESET_ALL)
