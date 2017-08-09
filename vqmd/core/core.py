from vqmd.core.rawdata.rawdata import rawdata
from vqmd.core.viewdata.viewdata import viewdata

class core(object):

    def __init__(self, xmlin, **kwargs):
        self.rawdata = rawdata(xmlin.fields[0][1].fields[0][1])
        self.calcdata = []
        self.viewdata = viewdata(xmlin.fields[0][1].fields[2][1], self.rawdata, self.calcdata)
