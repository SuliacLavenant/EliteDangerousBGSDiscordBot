# Project description

# API Used
- [EDSM](https://www.edsm.net/)
- [Elite BGS](https://elitebgs.app/ebgs/)

# Requierement
Python extra packages:
- py-cord
- dotenv
- python-dotenv
- requests

Create a .env file with:
- DISCORD_TOKEN=DISCORDAPPTOKEN
- DISCORD_GUILDS=IDOFYOURDISCORDSERVER,...
- SUPER_ADMIN=IDOFUSER
- CONTACT_EMAIL=EMAIL
- DB_USER=
- DB_PW=
- DB_PORT=
- DB_NAME=


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


---------
# PostgreSQL
5432
pip install "psycopg[binary]"
pip install sqlalchemy "psycopg[binary]"

