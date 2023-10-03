from global_.globalConstant import DATA_TYPE_ONLY_LASTEST
from global_.globalConstant import DATA_TYPE_CONTINUAL
from global_.globalConstant import ARG_PART
from global_.globalConstant import SECTION_PART
from collections.abc import Callable, Iterable, Mapping
import threading
from typing import Any
import os
import sys
import json
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
# 通过串口和硬件进行通讯的模块


class DevieBasicMessage():
    def __init__(self) -> None:
        super().__init__()

    def init(self):
        # 串口缓存 含义是串口接收的原始信息的缓存序列 这个字典以下位机设备号位键值 以原始信息字符串缓存为值
        self.serialCache = {}
        # 锁 后面用于解析信息时避免数据顺序混乱
        self.lock = threading.RLock()
        self.config = json.loads(open("src/config/DeviceConfig.json").read())
        # 下位机设备号表
        self.deviceIDs = self.config["deviceIDs"]
        # 下位机设备号映射到其串口号
        self.deviceIDtoIO = self.config["deviceIDtoIO"]
        # 以deviceID为键值的实际串口通讯对象
        self.serialsMap = {}
        # 以deviceID为键值的消息缓存池
        self.messageGetCachePool = {}
        # 以moudleID为键值的消息缓存池
        self.messagePool = {}
        # 最大消息缓存池长度
        self.maxMessageCache = 100000
        for deviceID in self.deviceIDs:
            self.messageGetCachePool[deviceID] = GetMessageThread(
                self, name=deviceID)
        self.startAllGetMessage()

    def listDeviceIDs(self):
        return self.deviceIDs
    
    # 通过串口向下位机发送消息
    def sendMessage(self, deviceID, module, datatype, message):
        serial = self.serialsMap[deviceID]
        serial.write(module+ARG_PART+datatype+ARG_PART+message+SECTION_PART)
        serial.flushOutput()

    # 开始轮询下位机上传消息的线程
    def startGetMessage(self, deviceID):
        self.messageGetCachePool[deviceID] = GetMessageThread(
            self, name=deviceID)
        self.messageGetCachePool[deviceID].start()

    # 终止获取消息的线程
    def pauseGetMessage(self, deviceID):
        self.messageGetCachePool[deviceID].terminate()

    def startAllGetMessage(self):
        for deviceID in self.deviceIDs:
            self.startGetMessage(deviceID)

    def pauseAllGetMessage(self):
        for deviceID in self.deviceIDs:
            self.pauseAllGetMessage(deviceID)

    # 内部方法 当线程接到下位机输入的消息调用
    def putMessage(self, deviceID, message):
        if (deviceID not in self.serialCache.keys()):
            self.serialCache[deviceID] = ""
        self.serialCache[deviceID] += message
        if (SECTION_PART in message):
            self.messagePreprocess()

    # 根据deviceID获取COM口
    def getCOMByID(self, deviceID):
        return self.deviceIDtoIO[deviceID]
    
    # 获取所有Serial对象
    def getSerials(self):
        return self.serialsMap.values()
    
    # 获取某个moudle的消息 这些消息的格式是数组 用arg_part隔开的 具体含义根据不同程序情况解释
    def getMessage(self, module):
        return self.messagePool[module]
    
    # 和getMessage不同的是这个是pop
    def popMessage(self, module):
        m = self.messagePool[module]
        self.messagePool[module] = []
        return m
    
    # 切割输入的原始数据 并且按照模块-参数数组的方式放入映射表
    def messagePreprocess(self, deviceID):
        # 取得锁 放置多个线程同时访问原始消息缓存
        self.lock.acquire()
        # 获取指定的下位机目前原始消息缓存
        message = self.messageGetCachePool[deviceID]
        # 根据数据包分划标志切割数据包
        messages = message.split(SECTION_PART)
        # 如果刚好分划成整数个标志数据包 则不需要把结尾放回缓存
        if (message[-1] == SECTION_PART):
            self.messageGetCachePool[deviceID] = ""
        else:
            self.messageGetCachePool[deviceID] = messages[-1]
        # 每个消息再按照参数进行划分
        for m in messages:
            ms = m.split(ARG_PART)
            if (ms[1] == DATA_TYPE_ONLY_LASTEST):
                self.messagePool[ms[0]] = ms[2:]
            elif (ms[1] == DATA_TYPE_CONTINUAL):
                if (ms[0] not in self.messagePool.keys):
                    self.messagePool[ms[0]] = []
                self.messagePool[ms[0]].append(ms[2:])
                if (len(self.maxMessageCache[ms[0]]) > self.maxMessageCache):
                    del self.messageGetCachePool[ms[0][0]]
        self.lock.release()

    # 这个线程会轮询串口从下位机获取的信息
class GetMessageThread(threading.Thread):
    def __init__(self, deviceBasicMessage, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.name = name
        self.isRun = True
        self.deviceBasicMessage = deviceBasicMessage
        self.serials = self.deviceBasicMessage.getSerials()

    def run(self):
        while (self.isRun):
            for idx in self.deviceBasicMessage.listDevices():
                COM = self.deviceBasicMessage.getCOMByID(idx)
                serial = self.serials[COM]
                count = serial.inWaiting()
                if (count != 0):
                    self.deviceBasicMessage.putMessage(idx, serial.read(count))

    def terminate(self):
        self.isRun = False
