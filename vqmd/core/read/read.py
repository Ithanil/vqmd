"""
This class is the top level of data input structures

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.
"""

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
