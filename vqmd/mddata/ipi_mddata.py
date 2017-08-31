"""
Contains the ipi_mddata class, which is a mddata child for i-Pi output

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.
"""

from vqmd.mddata import mddata
from vqmd.mddata.warnings import *

def append_idict(vlist, llist, idict, iname):
    # Appends to list vlist a float value from line split list llist,
    # found at the index specified by the value to key iname in idict.
    if iname in idict:
        vlist.append(float(llist[int(idict[iname])-1]))
        return 0
    else:
        return 1

def append_idict_lists(listdict, llist, idict):
    # Calls append_idict for key(names)/value(lists) pairs from listdict
    for iname in listdict:
        append_idict(listdict[iname], llist, idict, iname)

class ipi_mddata(mddata):

    tsspnames = mddata.tsspnames + ['consqty', 'ekin_md', 'press_md', 'espring']
    tsmpnames = mddata.tsmpnames + ['ekint', 'virialt', 'virialt_md' 'kstresst', 'kstresst_md', 'stresst', 'stresst_md']
    tcvpnames = mddata.tcvpnames + ['cradgyrv']

    def __init__(self, dirpath, fprefix):

        timelist = []
        consqlist = []
        templist = []
        epotlist = []
        ekinmdlist = []
        ekincvlist = []
        pressmdlist = []
        presscvlist = []
        radgyrlist = []
        espringlist = []

        lnamedict = {
            'time'         : timelist,
            'conserved'    : consqlist,
            'temperature'  : templist,
            'potential'    : epotlist,
            'kinetic_md'   : ekinmdlist,
            'kinetic_cv'   : ekincvlist,
            'pressure_md'  : pressmdlist,
            'pressure_cv'  : presscvlist,
            'r_gyration'   : radgyrlist,
            'spring'       : espringlist
        }

        obsdict = {}

        path = dirpath+'/'+fprefix

        try:
            with open(path + '.md') as mdfile:
                for line in mdfile:
                    spaceline = line.replace('{',' ')
                    linelist = spaceline.split()

                    if linelist[0] == '#':
                        obsdict[linelist[4]] = linelist[2]

                    else:
                        append_idict_lists(lnamedict, linelist, obsdict)
        except(FileNotFoundError):
            warn_file_not_found(path + '.md')

        kwnamedict = {
            'conserved' : 'consqty',
            'temperature' : 'temp',
            'potential' : 'epot',
            'kinetic_md' : 'ekin_md',
            'kinetic_cv' : 'ekin',
            'pressure_md' : 'press_md',
            'pressure_cv' : 'press',
            'r_gyration' : 'radgyr',
            'spring' : 'espring'
        }

        seriesdict = {}

        for vname,vlist in lnamedict.items():
            if vname in obsdict and vname in kwnamedict:
                seriesdict[kwnamedict[vname]] = [timelist, vlist]

        super(ipi_mddata, self).__init__(path, 0, 1, 3, seriesdict)
