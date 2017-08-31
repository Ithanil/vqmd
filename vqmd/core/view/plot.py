"""
This class handles the plot level of data plotting

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.

"""

import pandas as pd
from vqmd.core.warnings import *

class plot(object):

    def __init__(self, xmlin, core, newax, **kwargs):

        self.pltobs = eval(xmlin.fields[0][1])
        self.ax = newax

        pltdict = {}
        if isinstance(self.pltobs, str): self.pltobs = [self.pltobs]

        for mddata in core.read.datas:
            for obs in self.pltobs:
                if obs in mddata.data.tssprops:
                    datname = mddata.name
                    if len(self.pltobs)>1:
                        datname += " " + obs
                    pltdict[datname]=getattr(mddata.data, obs)
                else:
                    if obs in mddata.data.props:
                        print('Plotting non-tssprops not yet implemented.')
                    else:
                        print('\'' + obs + '\' is not a property of the provided mddata object with name \'' + mddata.name + '\'. Did nothing.')

        pltdata = pd.DataFrame(pltdict)

        try: dolegend = xmlin.attribs['legend'].strip().lower() == 'true'
        except KeyError: dolegend = False

        pltdata.plot(ax=self.ax, legend=dolegend)

        try: self.ax.set_title(xmlin.attribs['title'])
        except KeyError: pass

        try: self.ax.set_xlabel(xmlin.attribs['xlabel'])
        except KeyError: pass

        try: self.ax.set_ylabel(xmlin.attribs['ylabel'])
        except KeyError: pass

        try: self.ax.set_xscale(xmlin.attribs['xscale'])
        except KeyError: pass

        try: self.ax.set_yscale(xmlin.attribs['yscale'])
        except KeyError: pass
