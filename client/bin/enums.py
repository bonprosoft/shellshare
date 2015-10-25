#-*- coding: utf-8 -*-

## python 2.7のenum
## https://gyazo.com/1b122430d032aaf6ca48d5c70995e065

class ContentType():
    PlainText = 0
    CSharp = 1
    Python = 2
    Shell = 3
    JavaScript = 4
    CPlusPlus = 5

class MessageType():
    BroadcasterLoginRequest = 0
    BroadcasterLoginSuccess = 1
    BroadcasterLoginFailed = 2

    ListenerLoginRequest = 10
    ListenerLoginSuccess = 11
    ListenerLoginFailed = 12

    UpdateContentRequest = 20
    UpdateContentTypeRequest = 21

    ListBroadcasterRequest = 30
    ListBroadcasterResponse = 31
    FetchBufferRequest = 32

    UpdateContentNotification = 40
    UpdateContentTypeNotification = 41
    AppendBroadcasterNotification = 42
    RemoveBroadcasterNotification = 43

class UpdateContentType():
    Edit = 0
    Insert = 1
    Delete = 2
    Append = 3
    RefreshAll = 4

