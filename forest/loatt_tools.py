
import itertools
import time
import numpy
import pymeasure
import pyinterface.server_client_wrapper

class loatt_controller(object):
    _latest_bias = []
    
    def __init__(self):
        com1 = pymeasure.ethernet('192.168.40.31', 1234)
        com2 = pymeasure.ethernet('192.168.40.32', 1234)
        
        elva100 = pymeasure.ELVA1.GPDVC15_100
        elva200 = pymeasure.ELVA1.GPDVC15_200
        
        att = [(elva100, com1, 4),
               (elva100, com1, 5),
               (elva200, com1, 6),
               (elva200, com1, 7),
               (elva100, com1, 8),
               (elva100, com1, 9),
               (elva100, com1, 10),
               (elva100, com1, 11),]
        
        self.att = []
        for _att, _host, _gpib in att:
            gpib = pymeasure.gpib_prologix(_host, _gpib)
            self.att.append(_att(gpib))
            continue
            
        self.bias_set(0)
        self.bias_get()
        pass
    
    def bias_set(self, bias, **kwargs):
        """
        Set bias current which applied to LO Att(s).
        
        Args
        ====
        Required
        --------
        < bias : float : (mA) >
            Bias current applied to the LO Att(s). Unit is mA.
            Target Att(s) are specified in the optional parameters.
            
            optional parameters
            - - - - - - - - - -      
             (A) None : If no parameters are specified, <bias> will be applied
                        to all attenuators.
                  
             (B) att : Use Att number (1-8) to specify the target Att.
         
             (C) beam, pol : Use beam number (1-4), and polarization (H, V),
                             to specify the target Att.
        
        optional
        --------
        (Option A)
            Apply <bias> to all attenuators.
            No additional parameters are required.
        
        (Option B)
            Apply <bias> to <drive> attenuator.
            < att : int : 1-8 >
                Attenuator number to specify the target attenuator.
                Attenuator number should be 1-8.
        
        (Option C)
            Apply <bias> to <beam>:<pol> Att.
            < beam : int : 1-4 >
                Beam number to specify the target Att.
                Beam number should be 1-4.
        
            < pol : str : 'H', 'V' >
                Polarization to specify the target Att.
                Polarization should be 'H' or 'V'.
        
        Returns
        =======
        Nothing
        
        Examples
        ========
        >>> b.bias_set(0)
        >>> b.bias_set(1.2)
        >>> b.bias_set(10.2, drive=1)
        >>> b.bias_set(21.01, beam=1)
        >>> b.bias_set(25.43, beam=2, pol='V')
        """
        argc = len(kwargs)
        if argc==0:
            target = loatt_ch_mapper()
        else:
            if kwargs.get('att') is not None:
                att = att_num(kwargs.get('att'))
                target = loatt_ch_mapper(drive=att)
            else:
                beam = beam_num(kwargs.get('beam'))
                pol = pol_char(kwargs.get('pol'))
                target = loatt_ch_mapper(beam=beam, pol=pol)
                pass
            pass
        self._bias_set(bias, target.ind)
        self.bias_get()
        return
    
    def _bias_set(self, bias, targets):
        for t in targets:
            self.att[t].com.use_gpibport()
            self.att[t].output_set(bias)
            time.sleep(0.05)
            continue
        return

    def bias_get(self, **kwargs):
        """
        Get bias current and current of LO Att(s).
        
        Args
        ====
        Required
        --------
        Nothing.
        
        If no parameters are specified, bias currents for all LO Att will be
        returned.
        Target attenuator(s) are specified in the optional parameters.
        
            optional parameters
            - - - - - - - - - -      
             (A) None : If no parameters are specified, the target attenuators
                        are specified as all LO Att.
             
             (B) att : Use Att number (1-8) to specify the target attenuator.
         
             (C) beam, pol : Use beam number (1-4), and polarization (H, V),
                             to specify the target Att.
        
        optional
        --------
        (Option A)
            Get all LO Att bias parameters.
            No additional parameters are required.
        
        (Option B)
            Get bias parameters of <att> attenuator.
            < att : int : 1-4 >
                Attenuator number to specify the target attenuator.
                Attenuator number should be 1-4.
        
        (Option C)
            Get bias parameters of <beam>:<pol> attenuator.
            < beam : int : 1-4 >
                Beam number to specify the target attenuator.
                Beam number should be 1-4.
        
            < pol : str : 'H', 'V' >
                Polarization to specify the target attenuator.
                Polarization should be 'H' or 'V'.
        
        Returns
        =======
        (Option A, B, C)
            < bias_currents : list(float) : (mA) >
                A list of bias currents of all LO Att. Unit is in mA.
        
        (Option B, C)
            Note: If you specified an Att (i.e., specified all arguments;
            for example, in a case of option C, <beam> and <pol>), a float
            values will be returned. (See Examples below.)
                
        Examples
        ========
        >>> b.bias_get()
        [0.12, 0.12, ..., 0.34, 0.32]
        
        >>> b.bias_get(att=1)
        0.12
        
        >>> b.bias_get(beam=1)
        [0.12, 0.12]
        
        >>> b.bias_get(beam=2, pol='H')
        0.12
        """
        argc = len(kwargs)
        if argc==0:
            target = loatt_ch_mapper()
        else:
            if kwargs.get('att') is not None:
                att = att_num(kwargs.get('att'))
                target = loatt_ch_mapper(drive=att)
            else:
                beam = beam_num(kwargs.get('beam'))
                pol = pol_char(kwargs.get('pol'))
                target = loatt_ch_mapper(beam=beam, pol=pol)
                pass
            pass
        ret = self._bias_get(target.ind)
        return ret
        
    def _bias_get(self, targets):
        retall = []
        ret = []
        for i in range(len(self.att)):
            retall.append(self.att[i].output_get())
            continue
        self._latest_bias = retall
        
        for t in targets:
            ret.append(retall[t])
            continue
        return ret
        
    def read_bias(self):
        return self._latest_bias

