# Project description

# API Used
- [EDSM](https://www.edsm.net/)
- [Elite BGS](https://elitebgs.app/ebgs/)

# Requierement
Python extra packages:
- discord.py
- dotenv
- python-dotenv
- requests

Create a .env file with:
- DISCORD_TOKEN=DISCORDAPPTOKEN
- DISCORD_GUILD=IDOFYOURDISCORDSERVER


# Data 

Faction:
- name: str
- allegiance: str
- government: str
- population: int
- systems: dict{System}

System:
- name: str
- controllingFaction: str
- factions: dict{name, allegiance}

FactionInSystem:
- name: str
- allegiance: str
- government: str
- influence: int
- state: str
