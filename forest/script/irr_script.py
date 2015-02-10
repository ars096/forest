
import os
import time
import numpy
import pylab
import matplotlib.ticker

import forest
import base


pylab.rcParams['font.size'] = 6


def irr_spec_plot(x, dcold, dhot, dsig_u, dsig_l, irr, savepath):
    name = os.path.basename(savepath)
    
    dmin = numpy.min([dcold, dhot, dsig_u, dsig_l]) - 2
    dmax = numpy.max([dcold, dhot, dsig_u, dsig_l]) + 5
    
    avcold = numpy.average(10**(dcold/10.), axis=-1)
    avhot = numpy.average(10**(dhot/10.), axis=-1)
    avcolddb = 10 * numpy.log10(avcold)
    avhotdb = 10 * numpy.log10(avhot)
    avy = 10 * numpy.log10(avcold / avhot)
    label = ['cold: %.1f dBm\nhot: %.1f dBm\nny: %.1f dB'%(_c, _h, _y)
             for _c, _h, _y in zip(avcolddb.ravel(), avhotdb.ravel(), avy.ravel())]
    
    fig1 = pylab.figure()
    ax1 = [fig1.add_subplot(4, 4, i+1) for i in range(16)]
    [_a.plot(x, _d, '-b') for _a, _d in zip(ax1, dcold.reshape((-1,461)))]
    [_a.plot(x, _d, '-r') for _a, _d in zip(ax1, dhot.reshape((-1,461)))]
    [_a.plot(x, _d, '-g') for _a, _d in zip(ax1, dsig_u.reshape((-1,461)))]
    [_a.plot(x, _d, '--g') for _a, _d in zip(ax1, dsig_l.reshape((-1,461)))]
    [_a.set_xlim(x[0], x[-1]) for _a in ax1]
    [_a.set_ylim(dmin, dmax) for _a in ax1]
    [_a.grid(True) for _a in ax1]
    [_a.text(0.1, 0.65, _l, transform=_a.transAxes) for _a, _l in zip(ax1, label)]
    [_a.set_xlabel('IF Freq. (MHz)', size=8) for i,_a in enumerate(ax1) if i/4>2]    
    [_a.set_ylabel('Power (dBm)', size=8) for i,_a in enumerate(ax1) if i%4==0]    
    fig1.suptitle(name, fontsize=10)
    fig1.savefig(savepath+'.raw.png')
    pylab.close(fig1)
    
    irrmin = None
    irrmax = None
    fig2 = pylab.figure()
    ax2 = [fig2.add_subplot(4, 4, i+1) for i in range(16)]
    [_a.plot(x, _d, '-k') for _a, _d in zip(ax2, irr.reshape((-1,461)))]
    [_a.set_xlim(x[0], x[-1]) for _a in ax2]
    [_a.set_ylim(irrmin, irrmax) for _a in ax2]
    [_a.grid(True) for _a in ax2]
    [_a.set_xlabel('IF Freq. (MHz)', size=8) for i,_a in enumerate(ax2) if i/4>2]    
    [_a.set_ylabel('IRR (dB)', size=8) for i,_a in enumerate(ax2) if i%4==0]    
    fig2.suptitle(name, fontsize=10)
    fig2.savefig(savepath+'.irr_spec.png')
    pylab.close(fig2)
    return

def irr_summary_plot(x, irr, dcold, dhot, thot, savepath):
    name = os.path.basename(savepath)
    
    irrmin = 0
    irrmax = 30
    
    tsysmin = 0
    tsysmax = 800

    avcold = numpy.average(10**(dcold/10.), axis=-1)
    avhot = numpy.average(10**(dhot/10.), axis=-1)
    tsys = forest.rsky(avhot, avcold, thot)
    
    fig = pylab.figure()
    ax = [fig.add_subplot(4, 4, i+1) for i in range(16)]
    ax2 = [_a.twinx() for _a in ax]
    [_a.plot(x, _d, 'k-o') for _a, _d in zip(ax, irr.reshape((-1,16)).T)]
    [_a.set_ylim(irrmin, irrmax) for _a in ax]
    [_a.grid(True) for _a in ax]
    [_a.set_xlabel('IF Freq. (GHz)', size=8) for i,_a in enumerate(ax) if i/4>2]    
    [_a.set_ylabel('IRR (dB)', size=8) for i,_a in enumerate(ax) if i%4==0]
    [_a.set_ytick_labels('') for i,_a in enumerate(ax) if i%4!=0]
    [_a.plot(x, _d, 'b-') for _a, _d in zip(ax2, tsys.reshape((-1,16)).T)]
    [_a.set_ylim(tsysmin, tsysmax) for _a in ax2]
    [_a.set_ylabel('Blue: Tsys (K)', size=8) for i,_a in enumerate(ax2) if i%4==3]
    [_a.set_ytick_labels('') for i,_a in enumerate(ax2) if i%4!=3]
    
    fig.suptitle(name, fontsize=10)
    fig.savefig(savepath)
    pylab.close(fig)
    return



