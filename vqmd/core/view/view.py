"""
This class is the top level of data visualization structures

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.
"""

from vqmd.core.view.fig import fig
from vqmd.core.warnings import *
import matplotlib.pyplot as plt

class view(object):

    def __init__(self, xmlin, core, **kwargs):

        self.figs = []

        for xmlfield in xmlin.fields:
            if xmlfield[0] == 'fig':
                self.figs.append(fig(xmlfield[1], core))

            else:
                warn_wrong_xml(xmlfield[0])

        plt.show()
