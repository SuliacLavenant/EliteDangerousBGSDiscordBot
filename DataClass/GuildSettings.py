from dataclasses import dataclass, field

@dataclass
class GuildSettings:
    bgs_change_log_channel_id: int = None
    bgs_system_recap_channel_id: int = None
    bgs_warning_recap_channel_id: int = None

    minor_faction_name: str = None

    #init from Dict
    @classmethod
    def init_from_dict(cls, guild_settings_dict: dict):
        guild_settings = cls(
            bgs_change_log_channel_id=guild_settings_dict["bgs_change_log_channel_id"],
            bgs_system_recap_channel_id=guild_settings_dict["bgs_system_recap_channel_id"],
            bgs_warning_recap_channel_id=guild_settings_dict["bgs_warning_recap_channel_id"],
            minor_faction_name=guild_settings_dict["minor_faction_name"]
            )
        return guild_settings

    def get_as_dict(self) -> dict:
        guild_settings_dict = {}
        guild_settings_dict["bgs_change_log_channel_id"] = self.bgs_change_log_channel_id
        guild_settings_dict["bgs_system_recap_channel_id"] = self.bgs_system_recap_channel_id
        guild_settings_dict["bgs_warning_recap_channel_id"] = self.bgs_warning_recap_channel_id
        guild_settings_dict["minor_faction_name"] = self.minor_faction_name

        return guild_settings_dict
