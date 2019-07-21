class Singleton:
    def __init__(self,Class):
        self.Class = Class
        self.instance = None
    def __call__(self,*args,**kwargs):
        if self.instance == None:
            self.instance = self.Class(*args,**kwargs)
        return self.instance