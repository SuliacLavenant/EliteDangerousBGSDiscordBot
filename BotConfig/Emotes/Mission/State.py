class State:
    active: str
    complete: str
    pending: str
    upcoming: str

    def __init__(self, emote_dict: dict):
        self.active = emote_dict["active"]
        self.complete = emote_dict["complete"]
        self.pending = emote_dict["pending"]
        self.upcoming = emote_dict["upcoming"]
