import math
class D3Position():
    def __init__(self,x,y,z) -> None:
        self.x=x
        self.y=y
        self.z=z
    def distance(self,p1):
        return math.sqrt((self.x-p1.x)**2+(self.y-p1.y)**2+(self.z-p1.z)**2)
    def __add__(self,p1):
        return D3Position(self.x+p1.x,self.y+p1.y,self.z+p1.z)
    def __sub__(self,p1):
        return D3Position(self.x-p1.x,self.y-p1.y,self.z-p1.z)
    def __mul__(self,p1):
        return D3Position(self.x*p1.x,self.y*p1.y,self.z*p1.z)
    def __str__(self):
        return "["+str(str.x)+","+str(str.y)+","+str(str.z)+"]"
class D3Vector():
    def __init__(self,x,y,z) -> None:
        self.x=x
        self.y=y
        self.z=z
    def __add__(self,v1):
        return D3Position(self.x+v1.x,self.y+v1.y,self.z+v1.z)
    def __sub__(self,v1):
        return D3Position(self.x-v1.x,self.y-v1.y,self.z-v1.z)
    def __mul__(self,v1):
        return D3Position(self.x*v1.x,self.y*v1.y,self.z*v1.z)
    def getIncludedAngle(self,v1):
        return math.asin(self*v1/(self.getLength()*v1.getLength()))
    def __str__(self):
        return "["+str(str.x)+","+str(str.y)+","+str(str.z)+"]"        
    def getLength(self):
        return math.sqrt(self*self)