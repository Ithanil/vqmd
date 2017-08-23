from vqmd.core.read.data import data
from vqmd.core.warnings import *

class read(object):

    def __init__(self, xmlin, core, **kwargs):

        self.datas = []

        for xmlfield in xmlin.fields:
            if xmlfield[0] == 'data':
                self.datas.append(data(xmlfield[1], core))

            else:
                warn_wrong_xml(xmlfield[0])
