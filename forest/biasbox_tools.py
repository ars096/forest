
import itertools
import numpy
import pyinterface
import pyinterface.server_client_wrapper

class biasbox_controller(object):
    _latest_bias = []
    
    def __init__(self):
        ai = pyinterface.create_gpg3100(1)
        ao = pyinterface.create_gpg3300(1)
        ai.use_differential()
        ai.set_range('AD_5V')
        ao.set_range('DA_5V')
        self.daq = pyinterface.create_daq(ai, ao)
        self.bias_get()
        pass
    
    def bias_set(self, bias, **kwargs):
        """
        Set bias voltage which applied to SIS mixer(s).
        
        Args
        ====
        Required
        --------
        < bias : float : (mV) >
            Bias voltage applied to the SIS mixer(s). Unit is mV.
            Target mixer(s) are specified in the optional parameters.
            
            optional parameters
            - - - - - - - - - -      
             (A) None : If no parameters are specified, <bias> will be applied
                        to all mixers.
                  
             (B) box, ch : Use box number (1-4) and ch (1-4) to specify the
                           target mixer.
         
             (C) beam, pol, dsbunit : Use beam number (1-4),
                                      polarization (H, V),
                                      and DSB unit number (1, 2) to specify
                                      the target mixer.
        
        optional
        --------
        (Option A)
            Apply <bias> to all mixers.
            No additional parameters are required.
        
        (Option B)
            Apply <bias> to <box>:<ch> mixer.
            < box : int : 1-4 >
                Box number to specify the target mixer.
                Box number should be 1-4.
        
            < ch : int : 1-4 >
                Ch number to specify the target mixer.
                Ch number should be 1-4.
        
        (Option C)
            Apply <bias> to <beam>:<pol>:<num> mixer.
            < beam : int : 1-4 >
                Beam number to specify the target mixer.
                Beam number should be 1-4.
        
            < pol : str : 'H', 'V' >
                Polarization to specify the target mixer.
                Polarization should be 'H' or 'V'.
        
            < dsbunit : int : 1,2 >
                DSB unit number to specify the target mixer.
                DSB unit number should be 1 or 2.
        
        Returns
        =======
        Nothing
        
        Examples
        ========
        >>> b.bias_set(0)
        >>> b.bias_set(1.2)
        >>> b.bias_set(0.5, box=1)
        >>> b.bias_set(0.5, box=1, ch=2)
        >>> b.bias_set(0.234, beam=1)
        >>> b.bias_set(0.234, beam=2, pol='V')
        >>> b.bias_set(0.234, beam=3, pol='H', dsbunit=2)
        """
        bias = sis_bias_value(bias)
        bias = bias_voltage_output_changer(sis=bias)
        argc = len(kwargs)
        if argc==0:
            self.daq.analog_output(bias.box)
        else:
            if kwargs.get('box') is not None:
                box = biasbox_num(kwargs.get('box'))
                ch = biasbox_ch_num(kwargs.get('ch'))
                sisch = biasbox_ch_mapper(box=box, ch=ch)
            else:
                beam = beam_num(kwargs.get('beam'))
                pol = pol_char(kwargs.get('pol'))
                dsbunit = dsbunit_num(kwargs.get('dsbunit'))
                sisch = biasbox_ch_mapper(beam=beam, pol=pol, dsbunit=dsbunit)
                pass
            self.daq.analog_output(bias.box, sisch.vout)
            pass
        self.bias_get()
        return
        
    def bias_get(self, **kwargs):
        """
        Get bias voltage and current of SIS mixer(s).
        
        Args
        ====
        Required
        --------
        Nothing.
        
        If no parameters are specified, bias voltages and currents
        for all SIS mixers will be returned.
        Target mixer(s) are specified in the optional parameters.
        
            optional parameters
            - - - - - - - - - -      
             (A) None : If no parameters are specified, the target mixers are
                        specified as all SIS mixers.
             
             (B) box, ch : Use box number (1-4) and ch (1-4) to specify the
                           target mixer.
         
             (C) beam, pol, dsbunit : Use beam number (1-4),
                                      polarization (H, V),
                                      and DSB unit number (1, 2) to specify
                                      the target mixer.
        
        optional
        --------
        (Option A)
            Get all mixer's bias parameters.
            No additional parameters are required.
        
        (Option B)
            Get bias parameters of <box>:<ch> mixer.
            < box : int : 1-4 >
                Box number to specify the target mixer.
                Box number should be 1-4.
        
            < ch : int : 1-4 >
                Ch number to specify the target mixer.
                Ch number should be 1-4.
        
        (Option C)
            Get bias parameters of <beam>:<pol>:<num> mixer.
            < beam : int : 1-4 >
                Beam number to specify the target mixer.
                Beam number should be 1-4.
        
            < pol : str : 'H', 'V' >
                Polarization to specify the target mixer.
                Polarization should be 'H' or 'V'.
        
            < dsbunit : int : 1,2 >
                DSB unit number to specify the target mixer.
                DSB unit number should be 1 or 2.
        
        Returns
        =======
        (Option A, B, C)
            < bias_parameters : list(float) : (mV, mA) >
                A list of bias parameters list of all SIS mixers.
                bias_parameters[0] : list of bias voltages (mV)
                bias_parameters[1] : list of bias currents (mA)
        
        (Option B, C)
            Note: If you specified a SIS mixer (i.e., specified all arguments;
            for example, in a case of option B, <box> and <ch>), a list of 
            float values will be returned. (See Examples below.)
                
        Examples
        ========
        >>> b.bias_get()
        [[0.12, 0.12, ..., 0.34, 0.32],
         [0.12, 0.12, ..., 0.34, 0.32]]
        
        >>> b.bias_get(box=1)
        [[0.12, 0.12, 0.34, 0.32],
         [0.12, 0.12, 0.34, 0.32]]
        
        >>> b.bias_get(box=2, ch=3)
        [0.22, 0.11]
        
        >>> b.bias_get(beam=1)
        [[0.12, 0.12, 0.34, 0.32],
         [0.12, 0.12, 0.34, 0.32]]
        
        >>> b.bias_get(beam=2, pol='H')
        [[0.12, 0.12],
         [0.12, 0.12]]
        
        >>> b.bias_get(beam=2, pol='V', ch=3)
        [0.22, 0.11]
        """
        argc = len(kwargs)
        if argc==0:
            sisch = biasbox_ch_mapper()
        else:
            if kwargs.get('box') is not None:
                box = biasbox_num(kwargs.get('box'))
                ch = biasbox_ch_num(kwargs.get('ch'))
                sisch = biasbox_ch_mapper(box=box, ch=ch)
            else:
                beam = beam_num(kwargs.get('beam'))
                pol = pol_char(kwargs.get('pol'))
                dsbunit = dsbunit_num(kwargs.get('dsbunit'))
                sisch = biasbox_ch_mapper(beam=beam, pol=pol, dsbunit=dsbunit)
                pass
            pass
        ret = self.daq.analog_input()
        self._set_latest_bias(ret)
        vin = numpy.array(ret)[sisch.vin]
        vin = bias_voltage_changer(box=vin)
        iin = numpy.array(ret)[sisch.iin]
        iin = bias_current_changer(box=iin)
        return vin.sis, iin.sis
        
    def _set_latest_bias(self, retdata):
        retdata = numpy.array(retdata)
        sischall = biasbox_ch_mapper()
        v = bias_voltage_changer(box=retdata[sischall.vin]).sis
        i = bias_current_changer(box=retdata[sischall.iin]).sis
        self._latest_bias = (v, i)
        return
                                
    def bias_sweep(self, sweep_values, **kwargs):
        bias = sis_bias_array(sweep_values)
        bias = bias_voltage_output_changer(sis=bias)
        argc = len(kwargs)
        if argc==0:
            sisch = biasbox_ch_mapper()
        else:
            if kwargs.get('box') is not None:
                box = biasbox_num(kwargs.get('box'))
                ch = biasbox_ch_num(kwargs.get('ch'))
                sisch = biasbox_ch_mapper(box=box, ch=ch)
            else:
                beam = beam_num(kwargs.get('beam'))
                pol = pol_char(kwargs.get('pol'))
                dsbunit = dsbunit_num(kwargs.get('dsbunit'))
                sisch = biasbox_ch_mapper(beam=beam, pol=pol, dsbunit=dsbunit)
                pass
            pass
        ret = self.daq.analog_sweep(bias.box, sisch.vout)
        vin = numpy.array(ret)[:,sisch.vin]
        vin = bias_voltage_changer(box=vin)
        iin = numpy.array(ret)[:,sisch.iin]
        iin = bias_current_changer(box=iin)
        return vin.sis, iin.sis
        
    def read_bias(self):
        return self._latest_bias

