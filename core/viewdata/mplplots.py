from pylab import *
import pandas as pd

class mplplot(object):

    def __init__(self, xmlin, rawdata, calcdata, **kwargs):

        self.fig = figure()
        self.axs = []

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

                pltdict = {}
                pltobs = eval(xmlfield[1].fields[0][1])
                if isinstance(pltobs, str): pltobs = [pltobs]

                for mddata in rawdata.data:
                    for obs in pltobs:
                        datname = mddata.name
                        if len(pltobs)>1:
                            datname += " " + obs
                        pltdict[datname]=getattr(mddata.data, obs)
                pltdata = pd.DataFrame(pltdict)

                try: dolegend = xmlfield[1].attribs['legend'].strip().lower() == 'true'
                except KeyError: dolegend = False

                itax += 1
                newax = self.fig.add_subplot(nax, 1, itax)
                pltdata.plot(ax=newax, legend=dolegend)

                try: newax.set_xlabel(xmlfield[1].attribs['xlabel'])
                except KeyError: pass

                try: newax.set_ylabel(xmlfield[1].attribs['ylabel'])
                except KeyError: pass

                try: newax.set_xscale(xmlfield[1].attribs['xscale'])
                except KeyError: pass

                try: newax.set_yscale(xmlfield[1].attribs['yscale'])
                except KeyError: pass

                self.axs.append(newax)

class mplplots(object):

    def __init__(self, xmlin, rawdata, calcdata, **kwargs):

        self.plots = []

        for xmlfield in xmlin.fields:
            if xmlfield[0] == 'fig':
                self.plots.append(mplplot(xmlfield[1], rawdata, calcdata))

        show()
