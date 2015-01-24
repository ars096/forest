
import forest
import base


class rxrot_move_org(base.forest_script_base):
    method = 'rxrot_move_org'
    ver = '2015.01.23'
    
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
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Move RxRot ORG Position ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        rxrot = self.open_rxrot()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Move RxRot')
        self.stdout.p('==========')
        
        self.stdout.write('Rx Rotator : Move to 0 deg ... ')
        rxrot.move(0)
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
        slider.close()
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return

class rxrot_move(base.forest_script_base):
    method = 'rxrot_move'
    ver = '2015.01.23'
    
    def run(self, target):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Start operation
        # ---------------
        args = {'target': target}
        argstxt = str(args)
        self.operation_start(argstxt)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Move RxRot ORG Position ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        rxrot = self.open_rxrot()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Move RxRot')
        self.stdout.p('==========')
        
        self.stdout.write('Rx Rotator : Move to %.2f deg ... '%(target))
        rxrot.move(target)
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
        slider.close()
        """
        
        self.stdout.p('All devices are closed.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        
        return


