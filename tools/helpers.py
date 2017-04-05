from collections import Iterable

def iter_ndim(testlist, ndim=0):
    
    if isinstance(testlist, Iterable):
        ndim += 1
        ndim = iter_ndim(testlist[0], ndim)
        return ndim
    
    else:
        return ndim
