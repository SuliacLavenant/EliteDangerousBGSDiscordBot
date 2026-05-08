class Members:
    leader: str
    officer: str
    member: str
    recruit: str

    def __init__(self, emote_dict: dict):
        self.leader = emote_dict["leader"]
        self.officer = emote_dict["officer"]
        self.member = emote_dict["member"]
        self.recruit = emote_dict["recruit"]
