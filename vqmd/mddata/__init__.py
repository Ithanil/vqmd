import numpy as np
import pandas as pd
import bisect

from vqmd.mddata.warnings import *

class mddata(object):

    # constant system scalar/vector/matrix properties
    csspnames = ['label', 'npart', 'nbead', 'ndim',
                'volume', 'density', 'wseitzr']
    csvpnames = []
    csmpnames = ['cellmat']

    # constant centroid scalar/vector properties
    ccspnames = ['names', 'cmasses']
    ccvpnames = []

    # constant bead scalar/vector properties
    cbspnames = ['bmasses']
    cbvpnames = []

    # time-dependent system scalar/vector/matrix properties
    tsspnames = ['temp', 'epot', 'ekin', 'etot', 'press', 'virial', 'radgyr',
                'tvolume', 'tdensity', 'twseitzr']
    tsvpnames = []
    tsmpnames = ['tcellmat']

    # time-dependent centroid scalar/vector properties
    tcspnames = []
    tcvpnames = ['cpos', 'cvel', 'cfrc', 'cmom']

    # time-dependent bead scalar/vector properties
    tbspnames = []
    tbvpnames = ['bpos', 'bvel', 'bfrc', 'bmom']

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

            if name in self.__class__.csspnames:
                if np.shape(newprop) == ():
                    self.cssprops.append(name)
                    newprop = newprop.item()
                elif np.shape(newprop) == (1,):
                    self.cssprops.append(name)
                    newprop = newprop[0]
                else:
                    warn_prop_isnot('Constant system scalar', name, 'a scalar or list with shape (1,)')
                    continue

            elif name in self.__class__.csvpnames:
                if np.shape(newprop) == (self.ndim,):
                    self.csvprops.append(name)
                    newprop = np.array(newprop, dtype=float)
                else:
                    warn_prop_isnot('Constant system vector', name, 'a list with shape (ndim,)')
                    continue

            elif name in self.__class__.csmpnames:
                if np.shape(newprop) == (self.ndim, self.ndim):
                    self.csmprops.append(name)
                    newprop = np.array(newprop, dtype=float)
                else:
                    warn_prop_isnot('Constant system matrix', name, 'a list with shape (ndim, ndim)')
                    continue

            elif name in self.__class__.ccspnames:
                if np.shape(newprop) == (self.npart,):
                    self.ccsprops.append(name)
                    try: newprop = np.array(newprop, dtype=float)
                    except ValueError: pass
                else:
                    warn_prop_isnot('Constant centroid scalar', name, 'a list with shape (npart,)')
                    continue

            elif name in self.__class__.ccvpnames:
                if np.shape(newprop) == (self.npart, self.ndim):
                    self.ccvprops.append(name)
                    newprop = np.array(newprop, dtype=float)
                else:
                    warn_prop_isnot('Constant centroid vector', name, 'a list with shape (npart, ndim)')
                    continue

            elif name in self.__class__.cbspnames:
                if np.shape(newprop) == (self.npart, self.nbead):
                    self.cbsprops.append(name)
                    newprop = np.array(newprop, dtype=float)
                else:
                    warn_prop_isnot('Constant bead scalar', name, 'a list with shape (npart, nbead)')
                    continue

            elif name in self.__class__.cbvpnames:
                if np.shape(newprop) == (self.npart, self.nbead, self.ndim):
                    self.cbvprops.append(name)
                    newprop = np.array(newprop, dtype=float)
                else:
                    warn_prop_isnot('Constant bead vector', name, 'a list with shape (npart, nbead, ndim)')
                    continue

            elif name in self.__class__.tsspnames:
                if np.shape(newprop) == (2, tlen):
                    self.tssprops.append(name)
                    newprop = pd.Series(newprop[1], index = newprop[0])
                else:
                    warn_prop_isnot('Time-dependent system scalar', name, 'a list with shape (2, *)')
                    continue

            elif name in self.__class__.tsvpnames:
                if np.shape(newprop) == (2, tlen, self.ndim):
                    self.tsvprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    warn_prop_isnot('Time-dependent system vector', name, 'a list with shape (2, *, ndim)')
                    continue

            elif name in self.__class__.tsmpnames:
                if np.shape(newprop) == (2, tlen, self.ndim, self.ndim):
                    self.tsmprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    warn_prop_isnot('Time-dependent system matrix', name, 'a list with shape (2, *, ndim, ndim)')
                    continue

            elif name in self.__class__.tcspnames:
                if np.shape(newprop) == (2, tlen, self.npart):
                    self.tcsprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    warn_prop_isnot('Time-dependent centroid scalar', name, 'a list with shape (2, *, npart)')
                    continue

            elif name in self.__class__.tcvpnames:
                if np.shape(newprop) == (2, tlen, self.npart, self.ndim):
                    self.tcvprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    warn_prop_isnot('Time-dependent centroid vector', name, 'a list with shape (2, *, npart, ndim)')
                    continue

            elif name in self.__class__.tbspnames:
                if np.shape(newprop) == (2, tlen, self.npart, self.nbead):
                    self.tbsprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    warn_prop_isnot('Time-dependent bead scalar', name, 'a list with shape (2, *, npart, nbead)')
                    continue

            elif name in self.__class__.tbvpnames:
                if np.shape(newprop) == (2, tlen, self.npart, self.nbead, self.ndim):
                    self.tbvprops.append(name)
                    newprop = pd.Series(newprop[1])
                else:
                    warn_prop_isnot('Time-dependent bead vector', name, 'a list with shape (2, *, npart, nbead, ndim)')
                    continue

            else:
                warn_prop_unknown(name)
                continue

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
            warn_prop_immutable(self.__class__.__name__, name)
        else:
            self.set_props({name : value})

    def calc_check(self, name, deps):
        if hasattr(self, name):
            warn_prop_nocalc(self.__class__.__name__, name)
            return False
        for dep in deps:
            if not hasattr(self, dep):
                warn_prop_missdep(self.__class__.__name__, name, dep)
                return False
        return True

    def calcset_volume(self):
        if self.calc_check('volume', ['cellmat']):
            self.volume = np.abs(np.dot(np.cross(self.cellmat[0], self.cellmat[1]), self.cellmat[2]))
