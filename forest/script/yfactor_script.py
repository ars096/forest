
import numpy
import pylab

import forest
import base


def tsys_plot(freq, dhot, dcold, tsys, save, suptitle):
    speana = ['SP:1', 'SP:2', 'SP:3', 'SP:4'] * 4 
    switch = ['SW:%d'%_ch for i in range(ax_x) for _ch in [1,2,3,4]]
    label = ['%s, %s'%(_sw, _sp) for _sw, _sp in zip(switch, speana)]
    
    freq_GHz = freq / 1e9
    
    if numpy.nanmin(tsys) < 200: tsys_max = 300
    elif numpy.nanmax(tsys) < 400: tsys_max = 500
    else: tsys_max = 1000
    dmin = numpy.nanmin(dcold) - 1
    dmax = numpy.nanmax(dhot) + 1
    
    fig = pylab.figure()
    fig.suptitle(suptitle, fontsize=11)
    ax = [fig.add_subplot(4, 4, i+1) for i in range(16)]
    ax2 = [_a.twinx() for _a in ax]
    [_a.plot(freq_GHz, _hot, 'r-') for _a, _hot in zip(ax, dhot)]
    [_a.plot(freq_GHz, _cold, 'b-') for _a, _cold in zip(ax, dcold)]
    [_a.plot(freq_GHz, _tsys, 'k+') for _a, _tsys in zip(ax2, tsys)]
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


class rsky_with_slider(base.forest_script_base):
    method = 'rsky_with_slider'
    ver = '2015.01.17'
    
    def run(self, f_start, f_stop, f_resbw, f_average, thot):
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
        hotdatapath = fpg('rsky.data.%s')
        hotdataname = os.path.basename(datapath)
        figpath = fpg('rsky.fig.%s.png')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'f_start': f_start, 'f_stop': f_stop, 'f_resbw': f_resbw,
                'f_average': f_average, 'thot': thot}
        argstxt = str(args)
        self.operation_start(argstxt, logfile=logpath)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : R-SKY with slider ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        slider = self.open_slider()
        sp = self.open_speana()
        sw = self.open_switch()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('R-SKY')
        self.stdout.p('=====')
        self.stdout.p('f_start = %f GHz'%(f_start))
        self.stdout.p('f_stop = %f GHz'%(f_stop))
        self.stdout.p('f_resbw = %f MHz'%(f_resbw))
        self.stdout.p('f_average = %d'%(f_average))
        self.stdout.p('thot = %f K'%(thot))
        self.stdout.nextline()
        
        self.stdout.p('Device configurations')
        self.stdout.p('---------------------')
        self.stdout.p('Speana : Set start freq %f GHz.'%(f_start))
        sp.frequency_start_set(f_start, 'GHz')
        
        self.stdout.p('Speana : Set stop freq %f GHz.'%(f_stop))
        sp.frequency_stop_set(f_stop, 'GHz')
        
        self.stdout.p('Speana : Set res. BW %f MHz.'%(f_resbw))
        sp.resolution_bw_set(f_resbw, 'MHz')
        
        self.stdout.p('Speana : Set average %d.'%(f_average))
        sp.average_set(f_average)
        sp.average_onoff_set('ON')
        sweeptime = sp.sweep_time_query()[0]
        acquiretime = sweeptime * f_average
        self.stdout.p('Speana : acquiretime = %.3f sec.'%(acquiretime))
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        freq = sp.sp[0].gen_xaxis()
        self.stdout.p('Save : %s'(dataname + '.freq.npy'))
        numpy.save(datapath + '.freq.npy', freq)
        
        self.stdout.nextline()
        
        
        dcold = []
        dhot = []
        
        self.stdout.p('Get SKY data')
        self.stdout.p('------------')
        self.stdout.p('Slider : Move to SKY.')
        slider.move_sky()
        
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
    
        dcold = numpy.array(dcold)
        self.stdout.p('Save : %s'%(dataname + '.cold.npy'))
        numpy.save(datapath + '.cold.npy', dcold)
        self.stdout.nextline()
        
        
        self.stdout.p('Get R data')
        self.stdout.p('----------')
        self.stdout.p('Slider : Move to R.')
        slider.move_r()
        
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
        
        dhot = numpy.array(dhot)
        self.stdout.p('Save : %s'%(dataname + '.hot.npy'))
        numpy.save(datapath + '.hot.npy', dhot)
        self.stdout.nextline()
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        self.stdout.p('Slider : Move to SKY.')
        slider.move_sky()

        self.stdout.nextline()
        
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
                  tsys.reshape([16,-1]), figpath, 'Tsys (%s)'%(ts))
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


