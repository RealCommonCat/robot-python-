#主线程 可以注册任务和取消任务 任务可以根据依赖关系进行启动 相互调用 但是我没空写一个基于XML一类的管理器了
class Task(object):
    def __init__(self) -> None:
        pass

    def terminate(self):
        pass

    def start(self,args):
        pass

    def isAlive(self):
        pass

class CoreTaskManger(object):
    def __init__(self) -> None:
        self.tasks={}
        pass

    def listTasks(self):
        return self.tasks.keys()
    
    def terminateAll(self):
        for key in self.listTasks():
            if(self.tasks[key].isAlive()):
                self.tasks[key].terminate()
                
    