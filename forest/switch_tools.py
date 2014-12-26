
import pymeasure

class switch(object):
    def __init__(self):
        com = pymeasure.ethernet('192.168.40.51', 5025)
        self.driver = pymeasure.Agilent.agilent_11713C(com)
        self.ch_check()
        pass
    
    def ch_check(self):
        """
        Check the using chnnel for each switch.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        < ch_list : list(int) : 1-4 >
            Return a list of ch using for each switch.
            ch is in 1-4.
        
        Examples
        ========
        >>> s.ch_check()
        [1, 2, 4, 1]
        """
        bank1 = self.driver.switch_open_query('101:110')
        bank2 = self.driver.switch_open_query('201:210')
        status = switch_status(bank1=bank1, bank2=bank2)
        self.status = status
        return status.switches

    def ch_set(self, ch, driver=1):
        """
        Set the using chnnel for a specified driver.
        
        Args
        ====
        < ch : int : 1-4 >
            Specify the ch to use. (1-4)
        
        < driver : int : 1-4 >
            Specify the driver to set. (1-4)
            default is 1.
        
        Returns
        =======
        Nothing
        
        Examples
        ========
        >>> s.ch_set(1)
        >>> s.ch_set(2, driver=2)
        """
        switches = self.ch_check()
        switches[driver-1] = ch
        new_status = switch_status(switches=switches)
        self.driver.switch_close_all()
        self.driver.switch_open(new_status.open_ch)
        return
    
    def ch_set_all(self, ch):
        """
        Set the using chnnel for each switches.
        
        Args
        ====
        < ch : int, or list of int : 1-4 >
            If <ch> is an int, all drivers will be set <ch>.
            
            If <ch> is a list, driver[i] will set ch[i].
            In this case, len(ch) should be 4.
        
        Returns
        =======
        Nothing
        
        Examples
        ========
        >>> s.ch_set_all(1)
        >>> s.ch_set_all([1, 2, 3, 4])
        """
        if type(ch) == int: ch = [ch]*4
        new_status = switch_status(switches=ch)
        self.driver.switch_close_all()
        self.driver.switch_open(new_status.open_ch)
        return
    
        

# ==============
# Helper Classes
# ==============

# Switch Status
# =============
class switch_status(object):
    switches = [0, 0, 0, 0]
    
    def __init__(self, bank1=None, bank2=None, switches=None):
        if bank1 is not None:
            self._set_by_bank(bank1, bank2)
        elif switches is not None:
            self._set_by_switches(switches)
            pass
        self._generate_open_ch()
        pass
    
    def __list__(self):
        return self.switches
    
    def _set_by_bank(self, bank1, bank2):
        self.bank1 = bank1
        self.bank2 = bank2
        
        def check(d):
            if sum(d)==0: return 0
            if sum(d)>1: return -1
            for i in range(len(d)):
                if d[i]==1: return i+1
                continue
            return
            
        self.switches[0] = check(bank1[:4])
        self.switches[1] = check(bank1[4:8])
        self.switches[2] = check(bank2[:4])
        self.switches[3] = check(bank2[4:8])
        return

    def _set_by_switches(self, switches):
        self.switches = switches
        
        def make_opens(ch):
            opens = [0, 0, 0, 0]
            if ch==0: return opens
            opens[ch-1] = 1
            return opens
            
        opens = [make_opens(ch) for ch in switches]
        self.bank1 = opens[0] + opens[1] + [0, 0]
        self.bank2 = opens[2] + opens[3] + [0, 0]
        return

    def _generate_open_ch(self):
        def generate(opens, bank):
            ch = []
            for i in range(len(opens)):
                if opens[i]==1: ch.append(bank*100 + i+1)
                continue
            return ch
            
        open_ch = []
        open_ch += generate(self.bank1, bank=1)
        open_ch += generate(self.bank2, bank=2)
        self.open_ch = open_ch
        return
