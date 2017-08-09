import numpy as np
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

        propdict = ({'label' : label, 'npart' : npart, 'nbead' : nbead, 'ndim' : ndim})
        propdict.update(kwdict)
        propdict.update(kwargs)

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

        self.__dict__['cprops'] = []
        self.__dict__['tprops'] = []
        self.__dict__['props'] = []

        self.set_props(propdict)

    def set_props(self, kwdict):

        for name in kwdict:
            newprop = np.array(kwdict[name], dtype=object) # first convert all properties to np.ndarray
            try: tlen = len(newprop[0]) # and calculate number of time steps for time-dependent props
            except: tlen = 0

            # The following if tree checks if the input lists have reasonable shape.
            # Probably not very pythonic

            if name in mddata.csspnames:
                if np.shape(newprop) == ():
                    self.cssprops.append(name)
                elif np.shape(newprop) == (1,):
                    self.cssprops.append(name)
                    newprop = newprop[0]
                else:
                    print('Warning: Constant system scalar property \''+ name \
                          +'\' is not a scalar or a list with shape (1,). Property will not be added.')
                    continue

            elif name in mddata.csvpnames:
                if np.shape(newprop) == (self.ndim,):
                    self.csvprops.append(name)
                else:
                    print('Warning: Constant system vector property \''+ name \
                          +'\' is not a list with shape (ndim,). Property will not be added.')
                    continue

            elif name in mddata.csmpnames:
                if np.shape(newprop) == (self.ndim, self.ndim):
                    self.csmprops.append(name)
                else:
                    print('Warning: Constant system matrix property \''+ name \
                          +'\' is not a list with shape (ndim, ndim). Property will not be added.')
                    continue

            elif name in mddata.ccspnames:
                if np.shape(newprop) == (self.npart,):
                    self.ccsprops.append(name)
                else:
                    print('Warning: Constant centroid scalar property \''+ name \
                          +'\' is not a list with shape (npart,). Property will not be added.')
                    continue

            elif name in mddata.ccvpnames:
                if np.shape(newprop) == (self.npart, self.ndim):
                    self.ccvprops.append(name)
                else:
                    print('Warning: Constant centroid vector property \''+ name \
                          +'\' is not a list with shape (npart, ndim). Property will not be added.')
                    continue

            elif name in mddata.cbspnames:
                if np.shape(newprop) == (self.npart, self.nbead):
                    self.cbsprops.append(name)
                else:
                    print('Warning: Constant bead scalar property \''+ name \
                          +'\' is not a list with shape (npart, nbead). Property will not be added.')
                    continue

            elif name in mddata.cbvpnames:
                if np.shape(newprop) == (self.npart, self.nbead, self.ndim):
                    self.cbvprops.append(name)
                else:
                    print('Warning: Constant bead vector property \''+ name \
                          +'\' is not a list with shape (npart, nbead, ndim). Property will not be added.')
                    continue

            elif name in mddata.tsspnames:
                if np.shape(newprop) == (2, tlen):
                    self.tssprops.append(name)
                    newprop = pd.Series(newprop[1], index = newprop[0])
                else:
                    print('Warning: Time-dependent system scalar property \''+ name \
                          +'\' is not a list with shape (2, *). Property will not be added.')
                    continue

            elif name in mddata.tsvpnames:
                if np.shape(newprop) == (2, tlen, self.ndim):
                    self.tsvprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    print('Warning: Time-dependent system vector property \''+ name \
                          +'\' is not a list with shape (2, *, ndim). Property will not be added.')
                    continue

            elif name in mddata.tsmpnames:
                if np.shape(newprop) == (2, tlen, self.ndim, self.ndim):
                    self.tsmprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    print('Warning: Time-dependent system matrix property \''+ name \
                          +'\' is not a list with shape (2, *, ndim, ndim). Property will not be added.')
                    continue

            elif name in mddata.tcspnames:
                if np.shape(newprop) == (2, tlen, self.npart):
                    self.tcsprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    print('Warning: Time-dependent centroid scalar property \''+ name \
                          +'\' is not a list with shape (2, *, npart). Property will not be added.')
                    continue

            elif name in mddata.tcvpnames:
                if np.shape(newprop) == (2, tlen, self.npart, self.ndim):
                    self.tcvprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    print('Warning: Time-dependent centroid vector property \''+ name \
                          +'\' is not a list with shape (2, *, npart, ndim). Property will not be added.')
                    continue

            elif name in mddata.tbspnames:
                if np.shape(newprop) == (2, tlen, self.npart, self.nbead):
                    self.tbsprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    print('Warning: Time-dependent bead scalar property \''+ name \
                          +'\' is not a list with shape (2, *, npart, nbead). Property will not be added.')
                    continue

            elif name in mddata.tbvpnames:
                if np.shape(newprop) == (2, tlen, self.npart, self.nbead, self.ndim):
                    self.tbvprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    print('Warning: Time-dependent bead vector property \''+ name \
                          +'\' is not a list with shape (2, *, npart, nbead, ndim). Property will not be added.')
                    continue

            else:
                raise AttributeError('mddata set_props: Tried to set property \'' + name + '\' that is not in property lists.')

            self.__dict__[name] = newprop

        self.__dict__['cprops'] = \
            self.cssprops + self.csvprops + self.csmprops \
            + self.ccsprops + self.ccvprops + self.cbsprops + self.cbvprops

        self.__dict__['tprops'] = \
                self.tssprops + self.tsvprops + self.tsmprops \
            + self.tcsprops + self.tcvprops + self.tbsprops + self.tbvprops

        self.__dict__['props'] = self.cprops + self.tprops

    def __setattr__(self, name, value):
        if hasattr(self,name):
            raise TypeError('mddata setattr: Tried to change mddata attribute \'' + name + '\', but it is immutable.')
        else:
            self.set_props({name : value})
