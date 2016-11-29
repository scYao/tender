# coding=utf8
from tornado.options import define, options
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from datetime import datetime

from index import app

def tick():
    print('Tick! The time is: %s' % datetime.now())


if __name__ == '__main__':

    args = options.parse_command_line()
    if len(args) == 0:
        port = 5006
    else:
        port = args[0]

    http_server = HTTPServer(WSGIContainer(app), xheaders=True)

    http_server.listen(port)
    IOLoop.instance().start()
