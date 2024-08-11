# Backuper
A Plugin plugin in Python for Endstone

## Usage
create folder in dir /plugins/configuration/backuper


than in this folder create file conf.json
this file should have this fields

```json
{
    "world_folder_name": "Bedrock level", //name of world folder
    "backups_count": 0, //specifies max count of backups that this plugin will store
    "delay": 0, //specifies delay before first backup on start
    "period": 0 //specifies delay between backups
}
```

note all time intervals are in minecraft ticks 1 second = 20 ticks

note that plugin create backups on server shutdown