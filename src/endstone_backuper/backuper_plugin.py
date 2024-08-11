import json
import os
import time
import shutil
from endstone.plugin import Plugin
from endstone_backuper.listener import Listener
import endstone_backuper.tools.config_provider as conf


class BackuperPlugin(Plugin):
    version = "0.1.0"
    api_version = "0.5"

    def on_load(self) -> None:
        self.logger.info("Hub plugin is loading")

    def on_enable(self) -> None:
        self.logger.info("Hub plugin is load")

        self.register_events(self)
        self._listener = Listener(self)
        self.register_events(self._listener)

        configuration = conf.GetConfiguration()

        self.server.scheduler.run_task(
            self, 
            self.backup, 
            delay=configuration["delay"], 
            period=configuration["period"]
        )

    def on_disable(self) -> None:
        self.backup()

    def backup(self):
        configuration = conf.GetConfiguration()
        backups_folder = f"{os.getcwd()}/backups/"

        folder_name = f"{round(time.time() * 1000)}"

        source_folder = f"{os.getcwd()}/worlds/{configuration["world_folder_name"]}/"
        folder_path = f"{backups_folder}{folder_name}"

        files = os.listdir(source_folder)
        shutil.copytree(source_folder, folder_path)

        folders_count = 0

        for path in os.scandir(backups_folder):
            if path.is_dir():
                folders_count += 1

        backups_count = configuration["backups_count"];

        if folders_count > backups_count:
            backup_index = 0
            for path in os.scandir(backups_folder):
                if backup_index + 1 <= folders_count - backups_count:
                    shutil.rmtree(path.path)
                if path.is_dir:
                    backup_index += 1

        self.logger.info("world have been backup")
