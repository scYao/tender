# coding=utf8

import json

import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.escape
from tornado import gen


class MainHandler(tornado.web.RequestHandler):

    def doSomething(self):
        a = 0
        for i in xrange(0, 1000000000):
            a = a + 1

    @gen.coroutine
    def sleep(self):
        yield gen.sleep(10)
        raise gen.Return([1, 2, 3, 4, 5])

    def get(self):
        self.write("Hello, world")

    @tornado.web.asynchronous
    def post(self):
        result = {}

        result['status'] = 'SUCCESS'
        result['data'] = 'hello'
        self.doSomething()
        self.write(json.dumps(result))

class AsycHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://friendfeed-api.com/v2/feed/bret",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries "
                   "from the FriendFeed API")
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/asychander", AsycHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()