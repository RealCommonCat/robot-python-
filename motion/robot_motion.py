from collections.abc import Callable, Iterable, Mapping
from typing import Any
from device_api.deviceMessage import DeviceMessage
from displacement import DisplacementVedio
from displacement import IntegratedAccelerationDisplacement
import threading
import time
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from tasks.coreTaskManger import Task
# 机器人运动定义类型 包括了机器人的运动API 机器人运动状态的API 这个运动指的是“移动” 并不包括机械臂等外设在内


class RobotMotion(Task):
    def __init__(self, deviceMessage) -> None:
        self.name = "238 Robot"
        self.deviceMessage = deviceMessage
        self.speed = [0, 0]

    # 获取原始位置数据 一般由GPS直接输出
    def getLocalPosition(self):
        self.deviceMessage.getGPSLocalPosition()

    # 获取精确位移数据 一般输入加速度积分 并且定期借助视频位移测量进行校准
    def getExactDisplacement(self, orginalPosition, endPosition):
        return (endPosition-orginalPosition)[0]
    
    # 获取水平方向角度 由地磁输入
    def getHorizontalDirection(self):
        return self.deviceMessage.getOriginalDirectionCompassList[-1]
    
    # 获取原始速度数据 由GPS输入
    def getLocalSpeed(self):
        return self.deviceMessage.getGPSLocalSpeedList[-1]
    
    # 获取精确速度 一般由加速度计输入 视频校准
    def getOriginalExactSpeed(self):
        #TODO
        return
    
    # 顺时针为正 角度制
    def rotate(self, ang):
        pass

    # 前进距离 单位为米 米每秒
    def linearMove(self, distance, speed):
        pass

    # 终止移动
    def stopLinearMove(self):
        pass

    # 终止转动
    def stopRotate(self):
        pass

    #!!!飙车模式!!!
    def startTeleport(self):
        pass
    
    # 开始自动更新数据 自动校准
    # TODO
    def startAutoStateReflush(self):
        self.autoSateReflush = AutoRobotMotionState()
        self.autoSateReflush.start()
    def start(self):
        self.startAutoStateReflush()
    def terminate(self):
        self.autoSateReflush.isRun=False
    def isAlive(self):
        return self.autoSateReflush.isRun

class AutoRobotMotionState(threading.Thread):
    def __init__(self, robot, correctingTimes=10, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        self.robot = robot
        self.lastExactSpeedCorrectingTime = time.time_ns()
        self.isRun = True
        self.correctingTimes = correctingTimes
        self.lastIntegratedAccelerationDisplacementTime = time.time_ns()
        self.lastIntegratedAccelerationDisplacement = IntegratedAccelerationDisplacement()
        self.lastDisplacementVedioTime = time.time_ns()
        self.lastDisplacementVedio = DisplacementVedio()
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    def run(self):
        i = 0
        while (self.isRun):
            i+=1
            if (i > self.correctingTimes):
                i = 0
                nowTime = time.time_ns()
                nowDisplacementVedio = DisplacementVedio()
                deltaTime = nowTime-self.lastDisplacementVedioTime
                self.lastDisplacementVedioTime = nowTime
                d = (nowDisplacementVedio-self.lastDisplacementVedio)
                self.lastDisplacementVedio = nowDisplacementVedio
                self.robot.speed[0] = d[0]/deltaTime
                self.robot.speed[1] = d[0]/deltaTime
