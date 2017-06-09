from mddata.mddata import *

def flit_idict(llist, idict, iname):
    # If iname is a key in dictionary idict, return float(llist[int(idict[iname])-1]), else 0.
    if iname in idict:
        return float(llist[int(idict[iname])-1])
    else:
        return 0

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
        
        path = dirpath+'/'+fprefix
        obsdict = {}
        
        for line in open(path+'.md'):
            spaceline = line.replace('{',' ')
            linelist = spaceline.split()
            if linelist[0] == '#':
                
                obsdict[linelist[4]] = linelist[2]
            
            else:
                
                timelist.append(flit_idict(linelist, obsdict, 'time'))
                consqlist.append(flit_idict(linelist, obsdict, 'conserved'))
                templist.append(flit_idict(linelist, obsdict, 'temperature'))
                epotlist.append(flit_idict(linelist, obsdict, 'potential'))
                ekinmdlist.append(flit_idict(linelist, obsdict, 'kinetic_md'))
                ekincvlist.append(flit_idict(linelist, obsdict, 'kinetic_cv'))
                pressmdlist.append(flit_idict(linelist, obsdict, 'pressure_md'))
                presscvlist.append(flit_idict(linelist, obsdict, 'pressure_cv'))
                radgyrlist.append(flit_idict(linelist, obsdict, 'r_gyration'))
                espringlist.append(flit_idict(linelist, obsdict, 'spring'))
            
        if len(timelist)>1:
            dt = timelist[1] - timelist[0]
            if dt>0:
                for it, t in enumerate(timelist):
                    timelist[it] = it*dt
                    
        consqlist = list(zip(timelist, consqlist))
        templist = list(zip(timelist, templist))
        epotlist = list(zip(timelist, epotlist))
        ekinmdlist = list(zip(timelist, ekinmdlist))
        ekincvlist = list(zip(timelist, ekincvlist))
        pressmdlist = list(zip(timelist, pressmdlist))
        presscvlist = list(zip(timelist, presscvlist))
        radgyrlist = list(zip(timelist, radgyrlist))
        espringlist = list(zip(timelist, espringlist))
        
        super(ipi_mddata, self).__init__(path, 3, 16, 1, consq=consqlist, temp=templist, epot=epotlist, \
                                         ekinmd=ekinmdlist, ekincv=ekincvlist, pressmd=pressmdlist, \
                                         presscv=presscvlist, radgyr=radgyrlist, espring=espringlist)


#testmd = ipi_mddata('.','test')
