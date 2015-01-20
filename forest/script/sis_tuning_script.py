
import forest
import base

import os
import time
import numpy
import pylab


class sis_tune(base.forest_script_base):
    method = 'sis_tune'
    ver = '2015.01.20'
    
    def run(self, lo_freq):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'lo_freq': lo_freq}
        argstxt = str(args)        
        self.operation_start(argstxt)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Tuning SIS Mixer')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        sis = self.open_sis_biasbox()
        lo_att = self.open_lo_att()
        lo_sg = self.open_lo_sg()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        
        # Operation part
        # --------------
        self.stdout.p('Tuning SIS Mixer')
        self.stdout.p('================')        
        self.stdout.p('lo_freq = %d'%(lo_freq))
        self.stdout.nextline()
        
        self.stdout.p('Load tuning parameters.')
        sisp = forest.load_sis_config(lo_freq)
        unitlist = sorted(sisp.keys())
        self.stdout.p('Set tuning parameters...')
        
        for unit in unitlist:
            _beam = sisp[unit]['beam']
            _pol = sisp[unit]['pol']
            _b1 = sisp[unit]['bias1']
            _b2 = sisp[unit]['bias2']
            _att = sisp[unit]['lo_att']
            self.stdout.p('%s: (bias1) %.2f mV, (bias2) %.2f mV, (LO.Att) %.2f mA'%(unit, _b1, _b2, _att))
            sis.bias_set(_b1, beam=_beam, pol=_pol, dsbunit=1)
            sis.bias_set(_b2, beam=_beam, pol=_pol, dsbunit=2)
            lo_att.bias_set(_att, beam=_beam, pol=_pol)
            continue
        
        self.stdout.nextline()
        
        
        lo_sg_freq = lo_freq / 6.
        self.stdout.p('1st LO : Set RF frequency %f GHz.'%(lo_sg_freq))
        lo_sg.freq_set(lo_sg_freq, 'GHz')
        
        self.stdout.p('1st LO : Set RF power +18 dBm.')
        lo_sg.power_set(18, 'dBm')
        
        self.stdout.p('1st LO : Set RF output ON.')
        lo_sg.output_on()
        
        self.stdout.nextline()
        
        
        # Finalization Section
        # ====================
        
        # Close devices
        # -------------
        self.stdout.p('Close Devices')
        self.stdout.p('=============')
        
        # TODO: implement close method.
        """
        sis.close()
        #lo_sg.close()
        lo_att.close()
        #irr_sg.close()
        rxrot.close()
        slider.close()
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return

