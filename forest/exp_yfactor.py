
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

