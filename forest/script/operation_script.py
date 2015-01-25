
import forest
import base


class start_observation(base.forest_script_base):
    method = 'Observation'
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
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Start Observation ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        self.stdout.p('When observation is end, please execute forest_end_observation.py.')
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        
        return


class end_observation(base.forest_script_base):
    method = 'stop_observation'
    ver = '2015.01.23'
    
    def run(self):
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : End Observation')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.operation_done()
        return


class end_operation(base.forest_script_base):
    method = 'end_operation'
    ver = '2015.01.23'
    
    def run(self):
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : End Operation')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Stop operation
        # --------------
        self.stdout.p('//// Operation is done. ////')
        self.operation_done()
        return


