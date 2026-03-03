from dataclasses import dataclass, field

@dataclass
class GuildSettings:
    minor_faction_name: str = None

    #channels
    bgs_change_log_channel_id: int = None
    bgs_system_recap_channel_id: int = None
    bgs_warning_recap_channel_id: int = None
    mission_recap_channel_id: int = None
    trusted_channel_ids: list = field(default_factory=list)


    @classmethod
    def init_from_dict(cls, guild_settings_dict: dict):
        guild_settings = cls(
            minor_faction_name=guild_settings_dict["minor_faction_name"],
            bgs_change_log_channel_id=guild_settings_dict["bgs_change_log_channel_id"],
            bgs_system_recap_channel_id=guild_settings_dict["bgs_system_recap_channel_id"],
            bgs_warning_recap_channel_id=guild_settings_dict["bgs_warning_recap_channel_id"],
            mission_recap_channel_id=guild_settings_dict["mission_recap_channel_id"],
            trusted_channel_ids=guild_settings_dict["trusted_channel_ids"]
            )
        return guild_settings


    def get_as_dict(self) -> dict:
        guild_settings_dict = {}
        guild_settings_dict["minor_faction_name"] = self.minor_faction_name
        guild_settings_dict["bgs_change_log_channel_id"] = self.bgs_change_log_channel_id
        guild_settings_dict["bgs_system_recap_channel_id"] = self.bgs_system_recap_channel_id
        guild_settings_dict["bgs_warning_recap_channel_id"] = self.bgs_warning_recap_channel_id
        guild_settings_dict["mission_recap_channel_id"] = self.mission_recap_channel_id
        guild_settings_dict["trusted_channel_ids"] = self.trusted_channel_ids
        return guild_settings_dict


    ######## Trusted channels
    def is_channel_trusted(self, channel_id: int):
        return channel_id in self.trusted_channel_ids


    def add_trusted_channel(self, channel_id: int):
        if channel_id not in self.trusted_channel_ids:
            self.trusted_channel_ids.append(channel_id)
            return True
        else:
            return False


    def remove_trusted_channel(self, channel_id: int):
        if channel_id in self.trusted_channel_ids:
            self.trusted_channel_ids.remove(channel_id)
            return True
        else:
            return False
