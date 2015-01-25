
import functools
import pymeasure


def losg1():
    com = pymeasure.ethernet('192.168.40.21', 7777)
    sg = pymeasure.Agilent.E8257D(com)
    return sg

def losg2():
    com = pymeasure.ethernet('192.168.40.22', 7777)
    sg = pymeasure.Agilent.E8257D(com)
    return sg



class losg(object):
    def __init__(self):
        self.sg = [losg1(), losg2()]
        self.attr = [a for a in dir(self.sg[0]) if a[0]!='_']
        pass
        
    def __getattr__(self, name):
        if name in self.attr:
            self._call_name = name
            return self._call
        return self.__getattribute__(name)
        
    def _call(self, *args, **kwargs):
        ret = [s.__getattribute__(self._call_name)(*args, **kwargs) \
               for s in self.sg]
        self._call_name = None
        return ret
        
