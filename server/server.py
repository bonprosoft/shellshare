#-*- coding: utf-8 -*-
from stream_manager import *
import json
import tornado.ioloop
import tornado.web
from tornado import websocket

class SocketHandler(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        manager = kwargs.pop("manager", StreamManager())
        websocket.WebSocketHandler.__init__(self, *args, **kwargs)
        self.__manager = manager

    def check_origin(self, origin):
        return True
        ## 必要ならばドメインをチェックしてください
        #parsed_origin = urllib.parse.urlparse(origin)
        #return parsed_origin.netloc.endswith(".example.com")

    def open(self):
        # 何もしない？
        pass

    def on_close(self):
        # もし役職があれば通知
        self.__manager.logout_broadcaster(self)
        self.__manager.logout_listener(self)

    def on_message(self, message):
        try:
            obj = json.loads(message)
            if (obj["type"] == MessageType.BroadcasterLoginRequest):
                data = obj["data"]
                name = data["name"]
                token = data["token"]
                secret = data["secret"]
                self.__manager.login_broadcaster(self, name, token, secret)
            elif (obj["type"] == MessageType.ListenerLoginRequest):
                data = obj["data"]
                token = data["token"]
                self.__manager.login_listener(self, token)
            elif (obj["type"] == MessageType.UpdateContentRequest):
                self.__manager.update_content(self, obj["data"])
            elif (obj["type"] == MessageType.UpdateContentTypeRequest):
                self.__manager.update_content_type(self, obj["data"])
            elif (obj["type"] == MessageType.ListBroadcasterRequest):
                self.__manager.request_broadcaster_list(self)
            elif (obj["type"] == MessageType.FetchBufferRequest):
                data = obj["data"]
                target = data["target"]
                self.__manager.request_buffer(self, target)
            else:
                pass
        except Exception as e:
            print e

if __name__ == "__main__":
    manager = StreamManager()
    app = tornado.web.Application([
        (r"/", SocketHandler, {'manager': manager})
        ])
    app.listen(4567)
    print "Server is now working."

    tornado.ioloop.IOLoop.instance().start()

