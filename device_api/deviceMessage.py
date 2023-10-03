from tasks.coreTaskManger import Task
from global_.globalConstant import DATA_TYPE_CONTINUAL
from global_.globalConstant import DATA_TYPE_ONLY_LASTEST
from global_.globalConstant import SECTION_PART
from global_.globalConstant import ARG_PART
from deviceBasicMessage import DevieBasicMessage
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
defaultDevice0ID = "device0"


class DeviceMessage(Task):
    def __init__(self) -> None:
        self.deviceBasicMessage0 = DevieBasicMessage()

    # 驱动底盘电机
    def driveChassisMotor(self, tickPerSecond, ticks, motor="ChassisBoth"):
        self.deviceBasicMessage0.sendMessage(defaultDevice0ID, "DriveChassisMotor", DATA_TYPE_ONLY_LASTEST, str(
            tickPerSecond)+"&"+str(ticks)+"&"+str(motor))
        
    # 急停底盘电机
    def pauseChassisMotor(self, motor="ChassisBoth"):
        self.deviceBasicMessage0.sendMessage(
            defaultDevice0ID, "PauseChassisMotor", DATA_TYPE_ONLY_LASTEST, str(motor))
        
    # 驱动云台转到某个指定角度
    def driveThripod(self, angx, angz, motor="TripodMotor0"):
        self.deviceBasicMessage0.sendMessage(
            defaultDevice0ID, "TripodMotor", DATA_TYPE_ONLY_LASTEST, str(angx)+"&"+str(angz)+"&"+str(motor))
        
    # 获取基于GPS的原始位置数据序列 以[{时间，[latitude,longitude,height]},]的形式
    def getGPSLocalPositionList(self):
        return self.deviceBasicMessage0.getMessage("GPSPosition0")
    
    #获取基于GPS的本地时间序列 
    def getGPSLocalSpeedList(self):
        return self.deviceBasicMessage0.getMessage("GPSSpeed0")
    
    def getOriginalAcceleratedSpeedList(self):
        return self.deviceBasicMessage0.getMessage("AcceleratedSpeed0")

    def getOriginalDirectionCompassList(self):
        return self.deviceBasicMessage0.getMessage("Compass0")

    def getPitAngle(self):
        return self.deviceBasicMessage0.getMessage("PitAngle0")

    def getThripodAng(self):
        return self.deviceBasicMessage0.getMessage("TripodMotor")

    def start(self, args):
        self.deviceBasicMessage0.startGetMessage(args[0])

    def terminate(self):
        self.deviceBasicMessage0.pauseAllGetMessage()

    def isAlive(self):
        isAlive = False
        for i in self.deviceBasicMessage0.messageGetCachePool.keys():
            if (i.isRun):
                isAlive = True
        return isAlive
