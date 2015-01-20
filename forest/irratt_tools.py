
import itertools
import time
import numpy
import pymeasure
import pyinterface.server_client_wrapper

class irratt_controller(pymeasure.loatt_controller):
    _latest_bias = []
    
    def __init__(self):
        com2 = pymeasure.ethernet('192.168.40.32', 1234)
        
        elva100 = pymeasure.ELVA1.GPDVC15_100
        elva200 = pymeasure.ELVA1.GPDVC15_200
        
        att = [(elva200, com2, 12),]
        
        self.att = []
        for _att, _host, _gpib in att:
            gpib = pymeasure.gpib_prologix(_host, _gpib)
            self.att.append(_att(gpib))
            continue
            
        self.bias_set(0)
        self.bias_get()
        pass
    

def irratt():
    client = pyinterface.server_client_wrapper.control_client_wrapper(
        irratt_controller, '192.168.40.13', 4005)
    return client

def irratt_monitor():
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(
        irratt_controller, '192.168.40.13', 4105)
    return client

def start_irratt_server():
    irratt = irratt_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(irratt,
                                                              '', 4005, 4105)
    server.start()
    return server



