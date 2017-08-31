"""
Contains warnings related to mddata class

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.
"""

import warnings

def warn_prop_isnot(ptype, pname, isnot):
    warnings.warn(ptype + ' property \'' + pname \
                          + '\' is not ' + isnot  + '. Property will not be added.')

def warn_prop_unknown(pname):
    warnings.warn('Tried to set unknown property \'' + pname + '\'. Property will not be set.')

def warn_prop_immutable(clname, pname):
    warnings.warn('Tried to change ' + clname + ' property \'' + pname + '\', but it is immutable. Property will not be changed.')

def warn_prop_nocalc(clname, pname):
    warnings.warn('Tried to calculate ' + clname + ' property \'' + pname + '\', but it is already present. Property will not be calculated/changed.')

def warn_prop_missdep(clname, pname, dep):
    warnings.warn('Tried to calculate ' + clname + ' property \'' + pname + '\', but required property \'' + dep + '\' is missing. Property will not be calculated.')

def warn_file_not_found(fname):
    warnings.warn('File \'' + fname + '\' was not found. Did nothing.')
