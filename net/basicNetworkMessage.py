from collections.abc import Callable, Iterable, Mapping
import json
import asyncio
from typing import Any
import websocket
import threading


class BasicNetworkMessage():
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.init()

    def init(self):
        self.config = json.loads(open(r"src/config/NetworkConfig.json").read())
        self.core_addr = self.config["core"]["addr"]
        self.core_port = self.config["core"]["port"]
        self.wifi_ssid = self.config["wifi"]["ssid"]
        self.wifi_pwd = self.config["wifi"]["pwd"]
        self.isConnected = False
        self.websocket = websocket.WebSocketApp(
            url="ws://"+self.core_addr, on_message=self.messageProcess, on_error=self.error, on_close=self.closed)
        self.webCallbacks = {}

    # 收到websocket的消息后进行解析的函数，websocket的消息都是JSON格式的，其model是值得某个回调函数的键值
    async def messageProcess(self, websocket, message):
        try:
            m = json.loads(message)
            webCallbackName = m["webCallbackName"]
            self.webCallbacks[webCallbackName].webCallbackRun(webCallbackName)
        except:
            print("failed")

    def error(self, websocket, e):
        self.isConnected = False

    def closed(self):
        self.isConnected = False

    def connect(self):
        WebSocketConnector(self).start()

    def pauseConnect(self):
        self.websocket.close()
        self.isConnected = False

    def sendMessage(self, webCallbackName, message):
        try:
            self.websocket.send(json.dumps(
                {"webCallbackName": webCallbackName, "message": message}))
        except:
            pass
        # TODO

    # 测试连接
    def testConnected(self):
        try:
            self.websocket.send("")
        except:
            self.isConnected = False
            return False

    def registeWebCallback(self, webCallbackName, webCallback):
        self.webCallbacks[webCallbackName] = webCallback

    def deregisteWebCallback(self, webCallbackName):
        if (webCallbackName in self.webCallbacks.keys()):
            del self.webCallbacks[webCallbackName]

#因为在启动了websocket以后，会进入阻塞状态，所以做一个线程来承接这个进入阻塞状态的方法，使得调用网络启动服务的服务不会被堵塞
class WebSocketConnector(threading.Thread):
    def __init__(self,basicNetworkMessage, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        self.basicNetworkMessage=basicNetworkMessage
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        
    def run(self):
        self.basicNetworkMessage.websocket.run_forever(ping_interval=5, ping_timeout=2)