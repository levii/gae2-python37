# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from datetime import datetime

from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger import swag_from
from flasgger import validate

from framework.app.service.task import TaskEnqueueService
from framework.domain.entity.task import Task

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
swagger = Swagger(app)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/colors/<palette>/')
@swag_from('colors.yml')
def colors(palette):
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = 1  #all_colors
    else:
        result = {palette: all_colors.get(palette)}

    # Response Schema のチェック
    validate(result, 'Palette', 'colors.yml')
    return jsonify(result)


class HelloTask(Task):
    URL = '/task/handle'

    def __init__(
            self,
            message: str,
            schedule_time: datetime = None,
            in_seconds: int = None
    ):
        payload = {'message': message}

        super(HelloTask, self).__init__(
            payload=payload,
            schedule_time=schedule_time,
            in_seconds=in_seconds
        )

    @property
    def message(self):
        return self.payload['message']


@app.route('/task/add')
def task():
    t = HelloTask(
        message='hello',
        in_seconds=60
    )

    queue = 'test-queue'
    # 本来なら project と location は自動取得できるはず
    project = 'levii-python37-test'
    location = 'asia-northeast1'

    response = TaskEnqueueService(
        task=t, queue=queue, project=project, location=location
    ).execute()

    print('Created task {}'.format(response.name))
    return 'ok'


@app.route('/task/handle', methods=['POST'])
def task_handler():
    """Log the request payload."""
    t = HelloTask.load(request.get_data(as_text=True))
    print('Received task with payload: {}'.format(t.message))
    return 'Printed task payload: {}'.format(t.message)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
