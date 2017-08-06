import pandas as pd
import bisect

class mddata(object):

    cssprops = ['label', 'npart', 'nbead', 'ndim',
                'dtbase', 'volume', 'density', 'wsrad']
    csvprops = []
    csmprops = ['cellmat']

    ccsprops = ['names', 'masses', 'charges']
    ccvprops = ['dipmom', 'spin']

    cbsprops = []
    cbvprops = []

    tssprops = ['consq', 'temp', 'epot', 'ekinmd', 'ekincv', 'pressmd', 'presscv', 'radgyr', 'espring',
                'tvolume', 'tdensity', 'twsrad']
    tsvprops = []
    tsmprops = ['tcellmat']

    tcsprops = []
    tcvprops = ['cpos', 'cvel', 'cfrc', 'tdipmom', 'tspin']

    tbsprops = []
    tbvprops = ['bpos', 'bvel', 'bfrc']

    def __init__(self, label, npart, nbead, ndim, kwdict = {}, **kwargs):

        kwargs.update({'label' : label, 'npart' : npart, 'nbead' : nbead, 'ndim' : ndim})
        kwargs.update(kwdict)

        self.cssprops = []
        self.csvprops = []
        self.csmprops = []
        self.ccsprops = []
        self.ccvprops = []
        self.cbsprops = []
        self.cbvprops = []
        self.tssprops = []
        self.tsvprops = []
        self.tsmprops = []
        self.tcsprops = []
        self.tcvprops = []
        self.tbsprops = []
        self.tbvprops = []
        self.props = []

        self.set_props(kwdict)

    def set_props(self, kwdict):

        for name in kwdict:
            if name in mddata.cssprops:
                newprop = kwdict[name]
                self.cssprops.append(name)

            elif name in mddata.csvprops:
                newprop = kwdict[name]
                self.csvprops.append(name)

            elif name in mddata.csmprops:
                newprop = kwdict[name]
                self.csmprops.append(name)

            elif name in mddata.ccsprops:
                newprop = kwdict[name]
                self.ccsprops.append(name)

            elif name in mddata.ccvprops:
                newprop = kwdict[name]
                self.ccvprops.append(name)

            elif name in mddata.cbsprops:
                newprop = kwdict[name]
                self.cbsprops.append(name)

            elif name in mddata.cbvprops:
                newprop = kwdict[name]
                self.cbvprops.append(name)

            elif name in mddata.tssprops:
                newprop = kwdict[name]
                self.tssprops.append(name)

            elif name in mddata.tsvprops:
                newprop = kwdict[name]
                self.tsvprops.append(name)

            elif name in mddata.tsmprops:
                newprop = kwdict[name]
                self.tsmprops.append(name)

            elif name in mddata.tcsprops:
                newprop = kwdict[name]
                self.tcsprops.append(name)

            elif name in mddata.tcvprops:
                newprop = kwdict[name]
                self.tcvprops.append(name)

            elif name in mddata.tbsprops:
                newprop = kwdict[name]
                self.tbsprops.append(name)

            elif name in mddata.tbvprops:
                newprop = kwdict[name]
                self.tbvprops.append(name)

            else:
                raise AttributeError('mddata set_props: Tried to set property that is not in property lists.')

            self.props.append(name)
            self.__dict__[name] = newprop


            def __setattr__(self, name, value):
                if hasattr(self, name):
                    raise TypeError('mddata setattr: Tried to set mddata attribute, but they are immutable.')
                else:
                    self.set_props({name : value})

            def check_plists(self):
                return self.props == \
                    self.cssprops + self.csvprops + self.csmprops \
                    + self.ccsprops + self.ccvprops + self.cbsprops + self.cbvprops \
                    + self.tssprops + self.tsvprops + self.tsmprops \
                    + self.tcsprops + self.tcvprops + self.tbsprops + self.tbvprops
