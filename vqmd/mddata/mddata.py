import pandas as pd
import bisect

class mddata(object):

    csspnames = ['label', 'npart', 'nbead', 'ndim',
                'dtbase', 'volume', 'density', 'wsrad']
    csvpnames = []
    csmpnames = ['cellmat']

    ccspnames = ['names', 'masses', 'charges']
    ccvpnames = ['dipmom', 'spin']

    cbspnames = []
    cbvpnames = []

    tsspnames = ['consq', 'temp', 'epot', 'ekinmd', 'ekincv', 'pressmd', 'presscv', 'radgyr', 'espring',
                'tvolume', 'tdensity', 'twsrad']
    tsvpnames = []
    tsmpnames = ['tcellmat']

    tcspnames = []
    tcvpnames = ['cpos', 'cvel', 'cfrc', 'tdipmom', 'tspin']

    tbspnames = []
    tbvpnames = ['bpos', 'bvel', 'bfrc']

    def __init__(self, label, npart, nbead, ndim, kwdict = {}, **kwargs):

        kwargs.update({'label' : label, 'npart' : npart, 'nbead' : nbead, 'ndim' : ndim})
        kwargs.update(kwdict)

        self.__dict__['cssprops'] = []
        self.__dict__['csvprops'] = []
        self.__dict__['csmprops'] = []
        self.__dict__['ccsprops'] = []
        self.__dict__['ccvprops'] = []
        self.__dict__['cbsprops'] = []
        self.__dict__['cbvprops'] = []
        self.__dict__['tssprops'] = []
        self.__dict__['tsvprops'] = []
        self.__dict__['tsmprops'] = []
        self.__dict__['tcsprops'] = []
        self.__dict__['tcvprops'] = []
        self.__dict__['tbsprops'] = []
        self.__dict__['tbvprops'] = []
        self.__dict__['props'] = []

        self.set_props(kwargs)

    def set_props(self, kwdict):

        for name in kwdict:
            if name in mddata.csspnames:
                newprop = kwdict[name]
                self.cssprops.append(name)

            elif name in mddata.csvpnames:
                newprop = kwdict[name]
                self.csvprops.append(name)

            elif name in mddata.csmpnames:
                newprop = kwdict[name]
                self.csmprops.append(name)

            elif name in mddata.ccspnames:
                newprop = kwdict[name]
                self.ccsprops.append(name)

            elif name in mddata.ccvpnames:
                newprop = kwdict[name]
                self.ccvprops.append(name)

            elif name in mddata.cbspnames:
                newprop = kwdict[name]
                self.cbsprops.append(name)

            elif name in mddata.cbvpnames:
                newprop = kwdict[name]
                self.cbvprops.append(name)

            elif name in mddata.tsspnames:
                newprop = kwdict[name]
                self.tssprops.append(name)

            elif name in mddata.tsvpnames:
                newprop = kwdict[name]
                self.tsvprops.append(name)

            elif name in mddata.tsmpnames:
                newprop = kwdict[name]
                self.tsmprops.append(name)

            elif name in mddata.tcspnames:
                newprop = kwdict[name]
                self.tcsprops.append(name)

            elif name in mddata.tcvpnames:
                newprop = kwdict[name]
                self.tcvprops.append(name)

            elif name in mddata.tbspnames:
                newprop = kwdict[name]
                self.tbsprops.append(name)

            elif name in mddata.tbvpnames:
                newprop = kwdict[name]
                self.tbvprops.append(name)

            else:
                raise AttributeError('mddata set_props: Tried to set property \'' + name + '\' that is not in property lists.')

            self.props.append(name)
            self.__dict__[name] = newprop


    def __setattr__(self, name, value):
        if hasattr(self,name):
            raise TypeError('mddata setattr: Tried to change mddata attribute \'' + name + '\', but it is immutable.')
        else:
            self.set_props({name : value})

    def check_plists(self):
        return self.props == \
            self.cssprops + self.csvprops + self.csmprops \
            + self.ccsprops + self.ccvprops + self.cbsprops + self.cbvprops \
            + self.tssprops + self.tsvprops + self.tsmprops \
            + self.tcsprops + self.tcvprops + self.tbsprops + self.tbvprops
