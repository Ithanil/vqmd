from pylab import *
import pandas as pd
import bisect

class mddata(object):

    def __init__(self, label, kwdict, **kwargs):

        proplist = ['ndim', 'npart', 'nbead', 'pnames', 'masses', 'dtbase', 'cellabc']
        tproplist = ['pos', 'vel', 'frc', 'consq', 'temp', 'epot', 'ekinmd', 'ekincv',
                     'pressmd', 'presscv', 'radgyr', 'espring', 'tcellabc', 'tnpart']
        self.props = []
        self.tprops = []

        self.label = label
        kwargs.update(kwdict)

        for prop in proplist:
            self.checkset_prop(prop, kwargs)
        for tprop in tproplist:
            self.checkset_tprop(tprop, kwargs)

    def checkset_prop(self, name, kwdict):

        if name in kwdict:
            setattr(self, name, kwdict[name])
            self.props.append(name)

    def checkset_tprop(self, name, kwdict):

        if name in kwdict:
            print(name)
            print(kwdict[name])
            if isinstance(kwdict[name], pd.Series):
                setattr(self, name, kwdict[name])
                self.tprops.append(name)
            else:
                print('[mddata] Error: mddata constructor received time dependent property which is not an instance of Pandas Series.')
