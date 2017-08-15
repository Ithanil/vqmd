import warnings

# Warnings related to mddata class

def warn_prop_isnot(ptype, pname, isnot):
    warnings.warn(ptype + ' property \'' + pname \
                          + '\' is not ' + isnot  + '. Property will not be added.')

def warn_prop_unknown(name):
    warnings.warn('Tried to set unknown property \'' + name + '\'.')

def warn_file_not_found(fname):
    warnings.warn('No such file or directory: \'' + fname + '\'. Did nothing.')
