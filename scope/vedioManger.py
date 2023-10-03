import numpy as np
import cv2
import sys
import os,sys 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir) 
from device_api.deviceMessage import DeviceMessage

# 安装在云台上的摄像机
class CameraWithThripod(object):
    def __init__(self,camera,thripodID,deviceMessage) -> None:
        self.camera=camera
        self.thripodID=thripodID
        self.deviceMessage=deviceMessage
    # 转到某个角度
    def goto(self,angx,angz):
        self.deviceMessage.driveThripod(angx,angz,motor=self.thripodID)
    # 目前的角度
    def ang(self):
        return self.deviceMessage.getThripodAng()[int(self.thripodID[-1])]
    
# 摄像机管理器
class VedioManger(object):
    def __init__(self,deviceMessage) -> None:
        self.deviceMessage=DeviceMessage()
        #TODO
        self.cameras={}
        self.cameraWithThripods={}
    # 把某个相机在相机管理器进行注册
    def registeCamera(self,cameraID):
        self.cameras[cameraID]=cv2.VideoCapture(cameraID)
    # 把相机在相机管理器上取消注册
    def derigesteCamera(self,cameraID):
        self.closeCamera(cameraID)
        if(cameraID in self.cameraWithThripods.keys()):
            del self.cameraWithThripods[cameraID]
        del self.cameras[cameraID]
    # 取消某个摄像机的占用
    def closeCamera(self,cameraID):
        self.cameras[cameraID].release()
    # 根据cameraID获取相机对象
    def getCamera(self,cameraID):
        return self.cameras[cameraID]
    # 绑定并注册一个相机和云台
    def registeCameraWithThripods(self,cameraID,thripodID):
        self.cameraWithThripods[cameraID]=CameraWithThripod(self.getCamera(cameraID),thripodID,self.deviceMessage)
    # 获取相机云台
    def getCameraWithThripods(self,cameraID):
        return self.cameraWithThripods(cameraID)