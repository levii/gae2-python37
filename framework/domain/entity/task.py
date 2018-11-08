from datetime import datetime, timedelta
import json

from google.protobuf import timestamp_pb2


class Task:
    URL = None
    METHOD = 'POST'

    def __init__(
            self,
            payload: dict,
            schedule_time: datetime = None,
            in_seconds: int = None
    ):
        self._payload = payload

        if schedule_time is not None and in_seconds is not None:
            m = 'schedule_time and in_seconds should be specified exclusively.'
            raise ValueError(m)

        if schedule_time:
            self._schedule_time = schedule_time

        if in_seconds:
            td = timedelta(seconds=in_seconds)
            self._schedule_time = datetime.utcnow() + td

    @property
    def url(self)->str:
        return self.URL

    @property
    def method(self):
        return self.METHOD

    @property
    def payload(self):
        return self._payload

    @property
    def schedule_time(self):
        return self._schedule_time

    def payload_as_bytes(self)->bytes:
        return json.dumps(self._payload, ensure_ascii=False).encode('utf-8')

    def schedule_time_as_pb(self)->timestamp_pb2.Timestamp:
        timestamp = timestamp_pb2.Timestamp()
        return timestamp.FromDatetime(self._schedule_time)

    @classmethod
    def load(cls, body: bytes=None):
        payload = json.loads(body.decode('utf-8')) if body else None
        return cls(payload=payload)
