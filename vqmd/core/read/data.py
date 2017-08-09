from vqmd.mddata.mddata import mddata
from vqmd.mddata.ipi_mddata import ipi_mddata
from vqmd.core.warnings import *

class data(object):

    def __init__(self, xmlin, core, **kwargs):

        self.data = mddata('N/A', 0, 0, 0) # Defaults to empty mddata

        dodata = True # Only if dodata stays true we read data

        try: self.mode = xmlin.attribs['mode']
        except KeyError: self.mode = 'local'

        try: self.path = xmlin.attribs['path']
        except KeyError: self.path = '.'

        try: self.name = xmlin.attribs['name']
        except KeyError: self.name = ''

        try: self.type = xmlin.attribs['type']
        except KeyError: self.type = 'ipi'

        if not self.mode == 'local':
            warn_data_mode(self.mode)
            dodata = False

        if dodata:
            if self.type == 'ipi':
                self.data = ipi_mddata(self.path, str(xmlin.fields[0][1]).strip())

            else:
                warn_data_type(self.type)
