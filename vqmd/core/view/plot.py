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
                    print('Viewing of non-tssprops still to be implemented.')

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
