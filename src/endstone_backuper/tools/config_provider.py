import os
import json

configuration_path = f"{os.getcwd()}/plugins/configuration/backuper/conf.json"

def GetConfiguration() -> dict:
    file_path = f"{configuration_path}"
    if not os.path.exists(file_path): raise Exception()
    with open(f"{configuration_path}", "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
        return data
    
def SaveConfiguration(data: dict):
    file_path = f"{configuration_path}"
    with open(file_path, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)
        jsonFile.close()