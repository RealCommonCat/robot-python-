from global_.globalDataStructure import D3Vector
from global_.globalDataStructure import D3Position
import sklearn as skm
import sys
import math
from chasisVedio import ChasisVedio
import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
chasisVedio0 = ChasisVedio()
# 位移类 其作为一个标志 在初始化的时候会记录此时机器的位置 这个绝对的位置是没有意义的 但是其可以和比的位移做差 获得一个从末尾指向开头的向量


class Displacement():
    def __init__(self, deviceMessage) -> None:
        self.deviceMessage = deviceMessage

    def __sub__(self, displacement1):
        pass

# 根据底盘视觉输入获取位移数据


class DisplacementVedio(Displacement):
    def __init__(self, factHeight=0.4, factWidth=0.4, scanRate=0.2, scanScopeRate=0.2, mulLowbound=1, r=5) -> None:
        super().__init__()
        # 相关系数下界
        self.mulLowBound = mulLowbound
        # 拍照
        photo = chasisVedio0.getPhoto()
        self.photo = photo
        # 扫描采样率倒数
        self.r = r
        height = len(photo)
        width = len(photo[0])
        # 照片对应的显示长宽
        self.factHeight = factHeight
        self.factWidth = factWidth
        self.height = height
        self.width = width
        # 扫描长宽
        self.scanWidth = scanRate*width
        self.scanHeight = scanRate*height
        # 扫描框长宽
        self.scanScopeWidth = scanScopeRate*width
        self.scanScopeHeight = scanScopeRate*height
        # 扫描边界
        self.heightLowBound = int((0.5)*(1-scanRate)*height)
        self.heightTopBound = int((0.5)*(1+scanRate)*height)
        self.widthLeftBound = int((0.5)*(1-scanRate)*width)
        self.widthRightBound = int((0.5)*(1+scanRate)*width)
        # 防止扫描边界超过边界
        if (self.heightLowBound < int(self.scanScopeHeight/2)):
            self.scanScopeHeight = self.heightLowBound
        if (self.widthLeftBound < int(self.scanScopeWidth/2)):
            self.scanScopeWidth = self.widthLeftBound
        self.scopePhoto = photo[self.heightLowBound:self.heightTopBound,
                                self.widthLeftBound:self.widthRightBound]
        # 获取互相关系数

    def __mul__(self, displacement1):
        return skm.mutual_info_score(self.photo, displacement1.photo)
        # 选择互相关系数最大的位移量

    def __sub__(self, displacement1):
        # 裁剪出移动后的图像的扫描区域
        scopePhoto1 = displacement1.photo[self.heightLowBound-int(self.scanScopeHeight/2):self.heightTopBound-int(
            self.scanScopeHeight/2), self.widthLeftBound-int(self.scanScopeWidth/2):self.widthRightBound-int(self.scanScopeWidth/2)]
        maxMul = scopePhoto1*self
        # 从扫描区域左下角开始扫描
        x = -int(self.scanScopeWidth/2)
        y = -int(self.scanScopeHeight/2)
        x_min = x
        y_min = y
        # 选出相关系数最大值的方向
        while (x <= self.scanScopeWidth/2):
            while (y <= self.scanScopeHeight/2):
                x += self.width*self.r
                y += self.height*self.r
                mul = self.scopePhoto * \
                    displacement1.photo[self.heightLowBound+x:self.heightTopBound +
                                        x, self.widthLeftBound+y:self.widthRightBound+y]
                if (mul > maxMul):
                    maxMul = mul
                    x_min = x
                    y_min = y
        # 如果相关系数小于阈值 视为超出位移扫描范围 也就是图像飞出去了 因为帧间隔过大
        if (maxMul < self.mulLowBound):
            raise DisplacementVedioOutofRangeException()
        return D3Vector(x_min*self.factWidth/self.width, y_min*self.factHeight/self.height, 0)

# 图像监控位移超过范围


class DisplacementVedioOutofRangeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# 取到的加速度数据队列不包含某些需要的时间段内的数据


class IntegratedAccelerationDisplacementOverRangeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# 根据积分加速度传感器的数据获取位移


class IntegratedAccelerationDisplacement(Displacement):
    def __init__(self, deviceMessage,speed) -> None:
        self.speed=speed
        self.time = deviceMessage.getOriginalAcceleratedSpeedList()[-1][0]
        super().__init__(deviceMessage)

    def __sub__(self, displacement1):
        
        endTime = displacement1.time
        accelerationDisplacmentList = self.deviceMessage.getOriginalAcceleratedSpeedList()
        if (accelerationDisplacmentList[0][0] > endTime or accelerationDisplacmentList[0][0] > self.time):
            raise (IntegratedAccelerationDisplacementOverRangeException())
        i = -1
        timeUpBound = endTime
        timeDownBound = self.time
        if (self.time < endTime):
            timeUpBound = self.time
            timeDownBound = endTime
        nowTime = timeDownBound
        i = 0
        while (timeDownBound >= accelerationDisplacmentList[i][0]):
            i += 1
        xy = [0, 0]
        vxy = [0, 0]
        while (timeDownBound <= nowTime <= timeUpBound):
            nowTime = accelerationDisplacmentList[i][0]
            deltaTime = accelerationDisplacmentList[i][0] - \
                accelerationDisplacmentList[i-1][0]
            averageAX = (
                accelerationDisplacmentList[i][1]+accelerationDisplacmentList[i][1])/2
            averageAY = (
                accelerationDisplacmentList[i][2]+accelerationDisplacmentList[i][2])/2
            vxy[0] += averageAX*deltaTime
            vxy[1] += averageAY*deltaTime
            xy[0] += vxy[0]*deltaTime
            xy[1] += vxy[1]*deltaTime
        return [D3Vector(xy[0],xy[1]), D3Vector(vxy[0],vxy[1])]
