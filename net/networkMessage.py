from basicNetworkMessage import BasicNetworkMessage
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from tasks.coreTaskManger import Task
class NetworkMessage(Task):
    def __init__(self) -> None:
        self.basicNetworkMessage=BasicNetworkMessage()
        
    def terminate(self):
        self.basicNetworkMessage.pauseConnect()

    def start(self,args):
        self.basicNetworkMessage.connect()

    def isAlive(self):
        return self.basicNetworkMessage.testConnected()
    
    def sendMessage(self,webCallbackName,message):
        self.basicNetworkMessage.sendMessage(webCallbackName,message)

    #把回调在网络消息管理器中进行注册 当收到消息的时候 会调用消息中所指定的回调函数
    def registeWebCallback(self,webCallbackName,webCallback):
        self.basicNetworkMessage.registeWebCallback(webCallbackName,webCallback)

    #把回调取消注册
    def deregisteWebCallback(self,webCallbackName):
        self.basicNetworkMessage.deregisteWebCallback(webCallbackName)
