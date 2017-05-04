#coding: utf-8
import task1
from datetime import datetime
from celery_app import app
from tool.Util import Util


#定时推送
@app.task
def pushTemplateMessage():
    task1.pushTemplateMessage.apply_async(args=[])





