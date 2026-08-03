from dotenv import load_dotenv
import os

from DataStorageManager import DataStorageManager
from BotConfig.BotConfig import BotConfig

load_dotenv()
guild_ids_raw = os.getenv("DISCORD_GUILDS")
guild_ids = [int(guild_id) for guild_id in guild_ids_raw.split(",") if guild_id]

BotConfig.load()

#data format update
DataStorageManager.guild_settings_data_format_update(guild_ids)
DataStorageManager.system_data_format_update(guild_ids)
