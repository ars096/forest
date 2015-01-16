
import forest
import base


class slider_move_r(base.forest_script_base):
    method = 'slider_move_r'
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
        self.stdout.p('FOREST : Move Slider R Position')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        slider = self.open_slider()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Move Slider')
        self.stdout.p('===========')
        
        self.stdout.write('Slider : Move to R ... ')
        slider.move_r()
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


class slider_move_sky(base.forest_script_base):
    method = 'slider_move_sky'
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
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Move Slider SKY Position')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        slider = self.open_slider()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Move Slider')
        self.stdout.p('===========')
        
        self.stdout.write('Slider : Move to SKY ... ')
        slider.move_sky()
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


class slider_move_org(base.forest_script_base):
    method = 'slider_move_org'
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
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Move Slider ORG Position')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        slider = self.open_slider()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Move Slider')
        self.stdout.p('===========')
        
        self.stdout.write('Slider : Clear alarms ... ')
        slider.clear_alarm()
        slider.clear_interlock()
        self.stdout.write('ok')
        self.stdout.nextline()
        
        self.stdout.write('Slider : Move to ORG ... ')
        slider.move_org()
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


class slider_move(base.forest_script_base):
    method = 'slider_move'
    ver = '2015.01.17'
    
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
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Move Slider')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        slider = self.open_slider()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('Move Slider')
        self.stdout.p('===========')
        
        self.stdout.write('Slider : Move to %d ... '%(target))
        slider.move(target)
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

