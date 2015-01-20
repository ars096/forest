
import pymeasure

def irrsg():
    com = pymeasure.ethernet('192.168.40.41', 10001)
    sg = pymeasure.Phasematrix.FSW0020(com)
    return sg
    
