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
