
import forest
import base


class initialize(base.forest_script_base):
    method = 'initialize'
    ver = '2015.03.05'
    
    def run(self):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        self.operation_start()
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : System Initialize ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        sis = self.open_sis_biasbox()
        lo_sg = self.open_lo_sg()
        lo_att = self.open_lo_att()
        irr_sg = self.open_irr_sg()
        switch = self.open_switch()
        speana = self.open_speana()
        rxrot = self.open_rxrot()
        slider = self.open_slider()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('System Initialize')
        self.stdout.p('=================')
        
        self.stdout.write('SIS Bias : Set 0 mV ... ')
        sis.bias_set(0)
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('1st LO SG : Set -130 dBm ... ')
        lo_sg.power_set(-130)
        self.stdout.write('ok')
        
        self.stdout.write('1st LO SG : Set 10 GHz ... ')
        lo_sg.freq_set(10, 'GHz')
        self.stdout.write('ok')
        
        self.stdout.write('1st LO SG : Set output off ... ')
        lo_sg.output_off()
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('1st LO Att : Set max attenuation ... ')
        lo_att.bias_set(200)
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('IRR SG : Set output off ... ')
        irr_sg.output_off()
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('IRR SG : Use external reference source ... ')
        irr_sg.use_external_reference_source()
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('IF Switch : Set ch 1 ... ')
        switch.ch_set_all(1)
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('Speana : Preset ... ')
        speana.scpi_reset()
        self.stdout.write('ok')
        
        self.stdout.write('Speana : Set start freq 4 GHz.')
        speana.frequency_start_set(4, 'GHz')
        self.stdout.write('ok')
        
        self.stdout.write('Speana : Set stop freq 12 GHz.')
        speana.frequency_stop_set(12, 'GHz')
        self.stdout.write('ok')
        
        self.stdout.write('Speana : Set resolution BW 3 MHz.')
        speana.resolution_bw_set(3, 'MHz')
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('Rx Rotator : Move to 0 deg ... ')
        rxrot.move(0)
        # TODO: lock until movement is done.
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('Sliding Chopper : Move to SKY ... ')
        slider.move_sky()
        # TODO: lock until movement is done.
        self.stdout.write('ok')
        self.stdout.nextline()
        
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


class finalize(base.forest_script_base):
    method = 'finalize'
    ver = '2015.03.05'
    
    def run(self):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        self.operation_start()
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : System Finalize ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        sis = self.open_sis_biasbox()
        lo_sg = self.open_lo_sg()
        lo_att = self.open_lo_att()
        irr_sg = self.open_irr_sg()
        switch = self.open_switch()
        speana = self.open_speana()
        rxrot = self.open_rxrot()
        slider = self.open_slider()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('System Finalize')
        self.stdout.p('===============')
        
        self.stdout.write('SIS Bias : Set 0 mV ... ')
        sis.bias_set(0)
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('1st LO SG : Set -130 dBm ... ')
        lo_sg.power_set(-130)
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('1st LO SG : Set 10 GHz ... ')
        lo_sg.freq_set(10, 'GHz')
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('1st LO SG : Set output off ... ')
        lo_sg.output_off()
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('1st LO Att : Set max attenuation ... ')
        lo_att.bias_set(200)
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('IRR SG : Set output off ... ')
        irr_sg.output_off()
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('IF Switch : Set ch 1 ... ')
        switch.ch_set_all(1)
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('Speana : Preset ... ')
        speana.scpi_reset()
        self.stdout.write('ok')
        self.stdout.nextline()
                
        self.stdout.write('Rx Rotator : Move to 0 deg ... ')
        rxrot.move(0)
        # TODO: lock until movement is done.
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('Sliding Chopper : Move to R ... ')
        slider.move_r()
        # TODO: lock until movement is done.
        self.stdout.write('ok')
        self.stdout.nextline()
        
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