class irr_with_if_freq_sweep(base.forest_script_base):
    method = 'irr_with_if_freq_sweep'
    ver = '2015.02.10'
    
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
        figpath = fpg('irr.fig.%s')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'if_start': if_start, 'if_stop': if_stop, 'if_step': if_step,
                'lo_freq': lo_freq, 'thot': thot}
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
        
        self.stdout.p('Speana : Set freq span 1 MHz.')
        sp.frequency_span_set(1, 'MHz')
        
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
        acquiretime = (sweeptime+0.07) * 5
        self.stdout.p('Speana : acquiretime = %.3f sec.'%(acquiretime))
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        freq = sp.sp[0].gen_xaxis()
        self.stdout.p('Save : %s'%(dataname + '.freq.npy'))
        numpy.save(datapath + '.freq.npy', freq)
        x = (freq - numpy.average(freq)) / 1e6
        
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
            ref_sg.freq_set((lo_freq-if_freq)/6., 'GHz')            
            
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
        
        
        self.stdout.p('Calc IRR')
        self.stdout.p('--------')
        dcold_db = dcold.reshape((-1, 4, 4, 461))
        dhot_db = dhot.reshape((-1, 4, 4, 461))
        dsig_l_db = dsig_l.reshape((-1, 4, 4, 461))
        dsig_u_db = dsig_u.reshape((-1, 4, 4, 461))

        dcold = 10**(dcold_db/10.)
        dhot = 10**(dhot_db/10.)
        dsig_l = 10**(dsig_l_db/10.)
        dsig_u = 10**(dsig_u_db/10.)
        
        dc_u = dcold[:,:2,:,:]
        dh_u = dhot[:,:2,:,:]
        dl_u = dsig_l[:,:2,:,:]
        du_u = dsig_u[:,:2,:,:]
        
        dc_l = dcold[:,2:,:,:]
        dh_l = dhot[:,2:,:,:]
        dl_l = dsig_l[:,2:,:,:]
        du_l = dsig_u[:,2:,:,:]
        
        
        M_u = du_u / du_l
        M_l = dl_l / dl_u
        
        dP_u = numpy.average(dh_u - dc_u, axis=-1)
        dP_l = numpy.average(dh_l - dc_l, axis=-1)
        
        M_dsb = (dP_u / dP_l)[:,:,:,None]
        
        R_u = M_u * (M_l * M_dsb - 1.) / (M_u - M_dsb)
        R_l = M_l * (M_u - M_dsb) / (M_l * M_dsb - 1.)
        
        IRR_u = 10 * numpy.log10(R_u)
        IRR_l = 10 * numpy.log10(R_l)
        
        IRR = numpy.concatenate([IRR_u, IRR_l], axis=1)

        self.stdout.p('Save : %s'%(dataname + '.IRR_spec.npy'))
        numpy.save(datapath + '.IRR_spec.npy', IRR)
        
        
        ind_sig_u = numpy.nanargmax(du_u, axis=-1)
        ind_sig_l = numpy.nanargmax(dl_l, axis=-1)
        x1, x2, x3 = numpy.indices(ind_sig_u.shape)
        p_IRR_u = IRR_u[x1, x2, x3, ind_sig_u]
        p_IRR_l = IRR_u[x1, x2, x3, ind_sig_l]
        p_IRR = numpy.concatenate([p_IRR_u, p_IRR_l], axis=1)
        
        self.stdout.p('Save : %s'%(dataname + '.IRR.npy'))
        numpy.save(datapath + '.IRR.npy', p_IRR)
        
        self.stdout.nextline()
        
        
        self.stdout.p('Plot')
        self.stdout.p('----')
        self.stdout.p('Save : %s'%(figname))
        [irr_spec_plot(x, _c, _h, _u, _l, _i, '%s.IF%.1fGHz'%(figpath, freq))
         for i, (_c, _h, _u, _l, _i, freq) 
         in enumerate(zip(dcold_db, dhot_db, dsig_u_db, dsig_l_db, IRR, if_list))]
        
        irr_summary_plot(if_list, p_IRR, dcold_db, dhot_db, thot, '%s.IRR.png'%(figpath))
        
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
        

