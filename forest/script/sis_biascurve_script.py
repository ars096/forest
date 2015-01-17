
import forest
import base

import os
import time
import numpy
import pylab


def iv_plot(v, i, save, suptitle):
    ch = forest.biasbox_tools.biasbox_ch_mapper()
    l_box = ['BOX:%d'%(_i) for _i in ch.box]
    l_ch = ['CH:%d'%(_i) for _i in ch.ch]
    l_beam = ['BEAM:%d'%(_i) for _i in ch.beam]
    l_pol = ['(%s)'%(_i) for _i in ch.pol]
    l_unit = ['UNIT:%d'%(_i) for _i in ch.dsbunit]
    label = ['%s, %s\n%s %s, %s'%(_x, _c, _b, _p, _u) for _x, _c, _b, _p, _u \
             in zip(l_box, l_ch, l_beam, l_pol, l_unit)]
    
    pylab.rcParams['font.size'] = 7

    fig = pylab.figure()
    fig.suptitle(suptitle, fontsize=11)
    ax = [fig.add_subplot(4, 4, j+1) for j in range(16)]
    [_a.plot(_v, _i, '+') for _a, _v, _i in zip(ax, v, i)]
    [_a.text(0.08, 0.72, _l, transform=_a.transAxes) for _a, _l in zip(ax, label)]
    [_a.grid(True) for _a in ax]
    [_a.set_xlabel('Bias Voltage (mV)') for _i, _a in enumerate(ax) if _i/4.>=3]
    [_a.set_ylabel('Bias Current (uA)') for _i, _a in enumerate(ax) if _i%4==0]
    fig.savefig(save)
    
    pylab.close(fig)
    return


class get_sis_bias_curve(base.forest_script_base):
    method = 'get_sis_bias_curve'
    ver = '2015.01.17'
    
    def run(self, start, stop, step):
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
        datapath = fpg('biassweep.data.%s.npy')
        dataname = os.path.basename(datapath)
        figpath = fpg('biassweep.fig.%s.png')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'start': start, 'stop': stop, 'step': step}
        argstxt = str(args)        
        self.operation_start(argstxt, logfile=logpath)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Get SIS Bias Curve')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.p('savedir : %s'%(savedir))
        self.stdout.p('logfile : %s'%(logname))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        sis = self.open_sis_biasbox()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        
        # Operation part
        # --------------
        self.stdout.p('Get SIS Bias Curve')
        self.stdout.p('==================')
        
        self.stdout.p('start = %f'%(start))
        self.stdout.p('stop = %f'%(stop))
        self.stdout.p('step = %f'%(step))
        self.stdout.nextline()
        
        self.stdout.p('SIS Bias : Set 0 mV.')
        sis.bias_set(0)
        
        self.stdout.p('Generate input bias array ...')
        inp = numpy.arange(start, stop+step, step)
        self.stdout.p('inp : [%s %s %s ... %s %s %s]'%(
            inp[0], inp[1], inp[2], inp[-3], inp[-2], inp[-1]))
        
        inp = map(float, inp)
        
        self.stdout.write('SIS Bias : Sweep start ...')
        v, i = sis.bias_sweep(inp)
        self.stdout.write('done')
        self.stdout.nextline()
        
        self.stdout.p('v0 : [%.1f %.1f %.1f ... %.1f %.1f %.1f]'%(
            v[0,0], v[1,0], v[2,0], v[-3,0], v[-2,0], v[-1,0]))
        
        self.stdout.p('i0 : [%.1f %.1f %.1f ... %.1f %.1f %.1f]'%(
            i[0,0], i[1,0], i[2,0], i[-3,0], i[-2,0], i[-1,0]))
        
        self.stdout.p('SIS Bias : Set 0 mV.')
        sis.bias_set(0)
        
        self.stdout.p('Save : %s'%(dataname))
        numpy.save(datapath, (v, i))
        
        self.stdout.p('Plot : %s'%(figname))
        iv_plot(v.T, i.T, figpath, 'Bias Sweep (%s)'%(ts))
        
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


