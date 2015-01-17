
import forest
import base


class lo_att_set(base.forest_script_base):
    method = 'LO_att_set'
    ver = '2015.01.17'
    
    def run(self, bias, beam, pol):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'bias': bias, 'beam': beam, 'pol': pol}
        argstxt = str(args)
        self.operation_start(argstxt)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Set 1st LO Attenuation Levels ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        lo_att = self.open_lo_att()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Set Attenuation Levels')
        self.stdout.p('======================')
        self.stdout.p('bias = %f'%(bias))
        self.stdout.p('beam = %d'%(beam))
        self.stdout.p('pol = %s'%(pol))
        self.stdout.nextline()
        
        self.stdout.write('1st LO Att : Set %f mA ... '%(bias))
        lo_att.bias_set(bias, beam=beam, pol=pol)
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


