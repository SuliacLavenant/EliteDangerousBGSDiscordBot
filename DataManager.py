import os
import json

from DataClass.MinorFaction import MinorFaction
from DataClass.System import System

#TODO refaire proprement avec des catch
class DataManager:

    #create storage file for the discord
    def createDataFile(guild_id: str):
        filePath = f"data/{guild_id}.json"

        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        if not os.path.exists(filePath):
            with open(filePath, "w", encoding="utf-8") as f:
                f.write("{}")
        else:
            print("Data file already exist")
    

    #reset the data file content
    def resetDataFile(guild_id: str):
        filePath = f"data/{guild_id}.json"

        if not os.path.exists(filePath):
            with open(filePath, "w", encoding="utf-8") as f:
                f.write("{}")
        else:
            print("Data file do not exist")


    #set minor faction to the data file
    def setMinorFactionToDataFile(guild_id: str, minorFaction: MinorFaction):
        filePath = f"data/{guild_id}.json"

        #read actual content
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {type(e).__name__}")
            data = {}

        #data update
        data["name"] = minorFaction.name
        data["allegiance"] = minorFaction.allegiance
        data["government"] = minorFaction.government
        data["systems"] = {}

        #atomic write
        with open(filePath+".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(filePath+".tmp", filePath)

        return True


    def addSystemToDataFile(guild_id: str, system: System):
        filePath = f"data/{guild_id}.json"

        #read actual content
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {type(e).__name__}")
            data = {}

        #data update
        data["systems"][system.name] = {}
        data["systems"][system.name]["name"] = system.name
        data["systems"][system.name]["population"] = system.population
        data["systems"][system.name]["security"] = system.security
        data["systems"][system.name]["economy"] = system.economy
        data["systems"][system.name]["secondEconomy"] = system.secondEconomy
        data["systems"][system.name]["reserve"] = system.reserve


        data["systems"][system.name]["controllingFaction"] = system.controllingFaction
        data["systems"][system.name]["factions"] = system.factions

        #atomic write
        with open(filePath+".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(filePath+".tmp", filePath)

        return True
