from pylab import *
from mddata.ipi_mddata import *
class data(object):

    def __init__(self, xmlin, **kwargs):

        if xmlin[0]=='data':
            print(xmlin[1].attribs['mode'])
            print(xmlin[1].attribs['path'])
            print(xmlin[1].attribs['name'])
            print(xmlin[1].attribs['type'])
            self.mode = xmlin[1].attribs['mode']
            self.path = xmlin[1].attribs['path']
            self.name = xmlin[1].attribs['name']
            self.type = xmlin[1].attribs['type']
            
            if self.type == 'ipi':
                self.data = ipi_mddata(self.path, xmlin[1].fields[0][1])

class rawdata(object):

    def __init__(self, xmlin, **kwargs):

        self.data = []   
        for xmlfield in xmlin.fields:
            self.data.append(data(xmlfield))