def loatt():
    client = pyinterface.server_client_wrapper.control_client_wrapper(
        loatt_controller, '192.168.40.13', 4002)
    return client

def loatt_monitor():
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(
        loatt_controller, '192.168.40.13', 4102)
    return client

def start_loatt_server():
    loatt = loatt_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(loatt,
                                                              '', 4002, 4102)
    server.start()
    return server



# ==============
# Helper Classes
# ==============

# Att CH Changer
# ==============
class loatt_ch_mapper(object):
    drive_map = [None, 1, 2, 3, 4, 5, 6, 7, 8]
    
    beam_map = {1:{'H': 1, 'V': 5},
                2:{'H': 2, 'V': 6},
                3:{'H': 3, 'V': 7},
                4:{'H': 4, 'V': 8}}
    
    drive_index = [0, 1, 2, 3, 4, 5, 6, 7]
    
    def __init__(self, drive=None, beam=None, pol=None):
        if drive != None:
            drive = int(drive)
            self.drive = [self.drive_map[drive]]
        elif beam != None:
            beam = int(beam)
            if pol != None:
                pol = str(pol)
                self.drive = [self.beam_map[beam][pol]]
            else:
                self.drive = self.beam_map[beam].values()
                pass
        else:
            self.drive = range(1, 9)
            pass
        self._set_parameters()
        pass
        
    def _set_parameters(self):
        self.beam = []
        self.pol = []
        for beam_id, pols in self.beam_map.items():
            for pol_id, units in pols.items():
                if units in self.drive: 
                    self.beam.append(beam_id)
                    self.pol.append(pol_id)
                    pass
                continue
            continue
        self.ind = [self.drive_index[d-1] for d in self.drive]
        return

# Value Checker Class
# ===================

