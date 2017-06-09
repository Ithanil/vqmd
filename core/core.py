from pylab import *
from core.rawdata.rawdata import *
from core.viewdata.viewdata import *

class core(object):

    def __init__(self, xmlin, **kwargs):

        self.rawdata = rawdata(xmlin)
        self.calcdata = []
        self.viewdata = viewdata(xmlin, self.rawdata, self.calcdata)
        
