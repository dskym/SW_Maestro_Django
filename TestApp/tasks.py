from __future__ import absolute_import
from TestServer.celery import app


@app.task
def hello():
    return 'hello world'
