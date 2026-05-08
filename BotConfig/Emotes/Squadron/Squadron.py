from BotConfig.Emotes.Squadron.Members import Members

class Squadron:
    members: Members

    def __init__(self, emote_dict: dict):
        self.members = Members(emote_dict["members"])
