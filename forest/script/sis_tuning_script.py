
import forest
import base

import ConfigParser
import os
import time
import numpy
import pylab


class sis_tune(base.forest_script_base):
    method = 'sis_tune'
    ver = '2015.01.26'
    
    def run(self, name):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'name': name}
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
        self.stdout.p('name = %s'%(name))
        self.stdout.nextline()
        
        self.stdout.p('Load tuning parameters.')
        sisp = forest.load_sis_config(name)
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
        
        lo_freq = float(name.split('-')[0])
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

class sis_tune_temp(base.forest_script_base):
    method = 'sis_tune_temp'
    ver = '2015.01.26'
    
    def run(self, filepath):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'filepath': filepath}
        argstxt = str(args)        
        self.operation_start(argstxt)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Tuning SIS Mixer in temporary')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
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
        self.stdout.p('path = %s'%(filepath))
        self.stdout.nextline()
        
        self.stdout.p('Load tuning parameters.')
        sisp = ConfigParser.SafeConfigParser()
        sisp.read(filepath)
        unitlist = sorted(sisp.sections())
        self.stdout.p('Set tuning parameters...')
        
        for unit in unitlist:
            if unit == 'LO_SG': continue
            _beam = int(unit.strip('beam-hv'))
            _pol = unit.strip('beam1234-').upper()
            _b1 = sisp.get(unit, 'bias1')
            _b2 = sisp.get(unit, 'bias2')
            _att = sisp.get(unit, 'lo_att')
            self.stdout.p('%s: (bias1) %.2f mV, (bias2) %.2f mV, (LO.Att) %.2f mA'%(unit, _b1, _b2, _att))
            sis.bias_set(_b1, beam=_beam, pol=_pol, dsbunit=1)
            sis.bias_set(_b2, beam=_beam, pol=_pol, dsbunit=2)
            lo_att.bias_set(_att, beam=_beam, pol=_pol)
            continue
        
        self.stdout.nextline()
        
        lo_freq = float(sisp.get('LO_SG', 'freq'))
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


class sis_tune_show_params(base.forest_script_base):
    method = 'sis_tune_show_params'
    ver = '2015.01.26'
    
    def run(self, name):
        # Initialization Section
        # ======================
        
        # Print welcome message
        # ---------------------
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('FOREST : Show SIS Tuning Params')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('ver.%s'%(self.ver))
        print('')
        
        
        # Operation Section
        # =================
        
        # Operation part
        # --------------
        print('Show Tuning Params')
        print('==================')        
        print('name = %s'%(name))
        print('')
        
        print('Load tuning parameters.')
        sisp = forest.load_sis_config(name)
        unitlist = sorted(sisp.keys())
        
        for unit in unitlist:
            _beam = sisp[unit]['beam']
            _pol = sisp[unit]['pol']
            _b1 = sisp[unit]['bias1']
            _b2 = sisp[unit]['bias2']
            _att = sisp[unit]['lo_att']
            print('%s: (bias1) %.2f mV, (bias2) %.2f mV, (LO.Att) %.2f mA'%(unit, _b1, _b2, _att))
            continue
        
        print('')
        
        
        lo_freq = float(name.split('-')[0])
        lo_sg_freq = lo_freq / 6.
        print('1st LO SG frequency : %f GHz.'%(lo_sg_freq))
        
        print('')
        
        
        # Finalization Section
        # ====================
        
        return


class sis_tune_show_availables(base.forest_script_base):
    method = 'sis_tune_show_availables'
    ver = '2015.01.26'
    
    def run(self):
        # Initialization Section
        # ======================
        
        # Print welcome message
        # ---------------------
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('FOREST : Show Available SIS Tuning Params')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('ver.%s'%(self.ver))
        print('')        
        
        
        # Operation Section
        # =================
        
        # Operation part
        # --------------
        print('Show Available Tuning Params')
        print('============================')        
        print('')        
        
        print('Load tuning parameters.')
        sisp = forest.load_tuning_available()
        unitlist = sorted(sisp.keys())
        
        for unit in unitlist:
            availables = ', '.join(sisp[unit])
            print('%s: %s'%(unit, availables))
            continue
        
        print('')
        
        
        # Finalization Section
        # ====================
        
        return

