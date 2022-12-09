from story import StoryTeller, login
from config import config

story_background = "你在树林里冒险，指不定会从哪里蹦出来一些奇怪的东西，你握紧手上的手枪，希望这次冒险能够找到一些值钱的东西，你往树林深处走去。"

if __name__ == "__main__":
    try:
        config = login(config)
    finally:
        story_teller = StoryTeller(config, story_background)
        story_teller.interactive()
