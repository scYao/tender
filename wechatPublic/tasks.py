#coding:utf-8
import time
from celery import Celery

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'

app = Celery('my_task', broker=broker, backend=backend)

@app.task
def add(x, y):
    time.sleep(10)     # 模拟耗时操作
    return x + y

