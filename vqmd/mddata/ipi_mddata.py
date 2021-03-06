"""
Contains the ipi_mddata class, which is a mddata child for i-Pi output

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.
"""

from vqmd.mddata import mddata
from vqmd.lib.ipilib import *
from vqmd.mddata.warnings import *
import os


class ipi_mddata(mddata):

    tsspnames = mddata.tsspnames + ['consqty', 'ekin_md', 'press_md', 'espring']
    tsmpnames = mddata.tsmpnames + ['ekint', 'virialt', 'virialt_md' 'kstresst', 'kstresst_md', 'stresst', 'stresst_md']
    tcvpnames = mddata.tcvpnames + ['cradgyrv']

    def __init__(self, dirpath, fprefix):

        path = dirpath+'/'+fprefix

        timelist, seriesdict = parse_mdfile(path)

        seriesdict.update(parse_trajectories(path, timelist))

        npart = seriesdict.pop('npart', 1)
        nbead = seriesdict.pop('nbead', 1)

        super(ipi_mddata, self).__init__(path, npart, nbead, seriesdict)


def parse_mdfile(path):

    mddict = {}
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

    obsdict = {}

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


    for vname,vlist in lnamedict.items():
        if vname in obsdict and vname in kwnamedict:
            mddict[kwnamedict[vname]] = [timelist, vlist]

    return timelist, mddict


def parse_trajectories(path, timelist):

    trajsdict = {}

    trajsdict.update(parse_traj_centroid(path, 'pos.xyz', 'cpos', timelist))
    trajsdict.update(parse_traj_centroid(path, 'vel.xyz', 'cvel', timelist))
    trajsdict.update(parse_traj_centroid(path, 'frc.xyz', 'cfrc', timelist))

    trajsdict.update(parse_traj_bead(path, 'pos', 'xyz', 'bpos', timelist))
    trajsdict.update(parse_traj_bead(path, 'vel', 'xyz', 'bvel', timelist))
    trajsdict.update(parse_traj_bead(path, 'frc', 'xyz', 'bfrc', timelist))

    return trajsdict


def parse_traj_centroid(path, suffix, name, timelist):

    trajdict = {}

    try:
        trajfile = path + '.' + suffix
        trajdata = list(iter_file_name(trajfile))

        trajdict['npart'] = trajdata[0]['natoms']
        trajdict['cmasses'] = trajdata[0]['masses']
        trajdict['names'] = trajdata[0]['names']
        trajdict['cellmat'] = trajdata[0]['cell']

        tcellmatlist = [idict['cell'] for idict in trajdata]
        trajlist = [idict['data'].reshape(trajdict['npart'], 3) for idict in trajdata]

        trajdict['tcellmat'] = [timelist, tcellmatlist]
        trajdict[name] = [timelist, trajlist]

    except(FileNotFoundError):
        pass

    return trajdict


def parse_traj_bead(path, suffix, format, name, timelist):

    trajdict = {}
    btrajlist = []
    ibead = 0

    while True:
        try:
            trajfile = path + '.' + suffix + '_' + str(ibead) + '.' + format
            trajdata = list(iter_file_name(trajfile))

            if ibead == 0:
                trajdict['npart'] = trajdata[0]['natoms']
                trajdict['cmasses'] = trajdata[0]['masses']
                trajdict['names'] = trajdata[0]['names']
                trajdict['cellmat'] = trajdata[0]['cell']

                tcellmatlist = [idict['cell'] for idict in trajdata]
                trajdict['tcellmat'] = [timelist, tcellmatlist]
            btrajlist.append( [idict['data'].reshape(trajdict['npart'], 3) for idict in trajdata] )
            ibead += 1

        except(FileNotFoundError):
            if ibead > 0:
                trajlist = [] # Now the properly shaped list is constructed
                for step in range(len(btrajlist[0])):
                    steplist = []
                    for bead in range(ibead):
                        steplist.append(btrajlist[bead][step])
                    trajlist.append(steplist)

                trajdict['nbead'] = ibead
                trajdict[name] = [timelist, trajlist]

            return trajdict


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
