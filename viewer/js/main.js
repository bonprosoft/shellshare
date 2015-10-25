var uri = "ws://localhost:4567/";
var webSocket = null;
var TOKEN = "CLIENTAUTHKEY_HERE";

var panes = {};
var paneLayout = null;

var MESSAGE = {
  BroadcasterLoginRequest: 0,
  BroadcasterLoginSuccess: 1,
  BroadcasterLoginFailed: 2,

  ListenerLoginRequest: 10,
  ListenerLoginSuccess: 11,
  ListenerLoginFailed: 12,

  UpdateContentRequest: 20,
  UpdateContentTypeRequest: 21,

  ListBroadcasterRequest: 30,
  ListBroadcasterResponse: 31,
  FetchBufferRequest: 32,

  UpdateContentNotification: 40,
  UpdateContentTypeNotification: 41,
  AppendBroadcasterNotification: 42,
  RemoveBroadcasterNotification: 43
};

var UPDATETYPE = {
  Edit: 0,
  Insert: 1,
  Delete: 2,
  Append: 3,
  RefreshAll: 4
}

function init() {
  open();
}

function open() {
  if (webSocket == null) {
    webSocket = new WebSocket(uri);
    webSocket.onopen = onOpen;
    webSocket.onmessage = onMessage;
    webSocket.onclose = onClose;
    webSocket.onerror = onError;
  }
}

function onOpen(event) {
  appendLog("WebSocket connection opened.");
  var temp = { "type": MESSAGE.ListenerLoginRequest, "data": { "token": TOKEN } };
  sendWebSocket(temp);
}

function statusInitialize() {
  // 現在のPaneをすべて削除
  for (var key in panes) {
    paneLayout.root.contentItems[0].removeChild(panes[key]["item"]);
  }

  panes = {};
  appendLog("Status Initialized.");
 
  var temp = { "type": MESSAGE.ListBroadcasterRequest };
  sendWebSocket(temp);
}

function appendBroadcaster(name, id) {
  var config = {
    title: name,
    type: 'component',
    componentName: 'codeview',
    isClosable: false,
    componentState: { text: "Initialized!", broadcasterId: id }
  };
  var item = paneLayout.createContentItem(config, paneLayout.root);  
  panes[id] = { "name": name , "item": item};

  paneLayout.root.contentItems[0].addChild(item);
  
  appendLog("Connected (name:" + name + ", id:" + id + ")");
  
  // コンテンツのリクエストを送信
  var temp = { "type": MESSAGE.FetchBufferRequest, "data": { "target": id } };
  sendWebSocket(temp);
}

function removeBroadcaster(id) {
  appendLog("Disconnected (name:" + panes[id]["name"] + ", id:" + id + ")");
  paneLayout.root.contentItems[0].removeChild(panes[id]["item"]);
  delete panes[id];
// 
//   panes[id]["item"].close();
}

function sendWebSocket(data) {
  var msg = JSON.stringify(data);
  webSocket.send(msg);
}

function updateContent(content) {
  var target = $("#" + content["id"]);

  switch (content["type"]) {
    case UPDATETYPE.Append:
      var msgtag = $("<li>").text(content["text"]);
      target.append(msgtag);
      break;
  }
}

function onMessage(event) {
  var message = JSON.parse(event.data);
  switch (message["type"]) {
    case MESSAGE.ListenerLoginFailed:
      appendLog("Login Failed");
      break;
    case MESSAGE.ListenerLoginSuccess:
      appendLog("Login Success");
      statusInitialize();
      break;
    case MESSAGE.ListBroadcasterResponse:
      appendLog("Receiving broadcaster list...");
      var data = message["data"];
      for (var i = 0; i < data.length; i++) {
        appendBroadcaster(data[i]["name"], data[i]["id"]);
      }
      break;
    case MESSAGE.UpdateContentNotification:
      var data = message["data"];
      updateContent(data);
      break;
    case MESSAGE.UpdateContentTypeNotification:
      break;
    case MESSAGE.AppendBroadcasterNotification:
      var data = message["data"];
      appendBroadcaster(data["name"], data["id"]);
      break;
    case MESSAGE.RemoveBroadcasterNotification:
      var data = message["data"];
      removeBroadcaster(data["id"]);
      break;
    default:
      break;

  }
}

function onError(event) {
    appendLog("エラーが発生しました");
}

function onClose(event) {
  webSocket = null;
}

function appendLog(message) {
  var chats = $("#logContainer").find("li");
  while (chats.length >= 100) {
    chats = chats.last().remove();
  }
  var msgtag = $("<li>").text("[" + new Date().toLocaleTimeString() + "] : " + message);
  $("#logContainer").prepend(msgtag);
}

$(function () {
  var config = {
    content: [{
      type: 'row',
      content: []
    }]
  };

  paneLayout = new window.GoldenLayout(config, $('#layoutContainer'));

  paneLayout.registerComponent('codeview', function (container, state) {
    container.getElement().html('<ul class="codeview" id="' + state.broadcasterId + '"></ul>');
  });
  
  paneLayout.init();

  // WebSocket通信を開始
  init();

});
