import cv2
import numpy as np

# 双目测距点云
class StereoCamera(object):
    def __init__(self) -> None:
        self.cam_matrix_left=np.zeros([3,3], dtype=np.float64)
        self.cam_matrix_right=np.zeros([3,3], dtype=np.float64)
        self.distortion_left=np.zeros([1,5], dtype=np.float64)
        self.distortion_right=np.zeros([1,5], dtype=np.float64)
        self.R=np.zeros([3,3], dtype=np.float64)
        self.T=np.zeros([3,3], dtype=np.float64)
        self.doffs=0.0
        self.isRectified=False

class MainCameraOpticalProcessingToolBox():
    def __init__(self) -> None:
        self.cameras={}
        self.camerasParts=[]
        self.camerasArguments={}
        # 相对位置x，焦距f，基线b

    def setCameraArguments(self,cameraID,cameraArguments):
        self.camerasArguments[cameraID]=cameraArguments

    def getCameraArguments(self,camersID):
        return self.camerasArguments[camersID]
    
    def registeCamera(self,cameraID,calibrate=False):
        self.cameras[cameraID]=cv2.VideoCapture(cameraID)
        if(calibrate):
            self.calibrateCamera(cameraID)

    def registeCameraPart(self,cameraIDleft,cameraRight):
        i=len(self.camerasParts)
        self.camerasParts.append([cameraIDleft,cameraRight])
        return i
    
    def deregisteCamera(self,camerID):
        del self.cameras[camerID]

    def getCamera(self,cameraID):
        return self.cameras[cameraID]
    
    def calibrateCamera(self,cameraPartID):
        pass

    def getDistanceByDisparity(self,cameraPartID,leftPosition,rightPosition,frame,block_len=8):
        pass

    def openCamera(self,cameraID):
        self.cameras[cameraID]=cv2.VideoCapture(cameraID)
        
    def closeCamera(self,cameraID):
        self.cameras[cameraID].release()
    