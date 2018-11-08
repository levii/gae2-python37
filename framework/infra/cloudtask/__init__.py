from google.cloud import tasks_v2beta3

from framework.domain.entity.task import Task


def enqueue(task: Task, queue: str, project: str, location: str):
    client = tasks_v2beta3.CloudTasksClient()
    parent = client.queue_path(project, location, queue)
    task_dict = {
        'app_engine_http_request': {
            'http_method': task.method,
            'relative_uri': task.url
        }
    }

    if task.payload is not None:
        task_dict['app_engine_http_request']['body'] = task.payload_as_bytes()

    if task.schedule_time is not None:
        task_dict['schedule_time'] = task.schedule_time_as_pb()

    return client.create_task(parent, task_dict)
