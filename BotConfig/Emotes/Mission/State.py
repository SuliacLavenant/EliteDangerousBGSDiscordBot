class State:
    active: str
    complete: str
    failed: str
    pending: str
    state: str
    upcoming: str

    def __init__(self, emote_dict: dict):
        self.active = emote_dict["active"]
        self.complete = emote_dict["complete"]
        self.failed = emote_dict["failed"]
        self.pending = emote_dict["pending"]
        self.state = emote_dict["state"]
        self.upcoming = emote_dict["upcoming"]
