from vqmd.mddata.mddata import *

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
            'pressurve_cv' : presscvlist,
            'r_gyration'   : radgyrlist,
            'spring'       : espringlist
        }

        obsdict = {}

        path = dirpath+'/'+fprefix

        for line in open(path+'.md'):
            spaceline = line.replace('{',' ')
            linelist = spaceline.split()
            if linelist[0] == '#':

                obsdict[linelist[4]] = linelist[2]

            else:

                append_idict_lists(lnamedict, linelist, obsdict)

        dt = 0
        if len(timelist)>1:
            dt = timelist[1] - timelist[0]
        if dt<=0:
            dt = 0

        kwnamedict = {
            'conserved' : 'consq',
            'temperature' : 'temp',
            'potential' : 'epot',
            'kinetic_mc' : 'ekinmd',
            'kinetic_cv' : 'ekincv',
            'pressure_md' : 'pressmd',
            'pressure_cv' : 'presscv',
            'r_gyration' : 'radgyr',
            'spring' : 'espring'
        }

        seriesdict = {}

        for vname,vlist in lnamedict.items():
            if vname in obsdict and vname in kwnamedict:
                seriesdict[kwnamedict[vname]] = [timelist, vlist]

        super(ipi_mddata, self).__init__(path, 0, 1, 3, seriesdict, dtbase=dt)
