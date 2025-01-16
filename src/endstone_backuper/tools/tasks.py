class Task:
    delay: int
    task: any
    args: tuple
    kwargs: dict

    def __init__(self, delay: int, task: any, args: tuple = None, kwargs: dict = None):
        self.delay = delay
        self.task = task
        self.args = args if args is not None else ()
        self.kwargs = kwargs if kwargs is not None else {}

tasks: dict[str, Task] = {}

def check_tasks():
    for task_id in list(tasks.keys()):
        task = tasks[task_id]
        if task.delay == 0:
            if task.args or task.kwargs:
                task.task(*task.args, **task.kwargs)
            else:
                task.task()
        else:
            task.delay -= 1