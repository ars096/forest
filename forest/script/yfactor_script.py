
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
        datapath = fpg('rsky.data.%s')
        dataname = os.path.basename(datapath)
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
        self.stdout.p('Speana : Preset.')
        sp.scpi_reset()
        
        self.stdout.p('Speana : Set start freq %f GHz.'%(f_start))
        sp.frequency_start_set(f_start, 'GHz')
        
        self.stdout.p('Speana : Set stop freq %f GHz.'%(f_stop))
        sp.frequency_stop_set(f_stop, 'GHz')
        
        self.stdout.p('Speana : Set res. BW %f MHz.'%(f_resbw))
        sp.resolution_bw_set(f_resbw, 'MHz')
        
        self.stdout.p('Speana : Set attenuation 0 dB.')
        sp.attenuation_set(0)
        
        self.stdout.p('Speana : Set average %d.'%(f_average))
        sp.average_set(f_average)
        sp.average_onoff_set('ON')
        sweeptime = sp.sweep_time_query()[0]
        acquiretime = sweeptime * f_average
        self.stdout.p('Speana : acquiretime = %.3f sec.'%(acquiretime))
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        freq = sp.sp[0].gen_xaxis()
        self.stdout.p('Save : %s'%(dataname + '.freq.npy'))
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
                  tsys.reshape([16,-1]), figpath, 'Tsys (%s)'%(ts), smooth=11)
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
    ver = '2015.01.23'
    
    def run(self, step, thot, plot_tsys_min, plot_tsys_max):
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
        datapath = fpg('rsky.data.%s')
        dataname = os.path.basename(datapath)
        figpath = fpg('rsky.fig.%s')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'thot': thot}
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
        self.stdout.p('thot = %f K'%(thot))
        self.stdout.nextline()
        
        self.stdout.p('Device configurations')
        self.stdout.p('---------------------')
        self.stdout.p('Speana : Preset.')
        sp.scpi_reset()

        self.stdout.p('Speana : Set center freq 8 GHz.')
        sp.frequency_center_set(8, 'GHz')
        
        self.stdout.p('Speana : Set span 0 Hz.')
        sp.frequency_span_set(0, 'Hz')
        
        self.stdout.p('Speana : Set res. BW 3 MHz.')
        sp.resolution_bw_set(3, 'MHz')
        
        self.stdout.p('Speana : Set Video BW 100 Hz.')
        sp.video_bw_set(100, 'Hz')
        
        self.stdout.p('Speana : Set reference level -55 dBm.')
        sp.reference_level_set(-55)
        
        self.stdout.p('Speana : Set scale 1 dB/div.')
        sp.scalediv_set(1)
        
        self.stdout.p('Speana : Set attenuation 0 dB.')
        sp.attenuation_set(0)
        
        self.stdout.p('Speana : Set sweep time 0.1 sec.')
        sp.sweep_time_set(0.1)
        
        self.stdout.p('Speana : Set average OFF.')
        sp.average_onoff_set('OFF')
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        self.stdout.p('SIS Bias : Set 0 mV.')
        sis.bias_set(0)
        
        self.stdout.nextline()


        self.stdout.p('Prepare Sweep Bias Set')
        self.stdout.p('----------------------')
        bias_3j = [float(_d) for _d in numpy.arange(6.0, 8.01, step)]
        bias_4j = [float(_d) for _d in numpy.arange(8.0, 10.01, step)]
        #bias_3j = [float(_d) for _d in numpy.arange(6.0, 8.01, 0.2)]
        #bias_4j = [float(_d) for _d in numpy.arange(8.0, 10.01, 0.2)]
        #bias_3j = [float(_d) for _d in numpy.arange(6.0, 8.01, 1)]   # for test 
        #bias_4j = [float(_d) for _d in numpy.arange(8.0, 10.01, 1)]  # for test
        biasx_num = len(bias_3j)
        
        bias_3j1 = [_x for _x in bias_3j for _y in bias_3j] 
        bias_3j2 = [_y for _x in bias_3j for _y in bias_3j] 
        bias_4j1 = [_x for _x in bias_4j for _y in bias_4j] 
        bias_4j2 = [_y for _x in bias_4j for _y in bias_4j] 
        bias_num = len(bias_3j1)
        
        sisp = forest.load_sis_config()
        j_type = []
        sweep_data = []
        beam_pol = []
        for unit in sorted(sisp.keys()):
            _j_type = sisp[unit]['J-type']
            j_type.append(_j_type)
            beam = sisp[unit]['beam']
            pol = sisp[unit]['pol']
            self.stdout.p('Junction Type of %s is %s.'%(unit, _j_type))
            if _j_type == '3J':
                sweep_data.append([bias_3j1, bias_3j2])
            elif _j_type == '4J':
                sweep_data.append([bias_4j1, bias_4j2])
            else: 
                sweep_data.append([bias_3j1, bias_3j2])
                pass
            beam_pol.append([beam, pol])
            continue
            
        self.stdout.p('Sorting sweep data by ch.')
        biasch = forest.biasbox_ch_mapper()
        sweep_data_ch = biasch.sort_sweep_data_by_ch(sweep_data, beam_pol)
        
        self.stdout.p('SIS Bias : Set sweep data.')
        sis.bias_series_set(sweep_data_ch)
        
        self.stdout.nextline()

        
        self.stdout.p('Get R and SKY')
        self.stdout.p('-------------')
        
        spdata = []
        bias_ret = []
        rsky_info = []
        tsys = []
        
        for ch in [1,2,3,4]:
            self.stdout.p('IF Switch : Set ch %d.'%(ch))
            sw.ch_set_all(ch)
            time.sleep(0.1)
            
            for i, (b31, b32, b41, b42) in enumerate(zip(bias_3j1, bias_3j2, bias_4j1, bias_4j2)):
                self.stdout.p('SIS Bias : Set 3J = %.2f, %.2f; 4J = %.2f, %.2f. [%d/%d]'%(
                    b31, b32, b41, b42, i, bias_num))
                sis.bias_series_next()
                
                time.sleep(0.01)
                
                self.stdout.p('Speana : Average restart.')                
                sp.average_restart()
                
                self.stdout.p('Wait 0.1 sec.')
                time.sleep(0.13)
                
                self.stdout.p('SIS Bias : Get biases.')
                sis_vi = sis.bias_get()
                bias_ret.append(sis_vi)
                
                self.stdout.p('Speana : Get spectra.')
                d = sp.trace_data_query()
                spdata.append(d[0])
                spdata.append(d[1])
                spdata.append(d[2])
                spdata.append(d[3])
                
                self.stdout.p('Calc Tsys ...')
                _tsys1, _info1 = forest.evaluate_rsky_from_rotating_chopper_data(d[0], thot)
                _tsys2, _info2 = forest.evaluate_rsky_from_rotating_chopper_data(d[1], thot)
                _tsys3, _info3 = forest.evaluate_rsky_from_rotating_chopper_data(d[2], thot)
                _tsys4, _info4 = forest.evaluate_rsky_from_rotating_chopper_data(d[3], thot)
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
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        self.stdout.p('SIS Bias : Set 0 mV.')
        sis.bias_set(0)
        
        spdata = numpy.array(spdata)
        bias_ret = numpy.array(bias_ret)
        tsys = numpy.array(tsys)
        rsky_info = numpy.array(rsky_info, dtype=object)
        
        self.stdout.p('Save : %s'%(dataname + '.spdata.npy'))
        numpy.save(datapath + '.spdata.npy', spdata)
        
        self.stdout.p('Save : %s'%(dataname + '.bias.npy'))
        numpy.save(datapath + '.bias.npy', bias_ret)
        
        self.stdout.p('Save : %s'%(dataname + '.tsys.npy'))
        numpy.save(datapath + '.tsys.npy', tsys)
        
        self.stdout.p('Save : %s'%(dataname + '.info.npy'))
        numpy.save(datapath + '.info.npy', rsky_info)

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
        
        
        
        # Plotting 
        # --------
        #self.stdout.p('Plot')
        #self.stdout.p('----')
        print('Plot')
        print('----')
        
        pylab.rcParams['image.interpolation'] = 'none'
        pylab.rcParams['image.origin'] = 'lower'
        pylab.rcParams['font.size'] = 8
        
        # --
        
        tshape = (4, biasx_num, biasx_num, 4)
        tsys_reshape = tsys.reshape(tshape)
        tsys_swap = numpy.swapaxes(tsys_reshape, 1, 3)
        tsys_plot = tsys_swap.reshape([16, biasx_num, biasx_num])
        
        
        delt3 = (bias_3j[1] - bias_3j[0]) / 2.
        ext3 = [bias_3j[0] - delt3, bias_3j[-1] + delt3, bias_3j[0] - delt3, bias_3j[-1] + delt3]
        
        delt4 = (bias_4j[1] - bias_4j[0]) / 2.
        ext4 = [bias_4j[0] - delt4, bias_4j[-1] + delt4, bias_4j[0] - delt4, bias_4j[-1] + delt4]
        
        extentions = []
        for _jt in j_type:
            if _jt == '3J' :
                extentions.append(ext3)
                extentions.append(ext3)
            elif _jt == '4J':
                extentions.append(ext4)
                extentions.append(ext4)
            else:
                extentions.append(ext3)
                extentions.append(ext3)
                pass
            continue
        
            
        cbarticks = range(100, 1001, 100)

        #self.stdout.p('Plot : %s.tsysmap.png'%(figname))
        print('Plot : %s.tsysmap.png'%(figname))
        
        fig = pylab.figure()
        ax = [fig.add_subplot(4, 4, i+1) for i in range(16)]
        im = [_a.imshow(_t, extent=_ex,  vmin=plot_tsys_min, vmax=plot_tsys_max) 
              for _a, _t, _ex in zip(ax, tsys_plot, extentions)]
        [fig.colorbar(_im, ax=_a, ticks=[]) for i, (_im, _a) in enumerate(zip(im, ax)) if i%4 != 3]
        [fig.colorbar(_im, ax=_a, ticks=cbarticks) for i, (_im, _a) in enumerate(zip(im, ax)) if i%4 == 3]
        [_a.set_xlabel('Bias1 (mV)') for i, _a in enumerate(ax) if i/4 > 2]
        [_a.set_ylabel('Bias2 (mV)') for i, _a in enumerate(ax) if i%4 == 0]
        [_a.set_ylabel('Bias2 (mV)') for i, _a in enumerate(ax) if i%4 == 0]
        fig.savefig(figpath + '.tsysmap.png')
        pylab.close(fig)        
        
        
        # --
        
        sshape = (4, biasx_num, biasx_num, 4, -1)
        spdata_reshape = spdata.reshape(sshape)
        spdata_swap = numpy.swapaxes(spdata_reshape, 1, 3)
        spdata_plot = spdata_swap.reshape((16, biasx_num * biasx_num, -1))
        
        
        for ch, d in enumerate(spdata_plot):
            #self.stdout.p('Plot : %s.speana.%02d.png'%(figname, ch))
            print('Plot : %s.speana.%02d.png'%(figname, ch))

            loc = matplotlib.ticker.MultipleLocator(1)
            
            fig = pylab.figure()
            ax = [fig.add_subplot(biasx_num, biasx_num, i+1) for i in range(biasx_num * biasx_num)]
            [_a.plot(_d) for _a, _d in zip(ax, d)]
            [_a.set_xticklabels('') for _a in ax]
            [_a.set_yticklabels('') for _a in ax]
            [_a.yaxis.set_major_locator(loc) for _a in ax]
            [_a.grid(True) for _a in ax]
            fig.savefig(figpath + '.speana.%02d.png'%(ch))
            pylab.close(fig)
            continue

        #self.stdout.nextline()
        print('')
        
        print('//// plotting is done. ////')
        
        return


