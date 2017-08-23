from vqmd.mddata import mddata
from vqmd.mddata.ipi_mddata import ipi_mddata
from vqmd.core.warnings import *

import subprocess

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
            remote = xmlin.attribs['remote']
            try: port = xmlin.attribs['port']
            except KeyError: port = '22'

            if self.mode == 'scp':
                subprocess.run(["scp", "-rp", port, remote + '/.', self.path])
            elif self.mode == 'rsync':
                try: rsynce = xmlin.attribs['rsync-e']
                except KeyError: rsynce = "ssh -p " + port
                subprocess.run(["rsync", "-rve", rsynce, remote + '/', self.path])
            else:
                warn_data_mode(self.mode)
                dodata = False

        if dodata:
            if self.type == 'ipi':
                self.data = ipi_mddata(self.path, str(xmlin.fields[0][1]).strip())

            else:
                warn_data_type(self.type)
