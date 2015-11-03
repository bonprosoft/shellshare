#-*- coding: utf-8 -*-
import json
from enums import *
import uuid

class StreamManager(object):

    def __init__(self):
        self.__listener = []
        self.__broadcaster = {}

        self.LISTENER_KEY = "CLIENTAUTHKEY_HERE"
        self.BROADCASTER_KEY = "BROADCASTERKEY_HERE"
        self.BROADCASTER_SECRET = "BROADCASTERSECRET_HERE"

    def is_listener(self, user):
        return user in self.__listener

    def is_broadcaster(self, user):
        return user in self.__broadcaster

    def login_broadcaster(self, user, name, token, secret):
        if (token != self.BROADCASTER_KEY or secret != self.BROADCASTER_SECRET):
            data = {"type": MessageType.BroadcasterLoginFailed, "data": "Invalid token, secret"}
            s = json.dumps(data)
            user.write_message(s)
            return

        if (not user in self.__broadcaster):
            cid = uuid.uuid4().hex
            self.__broadcaster[user] = {"id": cid, "buffer": [], "content_type": ContentType.PlainText}

            data = {"type": MessageType.AppendBroadcasterNotification, "data": {"id": cid, "name": name}}
            s = json.dumps(data)

            for cl in self.__listener:
                cl.write_message(s)

        self.__broadcaster[user]["name"] = name
        data = {"type": MessageType.BroadcasterLoginSuccess, "data": ""}
        s = json.dumps(data)
        user.write_message(s)

    def logout_broadcaster(self, user):
        if (user in self.__broadcaster):
            cid = self.__broadcaster[user]["id"]
            del self.__broadcaster[user]

            data = {"type": MessageType.RemoveBroadcasterNotification , "data": {"id": cid}}
            s = json.dumps(data)

            for cl in self.__listener:
                cl.write_message(s)

    def login_listener(self, user, token):
        if (token != self.LISTENER_KEY):
            data = {"type": MessageType.ListenerLoginFailed, "data": "Invalid token"}
            s = json.dumps(data)
            user.write_message(s)
            return

        if (not user in self.__listener):
            self.__listener.append(user)

        data = {"type": MessageType.ListenerLoginSuccess, "data": ""}
        s = json.dumps(data)
        user.write_message(s)

    def logout_listener(self, user):
        if (user in self.__listener):
            self.__listener.remove(user)

    def request_broadcaster_list(self, sender):
        if (not self.is_listener(sender)):
            return

        temp = [{"id": v["id"], "name": v["name"]} for k,v in self.__broadcaster.iteritems()]
        data = {"type": MessageType.ListBroadcasterResponse, "data": temp}
        s = json.dumps(data)
        sender.write_message(s)

    def request_buffer(self, sender, user_id):
        if (not self.is_listener(sender)):
            return

        temp = [(k,v) for k,v in self.__broadcaster.iteritems() if v["id"] == user_id]
        if (len(temp) != 1):
            return

        # 送信
        broadcaster = temp[0][1]
        buf = broadcaster["buffer"]
        content_type = broadcaster["content_type"]

        data = {"type": MessageType.UpdateContentTypeNotification, "data": {"id": broadcaster["id"],"content_type": content_type}}
        s = json.dumps(data)
        sender.write_message(s)


        for i in buf:
            data = {"type": MessageType.UpdateContentNotification, "data": {"id": broadcaster["id"], "type": UpdateContentType.Append, "text": i, "pos" : -1}}
            s = json.dumps(data)
            sender.write_message(s)

    def update_content(self, sender, data):
        if (not self.is_broadcaster(sender)):
            return

        user = self.__broadcaster[sender]
        data["text"] = re.sub(r'\\e\[[0-9]*m', data["text"], "")
        text = data["text"]
        position = data["pos"]

        t = data["type"]
        if (t == UpdateContentType.RefreshAll):
            user["buffer"] = []
        elif (t == UpdateContentType.Append):
            user["buffer"].append(text)
        elif (position < len(user["buffer"]) and position >= 0):
            # 再度分岐
            if (t  == UpdateContentType.Delete):
                del user["buffer"][position]
            elif (t == UpdateContentType.Edit):
                user["buffer"][position] = text
            elif (t == UpdateContentType.Insert):
                user["buffer"].insert(position, text)
            else:
                return
        else:
            return

        data["id"] = user["id"]
        temp = {"type": MessageType.UpdateContentNotification, "data": data}
        s = json.dumps(temp)

        for cl in self.__listener:
            cl.write_message(s)

    def update_content_type(self, sender, data):
        if (not self.is_broadcaster(sender)):
            return

        user = self.__broadcaster[sender]
        user["content_type"] = data["content_type"]

        data["id"] = user["id"]
        temp = {"type": MessageType.UpdateContentTypeNotification, "data": data}
        s = json.dumps(temp)

        for cl in self.__listener:
            cl.write_message(s)