# Value Checker Base
# ------------------
class value_checker_base(object):
    val = None
    
    def __add__(self, x):
        return self.val.__add__(x)
        
    def __sub__(self, x):
        return self.val.__sub__(x)
        
    def __mul__(self, x):
        return self.val.__mul__(x)

    def __truediv__(self, x):
        return self.val.__truediv__(x)

    def __floordiv__(self, x):
        return self.val.__floordiv__(x)

    def __mod__(self, x):
        return self.val.__mod__(x)

    def __divmod__(self, x):
        return self.val.__divmod__(x)

    def __pow__(self, x):
        return self.val.__pow__(x)

    def __radd__(self, x):
        return self.val.__radd__(x)
        
    def __rsub__(self, x):
        return self.val.__rsub__(x)
        
    def __rmul__(self, x):
        return self.val.__rmul__(x)

    def __rtruediv__(self, x):
        return self.val.__rtruediv__(x)

    def __rfloordiv__(self, x):
        return self.val.__rfloordiv__(x)

    def __rmod__(self, x):
        return self.val.__rmod__(x)

    def __rdivmod__(self, x):
        return self.val.__rdivmod__(x)

    def __rpow__(self, x):
        return self.val.__rpow__(x)

    def __neg__(self, x):
        return self.val.__neg__(x)

    def __pos__(self, x):
        return self.val.__pos__(x)

    def __abs__(self, x):
        return self.val.__abs__(x)

    def __eq__(self, x):
        return self.val == x

    def __ne__(self, x):
        return self.val != x

    def __lt__(self, x):
        return self.val < x

    def __le__(self, x):
        return self.val <= x

    def __gt__(self, x):
        return self.val > x

    def __ge__(self, x):
        return self.val >= x

    def __bool__(self, x):
        return self.val.__bool__(x)
        
    def __index__(self):
        return self.val.__index__()
        
    def __key__(self):
        return self.val.__key__()

    def __str__(self):
        return self.val.__str__()

    def __int__(self):
        return self.val.__int__()

    def __float__(self):
        return self.val.__float__()


class str_container(value_checker_base):
    val = 'A'
    required = [0]
    error_msg = "value should be 'A'."
    
    def __init__(self, val):
        if val is None:
            self.val = val
        else:
            if not val in self.required:
                raise ValueError(self.error_msg + ' (val=%s)'%(val))
            self.val = str(val)
            pass
        pass
        
class int_container(value_checker_base):
    val = 0
    required = [0]
    error_msg = 'value should be 0.'

    def __init__(self, val):
        if val is None:
            self.val = val
        else:
            if not val in self.required:
                raise ValueError(self.error_msg + ' (val=%d)'%(val))
            self.val = int(val)
            pass
        pass

class float_container(value_checker_base):
    val = 0.0
    required_min = -1.0
    required_max = 1.0
    error_msg = 'value should be -1.0 - 1.0.'
    
    def __init__(self, val):
        if val is None:
            self.val = val
        else:
            if not(self.required_min <= val <= self.required_max):
                raise ValueError(self.error_msg + ' (val=%f)'%(val))
            self.val = float(val)
            pass
        pass
    
class array_container(value_checker_base):
    val = []
    required_min = -1.0
    required_max = 1.0
    error_msg = 'value should be -1.0 - 1.0.'
    
    def __init__(self, val):
        if val is None:
            self.val = val
        else:
            _min = self.required_min
            _max = self.required_max
            if not(((_min <= val) & (val <= _max)).all()):
                raise ValueError(self.error_msg + ' (val=%f)'%(val))
            self.val = numpy.array(val)
            pass
        pass

# Values 
# ------
class att_num(int_container):
    required = [1, 2, 3, 4, 5, 6, 7, 8]
    error_msg = 'Box number should be 1-8.'


class beam_num(int_container):
    required = [1, 2, 3, 4]
    error_msg = 'Beam number should be 1-4.'

class pol_char(str_container):
    required = ['H', 'V']
    error_msg = "Polarization should be 'H' or 'V'."


