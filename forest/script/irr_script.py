
import os
import time
import numpy
import pylab
import matplotlib.ticker

import forest
import base


def tsys_plot(freq, dhot, dcold, tsys, save, suptitle, smooth=1):
    speana = ['SP:1', 'SP:2', 'SP:3', 'SP:4'] * 4 
    switch = ['SW:%d'%_ch for i in [1,2,3,4] for _ch in [1,2,3,4]]
    label = ['%s, %s'%(_sw, _sp) for _sw, _sp in zip(switch, speana)]
    
    freq_GHz = freq / 1e9
    
    if numpy.nanmin(tsys) < 200: tsys_max = 500
    elif numpy.nanmax(tsys) < 400: tsys_max = 800
    else: tsys_max = 1300
    dmin = numpy.nanmin(dcold) - 1
    dmax = numpy.nanmax(dhot) + 1
    
    c = numpy.ones(smooth) / float(smooth)
    
    fig = pylab.figure()
    fig.suptitle(suptitle, fontsize=11)
    ax = [fig.add_subplot(4, 4, i+1) for i in range(16)]
    ax2 = [_a.twinx() for _a in ax]
    [_a.plot(freq_GHz, numpy.convolve(_hot, c, mode='same'), 'r-') for _a, _hot in zip(ax, dhot)]
    [_a.plot(freq_GHz, numpy.convolve(_cold, c, mode='same'), 'b-') for _a, _cold in zip(ax, dcold)]
    [_a.plot(freq_GHz, numpy.convolve(_tsys, c, mode='same'), 'k.', ms=3) for _a, _tsys in zip(ax2, tsys)]
    [_a.text(0.08, 0.84, _l, transform=_a.transAxes) for _a, _l in zip(ax, label)]
    [_a.set_xlim(freq_GHz.min(), freq_GHz.max()) for _a in ax]
    [_a.set_xlim(freq_GHz.min(), freq_GHz.max()) for _a in ax2]
    [_a.set_ylim(dmin, dmax) for _a in ax]
    [_a.set_ylim(0, tsys_max) for _a in ax2]
    [_a.set_xlabel('Frequency (GHz)') for i, _a in enumerate(ax) if i/4>=3]
    [_a.set_ylabel('Power (dBm)') for i, _a in enumerate(ax) if i%4==0]
    [_a.set_yticklabels('') for i, _a in enumerate(ax) if i%4!=0]
    [_a.set_ylabel('Tsys (K)') for i, _a in enumerate(ax2) if i%4==3]
    [_a.set_yticklabels('') for i, _a in enumerate(ax2) if i%4!=3]
    [_a.grid(True) for _a in ax]
    fig.savefig(save)
    
    pylab.close(fig)
    return


