"""
The core class is the top level of structures which handle the instructions from XML input files

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.

"""

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
