
import forest
import base


class lo_freq_set(base.forest_script_base):
    method = 'LO_freq_set'
    ver = '2015.01.17'
    
    def run(self, freq, unit='GHz'):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'freq': freq, 'unit': unit}
        argstxt = str(args)
        self.operation_start(argstxt)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Set 1st LOs Frequencies')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        lo_sg = self.open_lo_sg()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Set Frequencies')
        self.stdout.p('===============')
        
        self.stdout.write('1st LO SG : Set %.10f %s ... '%(freq, unit))
        lo_sg.freq_set(freq, unit)
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
        lo_sg.close()
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return


class lo_power_set(base.forest_script_base):
    method = 'LO_power_set'
    ver = '2015.01.17'
    
    def run(self, power):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'power': power}
        argstxt = str(args)
        self.operation_start(argstxt)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Set 1st LOs Output Powers ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        lo_sg = self.open_lo_sg()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Set Output Powers')
        self.stdout.p('=================')
        
        self.stdout.write('1st LO SG : Set %f dBm ... '%(power))
        lo_sg.power_set(power, 'dBm')
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
        lo_sg.close()
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return


class lo_output_off(base.forest_script_base):
    method = 'LO_output_off'
    ver = '2015.01.17'
    
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
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Set 1st LOs Output OFF')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        lo_sg = self.open_lo_sg()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Set RF Output OFF')
        self.stdout.p('=================')
        
        self.stdout.write('1st LO SG : Set output off ... ')
        lo_sg.output_off()
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
        lo_sg.close()
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return


class lo_output_on(base.forest_script_base):
    method = 'LO_output_on'
    ver = '2015.01.17'
    
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
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Set 1st LOs Output ON')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        lo_sg = self.open_lo_sg()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Set RF Output ON')
        self.stdout.p('================')
        
        self.stdout.write('1st LO SG : Set output on ... ')
        lo_sg.output_on()
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
        lo_sg.close()
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return