def biasbox():
    client = pyinterface.server_client_wrapper.control_client_wrapper(
        biasbox_controller, '192.168.40.13', 4001)
    return client

def biasbox_monitor():
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(
        biasbox_controller, '192.168.40.13', 4101)
    return client

def start_biasbox_server():
    biasbox = biasbox_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(biasbox,
                                                              '', 4001, 4101)
    server.start()
    return server


# ==============
# Helper Classes
# ==============

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
            val = numpy.array(val)
            _min = self.required_min
            _max = self.required_max
            if not(((_min <= val) & (val <= _max)).all()):
                raise ValueError(self.error_msg + ' (val=%f)'%(val))
            self.val = val
            pass
        pass

# Values 
# ------
class sis_bias_value(float_container):
    required_min = -16.0
    required_max = 16.0
    error_msg = 'SIS bias should be in -16.0 -- 16.0 mV'

class sis_bias_array(array_container):
    required_min = -16.0
    required_max = 16.0
    error_msg = 'SIS bias should be in -16.0 -- 16.0 mV'

class biasbox_num(int_container):
    required = [1, 2, 3, 4]
    error_msg = 'Box number should be 1-4.'

class biasbox_ch_num(int_container):
    required = [1, 2, 3, 4]
    error_msg = 'Box ch number should be 1-4.'

