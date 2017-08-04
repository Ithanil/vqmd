from pylab import *
import pandas as pd

class mplplot(object):

    def __init__(self, xmlin, rawdata, calcdata, **kwargs):
        tempdata = []
        potdata = []

        naml = []

        for mddata in rawdata.data:
            tempdata.append(mddata.data.temp)
            potdata.append(mddata.data.epot)
            
            naml.append(mddata.name)
        
        ptitle = xmlin[1].attribs['title']
        fig = figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
 
        multiGraphXY(ax1, tempdata, names = naml, ylabel='Temperature [K]', title=ptitle, yscale='log') 
        multiGraphXY(ax2, potdata, xlabel='Time [fs]', ylabel='Potential Energy [H]')  

class mplplots(object):

    def __init__(self, xmlin, rawdata, calcdata, **kwargs):
        
        self.plots = []   
        for xmlfield in xmlin.fields:
            if xmlfield[0] == 'plot':
                self.plots.append(mplplot(xmlfield, rawdata, calcdata))

        show()
