from vqmd.mddata.ipi_mddata import ipi_mddata
from vqmd.core.warnings import *

class data(object):

    def __init__(self, xmlin, core, **kwargs):

        if xmlin[0]=='data':
            try: self.mode = xmlin[1].attribs['mode']
            except KeyError: self.mode = 'local'

            try: self.path = xmlin[1].attribs['path']
            except KeyError: self.path = '.'

            try: self.name = xmlin[1].attribs['name']
            except KeyError: self.name = ''

            try: self.type = xmlin[1].attribs['type']
            except KeyError: self.type = 'ipi'

            if not self.mode == 'local':
                warn_data_mode(self.mode)

            if self.type == 'ipi':
                self.data = ipi_mddata(self.path, str(xmlin[1].fields[0][1]).strip())

            else:
                warn_data_type(self.type)

        else:
            warn_wrong_xml(xmlin[0])