class rsky_with_lo_att_sweep(base.forest_script_base):
    method = 'rsky_with_lo_att_sweep'
    ver = '2015.01.23'
    
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
        datapath = fpg('rsky.data.%s')
        dataname = os.path.basename(datapath)
        figpath = fpg('rsky.fig.%s')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'start': start, 'stop': stop, 'step': step, 'thot': thot}
        argstxt = str(args)        
        self.operation_start(argstxt, logfile=logpath)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : R-SKY with LO Att Sweep ')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        lo_att = self.open_lo_att()
        sp = self.open_speana()
        sw = self.open_switch()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        self.stdout.p('R-SKY')
        self.stdout.p('=====')
        self.stdout.p('start = %f mA'%(start))
        self.stdout.p('stop = %f mA'%(stop))
        self.stdout.p('step = %f mA'%(step))
        self.stdout.p('thot = %f K'%(thot))
        self.stdout.nextline()
        
        self.stdout.p('Device configurations')
        self.stdout.p('---------------------')
        self.stdout.p('Speana : Preset.')
        sp.scpi_reset()

        self.stdout.p('Speana : Set center freq 5.5 GHz.')
        sp.frequency_center_set(5.5, 'GHz')
        
        self.stdout.p('Speana : Set span 0 Hz.')
        sp.frequency_span_set(0, 'Hz')
        
        self.stdout.p('Speana : Set res. BW 3 MHz.')
        sp.resolution_bw_set(3, 'MHz')
        
        self.stdout.p('Speana : Set Video BW 100 Hz.')
        sp.video_bw_set(100, 'Hz')
        
        self.stdout.p('Speana : Set reference level -55 dBm.')
        sp.reference_level_set(-55)
        
        self.stdout.p('Speana : Set scale 1 dB/div.')
        sp.scalediv_set(1)
        
        self.stdout.p('Speana : Set attenuation 0 dB.')
        sp.attenuation_set(0)
        
        self.stdout.p('Speana : Set sweep time 0.1 sec.')
        sp.sweep_time_set(0.1)
        
        self.stdout.p('Speana : Set average OFF.')
        sp.average_onoff_set('OFF')
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        self.stdout.p('LO Att : Set 0 mV.')
        lo_att.bias_set(0)
        
        self.stdout.nextline()


        self.stdout.p('Create sweep data.')
        sweep_data = numpy.arange(start, stop+step, step)
        sweep_num = len(sweep_data)
        
        self.stdout.nextline()
        
        
        self.stdout.p('Get R and SKY')
        self.stdout.p('-------------')
        
        spdata = []
        rsky_info = []
        tsys = []
        
        for ch in [1,2,3,4]:
            self.stdout.p('IF Switch : Set ch %d.'%(ch))
            sw.ch_set_all(ch)
            time.sleep(0.1)
            
            for i, _att in enumerate(sweep_data):
                self.stdout.p('LO Att : Set bias %.2f mA. [%d/%d]'%(_att, i, sweep_num))
                lo_att.bias_set(_att)

                self.stdout.p('Wait 2 sec...')
                time.sleep(2)
                
                self.stdout.p('Speana : Average restart.')                
                sp.average_restart()
                
                self.stdout.p('Wait 0.15 sec.')
                time.sleep(0.15)
                
                self.stdout.p('Speana : Get spectra.')
                d = sp.trace_data_query()
                spdata.append(d[0])
                spdata.append(d[1])
                spdata.append(d[2])
                spdata.append(d[3])
                
                self.stdout.p('Calc Tsys ...')
                _tsys1, _info1 = forest.evaluate_rsky_from_rotating_chopper_data(d[0], thot)
                _tsys2, _info2 = forest.evaluate_rsky_from_rotating_chopper_data(d[1], thot)
                _tsys3, _info3 = forest.evaluate_rsky_from_rotating_chopper_data(d[2], thot)
                _tsys4, _info4 = forest.evaluate_rsky_from_rotating_chopper_data(d[3], thot)
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
        
        self.stdout.p('IF Switch : Set ch 1.')
        sw.ch_set_all(1)
        
        self.stdout.p('LO Att : Set 200 mV.')
        lo_att.bias_set(200)
        

        spdata = numpy.array(spdata)
        tsys = numpy.array(tsys)
        rsky_info = numpy.array(rsky_info, dtype=object)
        
        self.stdout.p('Save : %s'%(dataname + '.spdata.npy'))
        numpy.save(datapath + '.spdata.npy', spdata)
        
        self.stdout.p('Save : %s'%(dataname + '.loatt.npy'))
        numpy.save(datapath + '.loatt.npy', sweep_data)
        
        self.stdout.p('Save : %s'%(dataname + '.tsys.npy'))
        numpy.save(datapath + '.tsys.npy', tsys)
        
        self.stdout.p('Save : %s'%(dataname + '.info.npy'))
        numpy.save(datapath + '.info.npy', rsky_info)

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
        
        # plotting
        # ---------
        #self.stdout.p('Plot')
        #self.stdout.p('----')
        print('Plot')
        print('----')
        
        pylab.rcParams['font.size'] = 8
        
        # --
        
        tshape = (4, sweep_num, 4)
        tsys_reshape = tsys.reshape(tshape)
        tsys_swap = numpy.swapaxes(tsys_reshape, 1, 2)
        tsys_plot = tsys_swap.reshape((16, sweep_num))
        
        #self.stdout.p('Plot : %s.tsys.png'%(figname))
        print('Plot : %s.tsys.png'%(figname))
        
        fig = pylab.figure()
        ax = [fig.add_subplot(4, 4, i+1) for i in range(16)]
        im = [_a.plot(sweep_data, _t) for _a, _t in zip(ax, tsys_plot)]
        [_a.set_xlabel('LO Att. (mA)') for i, _a in enumerate(ax) if i/4 > 2]
        [_a.set_ylabel('Tsys* (K)') for i, _a in enumerate(ax) if i%4 == 0]
        fig.savefig(figpath + '.tsysmap.png')
        pylab.close(fig)        
        
        
        # --
        
        sshape = (4, sweep_num, 4, -1)
        spdata_reshape = spdata.reshape(sshape)
        spdata_swap = numpy.swapaxes(spdata_reshape, 0, 1)
        spdata_plot = spdata_swap.reshape((sweep_num, 16, -1))
        
        
        for ch, d in enumerate(spdata_plot):
            print('Plot : %s.speana.%02d.png'%(figname, ch))
            #self.stdout.p('Plot : %s.speana.%02d.png'%(figname, ch))
            
            fig = pylab.figure()
            ax = [fig.add_subplot(4, 4, i+1) for i in range(16)]
            [_a.plot(_d) for _a, _d in zip(ax, d)]
            fig.suptitle('LO att = %.2f'%(sweep_data[ch]))
            fig.savefig(figpath + '.speana.%04d.png'%(ch))
            pylab.close(fig)
            continue
        
        #self.stdout.nextline()
        print('')
        print('//// plotting is done ////'')
        
        
        return

