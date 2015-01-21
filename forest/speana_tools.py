
import multiprocessing.dummy
import pymeasure


def speana1():
    com = pymeasure.ethernet('192.168.40.61', 5025)
    sp = pymeasure.Agilent.N9343C(com)
    return sp

def speana2():
    com = pymeasure.ethernet('192.168.40.62', 5025)
    sp = pymeasure.Agilent.N9343C(com)
    return sp

def speana3():
    com = pymeasure.ethernet('192.168.40.63', 5025)
    sp = pymeasure.Agilent.N9343C(com)
    return sp

def speana4():
    com = pymeasure.ethernet('192.168.40.64', 5025)
    sp = pymeasure.Agilent.N9343C(com)
    return sp


class speana(object):
    def __init__(self):
        self.sp = [speana1(), speana2(), speana3(), speana4()]
        self.attr = [a for a in dir(self.sp[0]) if a[0]!='_']
        self._p = multiprocessing.dummy.Pool(4)
        pass
        
    def __getattr__(self, name):
        if name in self.attr:
            self._call_name = name
            return self._call
        return self.__getattribute__(name)
        
    def _call(self, *args, **kwargs):
        def exec_method(method):
            return method(*args, **kwargs)
        
        func = [s.__getattribute__(self._call_name) for s in self.sp]
        ret = self._p.map(exec_method, func)
        
        self._call_name = None
        return ret
        
