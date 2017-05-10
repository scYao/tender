#coding: utf-8
from datetime import timedelta
from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1:6379'               # 指定 Broker
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 指定 Backend

CELERY_TIMEZONE='Asia/Shanghai'                     # 指定时区，默认是 UTC

CELERY_IMPORTS = (                                  # 指定导入的任务模块
    'celery_app.task1',
    'celery_app.task2'
)

# schedules
CELERYBEAT_SCHEDULE = {
    # 'add-every-30-seconds': {
    #      'task': 'celery_app.task2.pushTemplateMessage',
    #      'schedule': timedelta(hours=12),       # 每 30 秒执行一次
    #      'args': ()                           # 任务函数参数
    # },
    # 'multiply-at-morning-time': {
    #     'task': 'celery_app.task2.pushTemplateMessage',
    #     'schedule': crontab(hour=9, minute=00),   # 每天早上 9 点执行一次
    #     'args': ()                                # 任务函数参数
    # },
    # 'multiply-at-afternoon-time': {
    #     'task': 'celery_app.task2.pushTemplateMessage',
    #     'schedule': crontab(hour=15, minute=04),  # 每天早上 17 点 执行一次
    #     'args': ()  # 任务函数参数
    # }
}