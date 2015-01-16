
import forest
import base


class initialize(base.forest_script_base):
    method = 'initialize'
    ver = '2015.01.16'
    
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
        
        # TODO: uncomment IRR SG
        """
        self.stdout.write('IRR SG : Set output off ... ')
        irr_sg.output_off()
        self.stdout.write('ok')
        self.stdout.nextline()
        """
        
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


