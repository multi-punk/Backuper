import os
import time
import shutil
from datetime import datetime, timedelta
from endstone.plugin import Plugin
from endstone_backuper.listener import Listener
import endstone_backuper.tools.config_provider as conf
from endstone_backuper.tools.tasks import check_tasks, tasks, Task

class BackuperPlugin(Plugin):
    version = "0.1.0"
    api_version = "0.5"

    def on_load(self) -> None:
        self.logger.info("Backuper plugin is loading")

    def on_enable(self) -> None:
        self.logger.info("Backuper plugin is enabled")

        self.register_events(self)
        self._listener = Listener(self)
        self.register_events(self._listener)

        self.configuration = conf.GetConfiguration()

        self.restore_tasks()

        self.server.scheduler.run_task(self, check_tasks, 0, 20)

    def on_disable(self) -> None:
        self.save_tasks()
        types = self.configuration["types"]
        self.backup(list(types.keys())[0])

    def schedule_backup(self, backup_type, delay):
        task_id = f"backup_{backup_type}"
        tasks[task_id] = Task(delay, self.backup, args=(backup_type,))

    def restore_tasks(self):
        now = datetime.now().timestamp()
        saved_tasks = self.configuration.get("saved_tasks", {})

        for task_id, task_data in saved_tasks.items():
            delay = max(0, task_data["run_at"] - now)
            backup_type = task_data["backup_type"]
            self.schedule_backup(backup_type, delay)

        for backup_type, config in self.configuration["types"].items():
            task_id = f"backup_{backup_type}"
            if task_id not in tasks:
                delay = config.get("time_between", 3600)
                self.schedule_backup(backup_type, delay)


    def save_tasks(self):
        now = datetime.now().timestamp()
        saved_tasks = {}

        for task_id, task in tasks.items():
            backup_type = task.args[0] if task.args else None
            saved_tasks[task_id] = {
                "run_at": now + task.delay,
                "backup_type": backup_type
            }

        self.configuration["saved_tasks"] = saved_tasks
        conf.SaveConfiguration(self.configuration)

    def backup(self, backup_type):
        config = self.configuration["types"].get(backup_type, {})
        backup_folder = f"{os.getcwd()}/backups/{backup_type}/"
        world_folder = f"{os.getcwd()}/worlds/{self.configuration["world_folder_name"]}/"
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S (%A)")
        backup_path = os.path.join(backup_folder, timestamp)

        os.makedirs(backup_folder, exist_ok=True)
        shutil.copytree(world_folder, backup_path)

        self.clean_old_backups(backup_folder, config.get("max_count", 1))

        self.logger.info(f"{backup_type.capitalize()} backup created at {backup_path}")

        task_id = f"backup_{backup_type}"
        tasks[task_id] = Task(config.get("time_between", 3600), self.backup, args=(backup_type,))
        self.logger.info(f"Scheduling next backup for {backup_type} in {config.get('time_between', 3600)} seconds")

    def clean_old_backups(self, folder, max_backups):
        backups = sorted([
            os.path.join(folder, d) for d in os.listdir(folder)
            if os.path.isdir(os.path.join(folder, d))
        ])

        while len(backups) > max_backups:
            oldest = backups.pop(0)
            shutil.rmtree(oldest)
            self.logger.info(f"Deleted old backup: {oldest}")