
import pyinterface

class biasbox(object):
    def __init__(self):
        ai = pyinterface.create_gpg3100(1)
        ao = pyinterface.create_gpg3300(1)
        ai.set_range('AD_5V')
        ao.set_range('DA_5V')
        self.daq = pyinterface.create_daq(ai, ao)
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
             (A) None : If no parameters are specified, <bias> will apply to
                        all mixers.
                  
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
        >>> b.bias_set(0.5, box=1, ch=2)
        >>> b.bias_set(0.234, beam=3, pol='H', dsbunit=2)
        """
        bias = bias_value(bias)
        bias = sis_voltage(sis=bias)
        argc = len(kwargs)
        if argc==0:
            self.daq.analog_output(bias.box)
        else:
            if argc==2:
                box = biasbox_num(kwargs['box'])
                ch = biasbox_ch_num(kwargs['ch'])
                sisch = biasbox_ch_mapper(box=box, ch=ch)
            elif argc==3:
                beam = beam_num(kwargs['beam'])
                pol = pol_char(kwargs['pol'])
                dsbunit = dsbunit_num(kwargs['dsbunit'])
                sisch = biasbox_ch_mapper(beam=beam, pol=pol, dsbunit=dsbunit)
                pass
            self.daq.analog_output(bias.box, sisch.vout)
            pass
        return
        

# ==============
# Helper Classes
# ==============

# Value Container Class
# =====================

# Value Container Base
# --------------------
class str_container(object):
    val = 'A'
    required = [0]
    error_msg = "value should be 'A'."

    def __init__(self, val):
        if not val in self.required:
            raise ValueError(self.error_msg + ' (val=%s)'%(val))
        self.val = val
        pass
        
    def __str__(self):
        return self.val

class int_container(object):
    val = 0
    required = [0]
    error_msg = 'value should be 0.'

    def __init__(self, val):
        if not val in self.required:
            raise ValueError(self.error_msg + ' (val=%d)'%(val))
        self.val = val
        pass
        
    def __int__(self):
        return self.val

class float_container(object):
    val = 0.0
    required_min = -1.0
    required_max = 1.0
    error_msg = 'value should be -1.0 - 1.0.'
    
    def __init__(self, val):
        if not(self.required_min < val < self.required_max):
            raise ValueError(self.error_msg + ' (val=%f)'%(val))
        self.val = val
        pass
        
    def __float__(self):
        return self.val

# Values 
# ------
class sis_bias_value(float_container):
    required_min = 0.0
    requred_max = 1.0
    error_msg = 'SIS bias should be in 0.0 - 1.0 mV'

class sis_voltage(bias_changer):
    sis_to_box_conversion_factor = 1.
    
class sis_current(bias_changer):
    sis_to_box_conversion_factor = 1.

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
            self.box = sis * self.sis_to_boxconversion_factor
        else:
            self.box = box
            self.sis = box / self.sis_to_boxconversion_factor
            pass
        pass


# Bias CH Changer
# ===============
class biasbox_ch_mapper(object):
    boxch_map = {1:{1:1, 2:2, 3:3, 4:4},
                 2:{1:5, 2:6, 3:7, 4:8},
                 3:{1:9, 2:10, 3:11, 4:12},
                 4:{1:13, 2:14, 3:15, 4:16}}
    
    beam_map = {1:{'H':{1:1, 2:2}, 'V'{1:3, 2:4}},
                2:{'H':{1:5, 2:6}, 'V'{1:7, 2:8}},
                3:{'H':{1:9, 2:10}, 'V'{1:11, 2:12}},
                4:{'H':{1:13, 2:14}, 'V'{1:15, 2:16}}}
    
    vout_map = [None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    vin_map = [None, 1, 3, 5, 7, 17, 19, 21, 23, 33, 35, 37, 39, 49, 51, 53, 55]
    iin_map = [None, 0, 2, 4, 6, 16, 18, 20, 22, 32, 34, 36, 38, 48, 50, 52, 54]
    
    def __init__(self, box=None, ch=None, beam=None, pol=None, dsbunit=None):
        if box is not None:
            self.sis = self.boxch_map[box][ch]
        else:
            self.sis = self.beam_map[beam][pol][dsbunit]
            pass
        self._set_parameters()
        pass
        
    def _set_parameters(self):
        for box_id, chs in boxch_map.items():
            for ch_id, val in chs.items():
                if val==self.sis: 
                    self.box = box_id
                    self.ch = ch_id
                    pass
                continue
            continue
        for beam_id, pols in beam_map.items():
            for pol_id, units in pols.items():
                for dsbunit_id, val in units.items():
                    if val==self.sis: 
                        self.beam = beam_id
                        self.pol = pol_id
                        self.dsbunit = dsbunit_id
                        pass
                    continue
                continue
            continue
        self.vout = vout_map[self.sis]
        self.vin = vin_map[self.sis]
        self.iin = iin_map[self.sis]
        return

