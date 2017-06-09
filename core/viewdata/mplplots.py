from pylab import *

class mplplot(object):

    def __init__(self, xmlin, rawdata, calcdata, **kwargs):
        tempdata = []
        potdata = []
   
        for mddata in rawdata.data:
            tempdata.append(mddata.data.temp)
            potdata.append(mddata.data.epot)
      
            fig = figure('64H Mol rs=1.33 T=1200K')
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)
 
            multiGraphXY(ax1, tempdata, names = naml, ylabel='Temperature [K]', title='64H Mol rs=1.33 T=1200K') 
            multiGraphXY(ax2, potdata, xlabel='Time [fs]', ylabel='Potential Energy [H]')  

class mplplots(object):

    def __init__(self, xmlin, rawdata, calcdata, **kwargs):
        
        self.plots = []   
        for xmlfield in xmlin.fields:
            self.plots.append(mplplot(xmlfield, rawdata, calcdata))

        show()
