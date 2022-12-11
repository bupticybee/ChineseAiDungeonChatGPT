from story_rewrite import StoryTeller

story_background = "你在树林里冒险，指不定会从哪里蹦出来一些奇怪的东西，你握紧手上的手枪，希望这次冒险能够找到一些值钱的东西，你往树林深处走去。"

if __name__ == "__main__":
    chatter = StoryTeller(story_background)
    chatter.start_cli()
