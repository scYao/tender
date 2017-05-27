# coding=utf8
from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.options import define, options
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from stoken.StsTokenManager import StsTokenManager
from celery_app import task2

from datetime import datetime

from index import app

def tick():
    print('Tick! The time is: %s' % datetime.now())


def interval_event():
    stsTokenManager = StsTokenManager()
    scheduler = TornadoScheduler()
    scheduler.add_job(stsTokenManager.createStsToken, 'interval', seconds=3000)
    # scheduler.add_job(task2.pushTemplateMessage, 'cron', second=0, minute=30, hour=9)
    # scheduler.add_job(task2.pushTemplateMessage, 'cron', second=0, minute=30, hour=11)
    # scheduler.add_job(task2.pushTemplateMessage, 'cron', second=0, minute=30, hour=13)
    # scheduler.add_job(task2.pushTemplateMessage, 'cron', second=0, minute=30, hour=17)
    scheduler.start()


if __name__ == '__main__':

    args = options.parse_command_line()
    if len(args) == 0:
        port = 5007
    else:
        port = args[0]

    interval_event()

    http_server = HTTPServer(WSGIContainer(app), xheaders=True)

    http_server.listen(port)
    IOLoop.instance().start()
