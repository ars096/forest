
import numpy

def dBm_to_mW(dBm):
    dBm = numpy.array(dBm)
    mW = 10. ** (dBm / 10.)
    return mW

def mW_to_dBm(mW):
    mW = numpy.array(mW)
    dBm = 10. * numpy.log10(mW)
    return dBm


def rsky(dhot, dsky, thot):
    dhot = numpy.array(dhot)
    dsky = numpy.array(dsky)
    
    y = dhot / dsky
    tsys = thot / (y - 1.)
    
    return tsys

def rsky_dB(dhot, dsky, thot):
    dhot = numpy.array(dhot)
    dsky = numpy.array(dsky)
    
    dhot = dBm_to_mW(dhot)
    dsky = dBm_to_mW(dsky)
    
    tsys = rsky(dhot, dsky, thot)
    return tsys

def evaluate_rsky_from_rotating_chopper_data(d, thot, smooth=3, cut=10, nsig=2):
    s = numpy.ones(smooth)/float(smooth)
    sd = numpy.convolve(d, s, mode='same')
    sdd = sd[1:] - sd[:-1]
    
    sig = numpy.var(sdd)
    iup = numpy.where(sdd > sig*nsig)[0]
    ibot = numpy.where(sdd < -sig*nsig)[0]
    
    mask = numpy.concatenate([iup, ibot])
    d[mask] = numpy.nan
    av = numpy.nanmean(d)
    dup = d[numpy.where(d>av)]
    dbot = d[numpy.where(d<av)]
    
    dhot = numpy.mean(dup)
    dcold = numpy.mean(dbot)
    
    tsys = rsky_dB(dhot, dcold, thot)
    return tsys, (dhot, dcold, mask)

def yfactor(dhot, dcold, thot, tcold):
    dhot = numpy.array(dhot)
    dcold = numpy.array(dcold)
    
    y = dhot / dcold
    trx = (y * tcold - thot) / (1 - y)
    
    return trx

def yfactor_dB(dhot, dcold, thot, tcold):
    dhot = numpy.array(dhot)
    dcold = numpy.array(dcold)
    
    dhot = dBm_to_mW(dhot)
    dcold = dBm_to_mW(dcold)
    
    trx = yfactor(dhot, dcold, thot, tcold)
    return trx

