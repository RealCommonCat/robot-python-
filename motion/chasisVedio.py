import cv2 
#底盘测速摄像机 提前进行二值化
class ChasisVedio():
    def __init__(self,camera_id=0) -> None:
        self.camera_id=camera_id
        self.cap=cv2.VideoCapture(camera_id)

    def getPhoto(self):
        ret, frame = self.cap.read()
        return cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)