
import pyinterface

class slider(object):
    pos_sky = 0
    pos_sig = 19000
    pos_r = 25000
    
    speed = 50000
    low_speed = 5
    acc = 1000
    dec = 1000
    
    def __init__(self, move_org=True):
        self.mtr = pyinterface.create_gpg7204(1)
        if move_org: self.move_org()
        pass
        
    def move_org(self):
        """
        Move to ORG position.
        
        NOTE: This method will be excuted in instantiation.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_org()
        """
        self.mtr.do_output(3)
        self.mtr.set_org()
        return

    def _move(self, dist, lock):
        pos = self.mtr.get_position()
        if pos == dist: return
        diff = dist - pos
        if lock: self.mtr.move_with_lock(self.speed, diff, self.low_speed,
                                         self.acc, self.dec)
        else: self.mtr.move(self.speed, diff, self.low_speed, self.acc,
                            self.dec)
        return
    
    def move_r(self, lock=True):
        """
        Move to R position.
        
        NOTE: If the slider is already at R position, it doesn't move.
        
        Args
        ====
        < lock : bool :  > (optional)
            If <lock> is False, the method returns immediately.
            Otherwise, it returns after the slider stopped.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_r()
        """
        self._move(self.pos_r, lock)
        return
    
    def move_sky(self, lock=True):
        """
        Move to SKY position.
        
        NOTE: If the slider is already at SKY position, it doesn't move.
        
        Args
        ====
        < lock : bool :  > (optional)
            If <lock> is False, the method returns immediately.
            Otherwise, it returns after the slider stopped.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_sky()
        """
        self._move(self.pos_sky, lock)
        return
    
    def move_sig(self, lock=True):
        """
        Move to SIG position.
        
        NOTE: If the slider is already at SIG position, it doesn't move.
        
        Args
        ====
        < lock : bool :  > (optional)
            If <lock> is False, the method returns immediately.
            Otherwise, it returns after the slider stopped.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_sig()
        """
        self._move(self.pos_sig, lock)
        return
    
    def unlock_brake(self):
        """
        Unlock the electromagnetic brake of the slider.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.unlock_brake()
        """
        self.mtr.do_output(2, 0)
        msg = '!! Electromagnetic brake is now UNLOCKED !!'
        print('*'*len(msg))
        print(msg)
        print('*'*len(msg))
        raw_input(' please ENTER to LOCK the brake... ')
        self.mtr.do_output(0)
        print('')
        print('')
        print('!! CAUTION !!')
        print('-------------')
        print('You must execute s.move_org() method, before executing any "move_**" method.')
        print('')
        return
    
    def clear_alarm(self):
        """
        Clear the alarm.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.clear_alarm()
        """
        self.mtr.do_output(1)
        return
