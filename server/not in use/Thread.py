import threading

class Thread():
    def __init__(self):
        self.threads=[]
    def CreateThread(self,func,args=[]):
        thread=threading.Thread(target=func,args=args)
        thread.start()
        self.threads.append(thread)
        return thread

    def removeThread(self,thread):
            self.threads.remove(thread)
                    