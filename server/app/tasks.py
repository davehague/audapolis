# This holds the tasks state. TODO(@pajowu), check if we should store this on disk
import uuid
from dataclasses import dataclass, field


@dataclass
class Task:
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    def cancel(self):
        pass


class Tasks:
    def __init__(self):
        self.tasks = {}

    def add(self, task: Task):
        self.tasks[task.uuid] = task
        return task

    def get(self, uuid: str):
        try:
            return self.tasks[uuid]
        except KeyError:
            raise TaskNotFoundError()

    def list(self):
        return self.tasks.values()

    def delete(self, uuid: str):
        try:
            task = self.tasks[uuid]
            task.cancel()
            self.tasks.pop(uuid)
        except KeyError:
            raise TaskNotFoundError()
    
    def update(self, task: Task):
        """Update an existing task in the task list"""
        self.tasks[task.uuid] = task
        return task


class TaskNotFoundError(Exception):
    pass


tasks = Tasks()
