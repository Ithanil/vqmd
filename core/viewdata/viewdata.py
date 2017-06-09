from pylab import *
from core.viewdata.mplplots import *

class viewdata(object):

    def __init__(self, xmlin, rawdata, calcdata, **kwargs):

        self.plots = mplplots(xmlin.fields[0][1], rawdata, calcdata)
	#self.views
