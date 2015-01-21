
import forest
import base

class sis_bias_set(base.forest_script_base):
    method = 'sis_bias_set'
    ver = '2015.01.21'
    
    def run(self, bias, beam, pol, dsbunit):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'bias': bias, 'beam': beam, 'pol': pol, 'dsbunit': dsbunit}
        argstxt = str(args)
        self.operation_start(argstxt)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Set SIS Bias')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        sis = self.open_sis_biasbox()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Set SIS Bias')
        self.stdout.p('============')
        self.stdout.p('bias = %f'%(bias))
        self.stdout.p('beam = %s'%(str(beam)))
        self.stdout.p('pol = %s'%(str(pol)))
        self.stdout.p('unit = %s'%(str(dsbunit)))
        self.stdout.nextline()
        
        self.stdout.write('SIS Bias : Set %f mV ... '%(bias))
        sis.bias_set(bias, beam=beam, pol=pol, dsbunit=dsbunit)
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
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return


