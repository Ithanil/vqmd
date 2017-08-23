from vqmd.core.read import read
from vqmd.core.view import view
from vqmd.core.warnings import *

class core(object):

    def __init__(self, xmlin, **kwargs):

        for xmlfield in xmlin.fields[0][1].fields:
            if xmlfield[0].strip().lower() == 'read':
                if hasattr(self, 'read'):
                    warn_mult_xml('read')
                self.read = read(xmlfield[1], self)

            elif xmlfield[0].strip().lower() == 'calc':
                if hasattr(self, 'calc'):
                    warn_mult_xml('calc')
                if not hasattr(self, 'read'):
                    warn_miss_xml('read', 'calc')
                self.calc = None #Not implemented yet

            elif xmlfield[0].strip().lower() == 'view':
                if hasattr(self, 'view'):
                    warn_mult_xml('view')
                if not hasattr(self, 'read'):
                    warn_miss_xml('read', 'view')
                self.view = view(xmlfield[1], self)

            else:
                warn_wrong_xml(xmlfield[0])
