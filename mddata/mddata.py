from pylab import *
import bisect

class mdtprop(ndarray):
# Array class to represent (multidimensional) data with respect to a
# monotonically increasing scalar variable, like the time.
    
    def __new__(cls, tdata, pdata=None, label=None):
    # If pdata=None, tdata is expected to be list of elements (t, p(t))
    # Else tdata should contain the time points t, pdata the data points p(t)
    # Optionally, a label can be set.

        if pdata is None:
            if len(shape(tdata)) < 2: raise ValueError('mdtprop.__new__: If tdata is provided without separate pdata, tdata must have at least two dimensions.')
            obj = asarray(tdata).view(cls)
        else:
            if len(shape(tdata)) > 1: raise ValueError('mdtprop.__new__: If tdata is provided with separate pdata, tdata must have only one dimension.') 
            obj = asarray(zip(tdata, pdata)).view(cls)
        
        obj.label = label
        return obj

    def __array_finalize__(self, obj):
    # needed for ndarray functionality
        
        if obj is None: return
        self.test = getattr(obj, 'label', None)

    def tindex(self, time):
    # Takes an any point in time and returns the time-wise closest
    # data index "to the left"
        
        index = bisect.bisect(self[:, 0], time)
        if index > 0: index -= 1
        
        return index

    def tpoint(self, time):
    # Takes an any point in time and returns the time-wise closest
    # data point "to the left"
        
        return self[self.tindex(time)]
    
    def tvalue(self, time):
    # Takes an any point in time and returns the time-wise closest
    # data value "to the left"
        
        return self[self.tindex(time), 1]

    def tslice(self, itime, ftime=None):
    # Takes two points in time and returns the data points in between

        if ftime is not None:
            indf = self.tindex(ftime)
        else:
            indf = len(self) - 1
        
        indi = self.tindex(itime)
        if indi+1 < len(self) and self[indi, 0] < itime: indi += 1
        
        if indf < indi:
            print("mdtprop.tslice: Final time index smaller/equal initial time index! Empty slice will be returned.")
        
        return self[indi:indf+1] # slice is mdtprop

    def tslicev(self, itime, ftime=None):
    # Takes two points in time and returns the data values in between
        
        return asarray(self.tslice(itime, ftime)[:, 1]) # no mdtprop


class mddata(object):

    def __init__(self, label, ndim, npart, nbead, **kwargs):
        
        self.label = label
        self.ndim = ndim
        self.npart = npart
        self.nbead = nbead
        
        proplist = ['pnames', 'masses', 'fixdt', 'density', 'volume', 'cellabc']
        tproplist = ['pos', 'vel', 'frc', 'consq', 'temp', 'epot', 'ekinmd', 'ekincv', 'pressmd', 'presscv', 'radgyr', 'espring']
        
        for prop in proplist:
            self.checkset_prop(prop, kwargs)
        for tprop in tproplist:
            self.checkset_tprop(tprop, kwargs)
        
    def checkset_prop(self, name, kwdict):
        
        if name in kwdict:
            setattr(self, name, kwdict[name])
        
    def checkset_tprop(self, name, kwdict):
        
        if name in kwdict:
            setattr(self, name, mdtprop(kwdict[name]))
