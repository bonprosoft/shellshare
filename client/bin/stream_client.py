#-*- coding: utf-8 -*-

import json
from ws4py.client.threadedclient import WebSocketClient
from enums import *

KEY = "BROADCASTERKEY_HERE"
SECRET = "BROADCASTERSECRET_HERE"
MAX = 5

class StreamClient(WebSocketClient):
    def __init__(self, *args, **kwargs):
        username = kwargs.pop("name", "Anonymous")
        WebSocketClient.__init__(self, *args, **kwargs)
        self.__is_logined = False
        self.__username = username
        self.__login_count = 0

    def opened(self):
        self.send_login()

    def send_login(self):
        temp = {"type": MessageType.BroadcasterLoginRequest, "data": {"name": self.__username, "token": KEY, "secret": SECRET}}
        s = json.dumps(temp)
        self.send(s)

    def notify_language(self):
        if not self.__is_logined:
            return

        temp = {"type": MessageType.UpdateContentTypeRequest, "data": {"content_type": ContentType.Shell}}
        s = json.dumps(temp)
        self.send(s)

    def notify_update(self, text):
        if not self.__is_logined:
            return

        temp = {"type": MessageType.UpdateContentRequest, "data": {"type": UpdateContentType.Append, "text": text, "pos": -1}}
        s = json.dumps(temp)
        self.send(s)

    def closed(self, code, reason=None):
        self.__is_logined = False
        # 再接続する？

    def received_message(self, m):
        try:
            obj = json.loads(m.data)
            if (obj["type"] == MessageType.BroadcasterLoginFailed):
                self.__is_logined = False
                if (self.__login_count < MAX):
                    # 上限試行回数までログインを試す
                    self.send_login()
                    self.__login_count += 1

            elif (obj["type"] == MessageType.BroadcasterLoginSuccess):
                self.__is_logined = True
                self.__login_count = 0
                # 言語を通知
                self.notify_language()

            else:
                pass
        except Exception as e:
            print e

