"""
This class handles the figure level of data plotting

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.

"""


import matplotlib.pyplot as plt
from vqmd.core.view.plot import plot
from vqmd.core.warnings import *

class fig(object):

    def __init__(self, xmlin, core, **kwargs):

        self.fig = plt.figure()
        self.plots = []

        try: self.fig.suptitle(xmlin.attribs['title'])
        except KeyError: pass

        # first count the number of axes
        nax = 0
        for xmlfield in xmlin.fields:
            if xmlfield[0] == 'plot':
                nax += 1

        itax = 0
        for xmlfield in xmlin.fields:
            if xmlfield[0] == 'plot':
                itax += 1
                newax = self.fig.add_subplot(nax, 1, itax)
                self.plots.append(plot(xmlfield[1], core, newax))