class get_sis_bias_curve_with_LO_att_level_sweep(base.forest_script_base):
    method = 'get_sis_bias_curve_with_LO_att_level_sweep'
    ver = '2015.01.17'
    
    def run(self, att_start, att_stop, att_step, sis_start, sis_stop, sis_step):
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
        datapath = fpg('biassweep.data.%s')
        dataname = os.path.basename(datapath)
        figpath = fpg('biassweep.fig.%s')
        figname = os.path.basename(figpath)
        ts = os.path.basename(fpg('%s'))
        
        # Start operation
        # ---------------
        args = {'att_start': att_start, 'att_stop': att_stop, 'att_step': att_step,
                'sis_start': sis_start, 'sis_stop': sis_stop, 'sis_step': sis_step}
        argstxt = str(args)        
        self.operation_start(argstxt, logfile=logpath)
        
        # Print welcome message
        # ---------------------
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('FOREST : Get SIS Bias Curve with LO Att Sweep')
        self.stdout.p('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        self.stdout.p('ver.%s'%(self.ver))
        self.stdout.p('savedir : %s'%(savedir))
        self.stdout.p('logfile : %s'%(logname))
        self.stdout.nextline()
        
        # Open devices
        # ------------
        self.stdout.p('Open Devices')
        self.stdout.p('============')
        
        sis = self.open_sis_biasbox()
        lo_att = self.open_lo_att()
        
        self.stdout.nextline()
        
        
        # Operation Section
        # =================
        
        # Operation part
        # --------------
        self.stdout.p('Get SIS Bias Curve')
        self.stdout.p('==================')
        self.stdout.p('att_start = %f'%(att_start))
        self.stdout.p('att_stop = %f'%(att_stop))
        self.stdout.p('att_step = %f'%(att_step))
        self.stdout.p('sis_start = %f'%(sis_start))
        self.stdout.p('sis_stop = %f'%(sis_stop))
        self.stdout.p('sis_step = %f'%(sis_step))
        self.stdout.nextline()
        
        self.stdout.p('1st LO Att : Set  0 mA.')
        lo_att.bias_set(0)

        self.stdout.p('SIS Bias : Set 0 mV.')
        sis.bias_set(0)
        
        self.stdout.p('Generate input Att bias array ...')
        att_inp = numpy.arange(att_start, att_stop+att_step, att_step)
        self.stdout.p('att_inp : [%s %s %s ... %s %s %s]'%(
            att_inp[0], att_inp[1], att_inp[2], att_inp[-3], att_inp[-2], att_inp[-1]))
        
        self.stdout.p('Generate input SIS bias array ...')
        sis_inp = numpy.arange(sis_start, sis_stop+sis_step, sis_step)
        self.stdout.p('sis_inp : [%s %s %s ... %s %s %s]'%(
            sis_inp[0], sis_inp[1], sis_inp[2], sis_inp[-3], sis_inp[-2], sis_inp[-1]))
        
        att_inp = map(float, att_inp)
        sis_inp = map(float, sis_inp)

        self.stdout.nextline()
        
        for count, abias in enumerate(att_inp):
            self.stdout.p('1st LO Att : Set %f mA. (%d/%d)'%(abias, count+1, len(att_inp)))
            lo_att.bias_set(abias)
            
            time.sleep(0.01)
            
            self.stdout.write('SIS Bias : Sweep start ... ')
            v, i = sis.bias_sweep(sis_inp)
            self.stdout.write('done')
            self.stdout.nextline()
            
            self.stdout.p('v0 : [%.1f %.1f %.1f ... %.1f %.1f %.1f]'%(
                v[0,0], v[1,0], v[2,0], v[-3,0], v[-2,0], v[-1,0]))
        
            self.stdout.p('i0 : [%.1f %.1f %.1f ... %.1f %.1f %.1f]'%(
                i[0,0], i[1,0], i[2,0], i[-3,0], i[-2,0], i[-1,0]))
            
            self.stdout.p('SIS Bias : Set 0 mV.')
            sis.bias_set(0)
        
            self.stdout.p('Save : %s'%(dataname + '.%04d.npy'%(count)))
            numpy.save(datapath + '.%04d.npy'%(count), (v, i))
            
            self.stdout.p('Plot : %s'%(figname + '.%04d.png'%(count)))
            fpath = figpath + '.%04d.png'%(count)
            plotargs = (v.T, i.T, fpath, 'Bias Sweep @ att=%.2f (%s)'%(abias, ts))
            self.detach_process(iv_plot, plotargs)
            
            self.stdout.nextline()
            continue

        self.stdout.p('1st LO Att : Set 200 mA.')
        lo_att.bias_set(200)

        self.stdout.p('SIS Bias : Set 0 mV.')
        sis.bias_set(0)
        
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