class rsky_with_sis_bias_sweep(base.forest_script_base):
    method = 'rsky_with_sis_bias_sweep'
    ver = '2015.01.17'
    
    def run(self, start, stop, step, thot):
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
        hotdatapath = fpg('rsky.data.%s')
        hotdataname = os.path.basename(datapath)
        figpath = fpg('rsky.fig.%s.png')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'start': start, 'stop': stop, 'step': step, 'thot': thot}
        argstxt = str(args)        
        self.operation_start(argstxt, logfile=logpath)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : R-SKY with SIS Bias Sweep ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        sis = self.open_sis_biasbox()
        sp = self.open_speana()
        sw = self.open_switch()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('R-SKY')
        self.stdout.p('=====')
        self.stdout.p('start = %f'%(start))
        self.stdout.p('stop = %f'%(stop))
        self.stdout.p('step = %f'%(step))
        self.stdout.p('thot = %f K'%(thot))
        self.stdout.nextline()
        
        self.stdout.p('Device configurations')
        self.stdout.p('---------------------')
        self.stdout.p('Speana : Set center freq 8 GHz.')
        sp.frequency_center_set(8, 'GHz')
        
        self.stdout.p('Speana : Set span 0 Hz.')
        sp.frequency_span_set(0, 'Hz')
        
        self.stdout.p('Speana : Set Video BW 100 Hz.')
        sp.video_bw_set(100, 'Hz')
        
        self.stdout.p('Speana : Set reference level -30 dBm.')
        sp.reference_level_set(-30)
        
        self.stdout.p('Speana : Set scale 1 dB/div.')
        sp.scalediv_set(1)
        
        self.stdout.p('Speana : Set attenuation 0 dB.')
        sp.attenuation_set(0)
        
        self.stdout.p('Speana : Set average OFF.')
        sp.average_onoff_set('OFF')
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        self.stdout.p('SIS Bias : Set 0 mV.')
        sis.bias_set(0)
        
        self.stdout.nextline()
        
        
        self.stdout.p('Get R and SKY')
        self.stdout.p('-------------')
        
        spdata = []
        rsky_info = []
        tsys = []
        
        self.stdout.p('Generate input bias array ...')
        inp = numpy.arange(start, stop+step, step)
        self.stdout.p('inp : [%s %s %s ... %s %s %s]'%(
            inp[0], inp[1], inp[2], inp[-3], inp[-2], inp[-1]))
        
        inp = map(float, inp)
        
        for ch in [1,2,3,4]:
            self.stdout.p('IF Switch : Set ch %d.'%(ch))
            sw.ch_set_all(ch)
            time.sleep(0.05)
            
            for bias1 in inp:
                for bias2 in inp:
                    self.stdout.p('SIS Bias : Set bias1 = %.2f, bias2 = %.2f.'%(bias1, bias2))
                    sis.bias_set(bias1)
                    sis.bias_set(bias2, beam=1, pol='H', dsbunit=2)
                    sis.bias_set(bias2, beam=1, pol='V', dsbunit=2)
                    sis.bias_set(bias2, beam=2, pol='H', dsbunit=2)
                    sis.bias_set(bias2, beam=2, pol='V', dsbunit=2)
                    sis.bias_set(bias2, beam=3, pol='H', dsbunit=2)
                    sis.bias_set(bias2, beam=3, pol='V', dsbunit=2)
                    sis.bias_set(bias2, beam=4, pol='H', dsbunit=2)
                    sis.bias_set(bias2, beam=4, pol='V', dsbunit=2)
                    time.sleep(0.2)
                    
                    self.stdout.p('Speana : Aquire.')
                    d = sp.trace_data_query()
                    spdata.append(d[0])
                    spdata.append(d[1])
                    spdata.append(d[2])
                    spdata.append(d[3])
                    
                    self.stdout.p('Calc Tsys ...')
                    _tsys1, _info1 = forest.evaluate_rsky_from_rotating_chopper_data(d[1], thot)
                    _tsys2, _info2 = forest.evaluate_rsky_from_rotating_chopper_data(d[2], thot)
                    _tsys3, _info3 = forest.evaluate_rsky_from_rotating_chopper_data(d[3], thot)
                    _tsys4, _info4 = forest.evaluate_rsky_from_rotating_chopper_data(d[4], thot)
                    tsys.append(_tsys1)
                    tsys.append(_tsys2)
                    tsys.append(_tsys3)
                    tsys.append(_tsys4)
                    rsky_info.append(_info1)
                    rsky_info.append(_info2)
                    rsky_info.append(_info3)
                    rsky_info.append(_info4)
                    continue
                continue            
            continue
        
        spdata = numpy.array(spdata)
        tsys = numpy.array(tsys)
        rsky_info = numpy.array(rsky_info)
        
        self.stdout.p('Save : %s'%(dataname + '.spdata.npy'))
        numpy.save(dataname + '.spdata.npy', spdata)
        
        self.stdout.p('Save : %s'%(dataname + '.tsys.npy'))
        numpy.save(dataname + '.tsys.npy', tsys)
        
        self.stdout.p('Save : %s'%(dataname + '.info.npy'))
        numpy.save(dataname + '.info.npy', rsky_info)

        self.stdout.nextline()
        
        #
        # Plotting part
        #
        
        
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


