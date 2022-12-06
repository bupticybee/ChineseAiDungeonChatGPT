# 中文版本的ai地牢的简易tkinter客户端


<img width="470" alt="Img" src="https://user-images.githubusercontent.com/43384183/205905781-f47d82b3-35c2-41f6-8db3-edb7be3c8fa7.png">

## 介绍

中文版的ai地牢，直接使用的openai的ChatGPT api作为讲故事的模型。原项目地址为[ChineseAiDungeon](https://github.com/bupticybee/ChineseAiDungeonChatGPT)。  
此项目用tkinter做了一个简单的交互客户端，包含token检查，登陆，自定义初始故事功能。更多功能正在开发中。token检查和登陆功能使用了[PyChatGPT](https://github.com/rawandahmad698/PyChatGPT)项目的部份代码。


## 安装和使用

拉取项目，然后在项目目录下运行
```shell
pip3 install -r requirements.txt
```
安装所有依赖

然后直接
```shell
python3 example_story.py
```

就可以在命令行运行起来

你也可以通过

```shell
python3 app.py
```

调出一个tkinter的客户端运行。

![](outputs/example_chatgpt_app.png)


## 常见问题

1. err TypeError: 'generator' object is not subscriptable

见 [#1](https://github.com/bupticybee/ChineseAiDungeonChatGPT/issues/1) ，尝试`pip3 install revChatGPT --upgrade`升级依赖

2. response = response.text.splitlines()[-4]  IndexError: list index out of rang

一般是接口太多人调用挂了，等openai修复就好
