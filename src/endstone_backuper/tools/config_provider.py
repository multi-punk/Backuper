import os
import json

configuration_path = f"{os.getcwd()}/plugins/configuration/backuper/conf.json"

def GetConfiguration():
    file_path = f"{configuration_path}"
    if not os.path.exists(file_path): raise Exception()
    with open(f"{configuration_path}", "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
        return data