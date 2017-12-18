# coding=utf8


from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import time
monkey.patch_all()

from index import app


if __name__ == "__main__":
  #app.run(debug = True,host="0.0.0.0",port=5000 )
  http_server = WSGIServer(('0.0.0.0',5018), app, handler_class=WebSocketHandler)
  http_server.serve_forever()