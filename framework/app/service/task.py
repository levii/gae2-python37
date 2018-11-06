import os

from framework.domain.entity.task import Task
from framework.infra.cloudtask import enqueue


class TaskEnqueueService:
    def __init__(
            self,
            task: Task,
            queue: str,
            project: str = None,
            location: str = None
    ):
        self._task = task
        self._queue = queue
        self._project = project if project else os.environ.get(
            'GOOGLE_CLOUD_PROJECT')
        self._location = location

    def execute(self):
        return enqueue(
            task=self._task,
            queue=self._queue,
            project=self._project,
            location=self._location
        )