class irr_with_if_freq_sweep(base.forest_script_base):
    method = 'irr_with_if_freq_sweep'
    ver = '2015.02.09'
    
    def run(self, lo_freq, if_start, if_stop, if_step, thot):
        # Initialization Section
        # ======================
        
        # Check other operation
        # ---------------------
        self.check_other_operation()
        
        # Generate file path
        # ------------------
        fpg = forest.filepath_generator(self.method)
        savedir = fpg(' ')
        logpath = fpg('log.%s.txt')
        logname = os.path.basename(logpath)
        datapath = fpg('irr.data.%s')
        dataname = os.path.basename(datapath)
        figpath = fpg('irr.fig.%s.png')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'if_start': if_start, 'if_stop': if_stop, 'if_step': if_step,
                'lo_freq' lo_freq, 'thot': thot}
        argstxt = str(args)
        self.operation_start(argstxt, logfile=logpath)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : IRR with IF Freq sweep')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        slider = self.open_slider()
        sp = self.open_speana()
        sw = self.open_switch()
        lo_sg = self.open_lo_sg()
        ref_sg = self.open_irr_sg()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('IRR')
        self.stdout.p('===')
        self.stdout.p('lo_freq = %f GHz'%(lo_freq))
        self.stdout.p('if_start = %f GHz'%(if_start))
        self.stdout.p('if_stop = %f GHz'%(if_stop))
        self.stdout.p('if_step = %f MHz'%(if_step))
        self.stdout.p('thot = %f K'%(thot))
        self.stdout.nextline()
        
        self.stdout.p('Device configurations')
        self.stdout.p('---------------------')
        
        self.stdout.p('1st LO SG : Set %f GHz.'%(lo_freq/6.))
        lo_sg.freq_set(lo_freq/6., 'GHz')
        
        self.stdout.p('1st LO SG : Set 18 dBm.')
        lo_sg.power_set(18)
                
        self.stdout.p('1st LO SG : Set output on.')
        lo_sg.output_on()
        
        self.stdout.p('IRR Ref SG : Set %f GHz.'%((lo_freq+if_start)/6.))
        ref_sg.freq_set((lo_freq+if_start)/6., 'GHz')
        
        self.stdout.p('IRR Ref SG : Set output off.')
        ref_sg.output_off()
        
        
        self.stdout.p('Speana : Preset.')
        sp.scpi_reset()
        
        self.stdout.p('Speana : Set freq span 10 MHz.')
        sp.frequency_span_set(10, 'MHz')
        
        self.stdout.p('Speana : Set center freq %f GHz.'%(if_start))
        sp.frequency_center_set(if_start, 'GHz')
        
        self.stdout.p('Speana : Set res. BW 1 kHz.')
        sp.resolution_bw_set(1, 'kHz')
        
        self.stdout.p('Speana : Set attenuation 0 dB.')
        sp.attenuation_set(0)
        
        self.stdout.p('Speana : Set average 5.')
        sp.average_set(5)
        sp.average_onoff_set('ON')
        sweeptime = sp.sweep_time_query()[0]
        acquiretime = sweeptime * 5
        self.stdout.p('Speana : acquiretime = %.3f sec.'%(acquiretime))
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        freq = sp.sp[0].gen_xaxis()
        self.stdout.p('Save : %s'%(dataname + '.freq.npy'))
        numpy.save(datapath + '.freq.npy', freq)
        
        self.stdout.nextline()
        
        if_list = numpy.arange(if_start, if_stop + if_step, if_step)
        
        
        dcold = []
        dhot = []
        dsig_u = []
        dsig_l = []
        
        self.stdout.p('Get SKY data')
        self.stdout.p('------------')
        self.stdout.p('Slider : Move to SKY.')
        slider.move_sky()
        
        for if_freq in if_list:
            self.stdout.p('Speana : Set center freq %f GHz.'%(if_freq))
            sp.frequency_center_set(if_freq, 'GHz')
            
            for ch in [1,2,3,4]:
                self.stdout.p('IF Switch : Set ch %d.'%(ch))
                sw.ch_set_all(ch)
                time.sleep(0.05)
                
                self.stdout.p('Speana : Acquire. waittime=%.1f'%(acquiretime))
                sp.average_restart()
                time.sleep(acquiretime)
                _d = sp.trace_data_query()
                dcold.append(_d)
                continue
                
            continue
        
        dcold = numpy.array(dcold)
        self.stdout.p('Save : %s'%(dataname + '.cold.npy'))
        numpy.save(datapath + '.cold.npy', dcold)
        self.stdout.nextline()
        

        self.stdout.p('Get R data')
        self.stdout.p('----------')
        self.stdout.p('Slider : Move to R.')
        slider.move_r()
        
        for if_freq in if_list:
            self.stdout.p('Speana : Set center freq %f GHz.'%(if_freq))
            sp.frequency_center_set(if_freq, 'GHz')
            
            for ch in [1,2,3,4]:
                self.stdout.p('IF Switch : Set ch %d.'%(ch))
                sw.ch_set_all(ch)
                time.sleep(0.05)
                
                self.stdout.p('Speana : Acquire. waittime=%.1f'%(acquiretime))
                sp.average_restart()
                time.sleep(acquiretime)
                _d = sp.trace_data_query()
                dhot.append(_d)
                continue
                
            continue
        
        dhot = numpy.array(dhot)
        self.stdout.p('Save : %s'%(dataname + '.hot.npy'))
        numpy.save(datapath + '.hot.npy', dhot)
        self.stdout.nextline()
        
        
        self.stdout.p('Get SIG data')
        self.stdout.p('------------')
        self.stdout.p('Slider : Move to R.')
        slider.move_r()
        self.stdout.p('IRR Ref SG : Set output on.')
        ref_sg.output_on()
        
        
        for if_freq in if_list:
            self.stdout.p('INFO : IF freq = %f GHz.'%(if_freq))
            self.stdout.p('INFO : (Upper Side Band)')            
            self.stdout.p('IRR Ref SG : Set %f GHz.'%((lo_freq+if_freq)/6.))
            ref_sg.freq_set((lo_freq+if_freq)/6., 'GHz')            
            
            self.stdout.p('Speana : Set center freq %f GHz.'%(if_freq))
            sp.frequency_center_set(if_freq, 'GHz')
            
            for ch in [1,2,3,4]:
                self.stdout.p('IF Switch : Set ch %d.'%(ch))
                sw.ch_set_all(ch)
                time.sleep(0.05)
                
                self.stdout.p('Speana : Acquire. waittime=%.1f'%(acquiretime))
                sp.average_restart()
                time.sleep(acquiretime)
                _d = sp.trace_data_query()
                dsig_u.append(_d)
                continue
            
            self.stdout.p('INFO : (Lower Side Band)')
            self.stdout.p('IRR Ref SG : Set %f GHz.'%((lo_freq-if_freq)/6.))
            ref_sg.freq_set((lo_freq+if_freq)/6., 'GHz')            
            
            for ch in [1,2,3,4]:
                self.stdout.p('IF Switch : Set ch %d.'%(ch))
                sw.ch_set_all(ch)
                time.sleep(0.05)
                
                self.stdout.p('Speana : Acquire. waittime=%.1f'%(acquiretime))
                sp.average_restart()
                time.sleep(acquiretime)
                _d = sp.trace_data_query()
                dsig_l.append(_d)
                continue
                
            continue
        
        dsig_u = numpy.array(dsig_u)
        dsig_l = numpy.array(dsig_l)
        self.stdout.p('Save : %s'%(dataname + '.dsig_u.npy'))
        self.stdout.p('Save : %s'%(dataname + '.dsig_l.npy'))
        numpy.save(datapath + '.dsig_u.npy', dsig_u)
        numpy.save(datapath + '.dsig_l.npy', dsig_l)
        self.stdout.nextline()
        
        
        self.stdout.p('IRR Ref SG : Set output off.')
        ref_sg.output_off()
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        self.stdout.p('Slider : Move to SKY.')
        slider.move_sky()
        
        self.stdout.nextline()
        
        """
        self.stdout.p('Calc Tsys')
        self.stdout.p('---------')
        tsys = forest.rsky_dB(dhot, dcold, thot)
        self.stdout.p('Save : %s'%(dataname + '.Tsys.npy'))
        numpy.save(datapath + '.Tsys.npy', tsys)
        self.stdout.nextline()
        
        self.stdout.p('Plot')
        self.stdout.p('----')
        self.stdout.p('Save : %s'%(figname))
        tsys_plot(freq, dhot.reshape([16,-1]), dcold.reshape([16,-1]),
                  tsys.reshape([16,-1]), figpath, 'Tsys (%s)'%(ts), smooth=11)
        self.stdout.nextline()
        """
        
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