class beam_num(int_container):
    required = [1, 2, 3, 4]
    error_msg = 'Beam number should be 1-4.'

class pol_char(str_container):
    required = ['H', 'V']
    error_msg = "Polarization should be 'H' or 'V'."

class dsbunit_num(int_container):
    required = [1, 2]
    error_msg = 'DSB unit number should be 1 or 2.'


# Bias Unit Changer
# =================
class bias_changer(object):
    sis_to_box_conversion_factor = 1.
    
    def __init__(self, sis=None, box=None):
        if sis is not None:
            self.sis = sis
            self.box = sis * self.sis_to_box_conversion_factor
        else:
            self.box = box
            self.sis = box / self.sis_to_box_conversion_factor
            pass
        pass

class bias_voltage_output_changer(bias_changer):
    sis_to_box_conversion_factor = 1./0.94/3.

class bias_voltage_changer(bias_changer):
    sis_to_box_conversion_factor = -1/5.

class bias_current_changer(bias_changer):
    sis_to_box_conversion_factor = -1/500.


# Bias CH Changer
# ===============
class biasbox_ch_mapper(object):
    boxch_map = {1:{1:1, 2:2, 3:3, 4:4},
                 2:{1:5, 2:6, 3:7, 4:8},
                 3:{1:9, 2:10, 3:11, 4:12},
                 4:{1:13, 2:14, 3:15, 4:16}}
    
    beam_map = {1:{'H':{1:3, 2:4}, 'V':{1:1, 2:2}},
                2:{'H':{1:7, 2:8}, 'V':{1:5, 2:6}},
                3:{'H':{1:9, 2:10}, 'V':{1:11, 2:12}},
                4:{'H':{1:13, 2:14}, 'V':{1:15, 2:16}}}
    
    vout_map = [None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    vin_map = [None, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
    iin_map = [None, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    
    def __init__(self, box=None, ch=None, beam=None, pol=None, dsbunit=None):
        if box != None:
            box = int(box)
            if ch != None:
                ch = int(ch)
                self.sis = [self.boxch_map[box][ch]]
            else:
                self.sis = self.boxch_map[box].values()
                pass
        elif beam != None:
            beam = int(beam)
            if pol != None:
                pol = str(pol)
                if dsbunit != None:
                    dsbunit = int(dsbunit)
                    self.sis = [self.beam_map[beam][pol][dsbunit]]
                else:
                    self.sis = self.beam_map[beam][pol].values()
                    pass
            else:
                sis_list = [s.values() for s in self.beam_map[beam].values()]
                self.sis = list(itertools.chain.from_iterable(sis_list))
                pass
            pass
        else:
            self.sis = range(1, 17)
            pass
        self._set_parameters()
        pass
        
    def _set_parameters(self):
        self.box = []
        self.ch = []
        for box_id, chs in self.boxch_map.items():
            for ch_id, val in chs.items():
                if val in self.sis: 
                    self.box.append(box_id)
                    self.ch.append(ch_id)
                    pass
                continue
            continue
            
        self.beam = []
        self.pol = []
        self.dsbunit = []
        for beam_id, pols in self.beam_map.items():
            for pol_id, units in pols.items():
                for dsbunit_id, val in units.items():
                    if val in self.sis: 
                        self.beam.append(beam_id)
                        self.pol.append(pol_id)
                        self.dsbunit.append(dsbunit_id)
                        pass
                    continue
                continue
            continue
        self.vout = [self.vout_map[s] for s in self.sis]
        self.vin = [self.vin_map[s] for s in self.sis]
        self.iin = [self.iin_map[s] for s in self.sis]
        
        if len(self.sis)==1:
            self.sis = self.sis[0]
            self.box = self.box[0]
            self.ch = self.ch[0]
            self.beam = self.beam[0]
            self.pol = self.pol[0]
            self.dsbunit = self.dsbunit[0]
            self.vout = self.vout[0]
            self.vin = self.vin[0]
            self.iin = self.iin[0]
            pass
        return

