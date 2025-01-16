# Backuper
A Plugin plugin in Python for Endstone

## Usage
create folder in dir /plugins/configuration/backuper


than in this folder create file conf.json
this file should have this fields

```json
{
    "world_folder_name": "Bedrock level", //name of the folder of the world to backup
    "types": {
        "profile": { //name of backup profile
            "time_between": 60, //time in seconds
            "max_count": 1 //max count of backups for this backup profile
        }
    },
    "saved_tasks": {} //here will be stored timings of backups tasks
}
```

note that plugin create backups on server shutdown in folder of the first backup profile