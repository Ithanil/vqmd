import os
import sys

# Check if vqmd is in path and add if not
dir_root = os.path.realpath(
               os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
if not dir_root in sys.path:
    sys.path.insert(0, dir_root)

import matplotlib.pyplot as plt
import pandas as pd
from vqmd.mddata.ipi_mddata import ipi_mddata

testdata1 = ipi_mddata('.', 'NFL')
testdata2 = ipi_mddata('.', 'DO')
testdata3 = ipi_mddata('.', 'LGV')
testdata4 = ipi_mddata('.', 'NONE')

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

tempdata = pd.DataFrame({'NFL' : testdata1.temp, 'DO' : testdata2.temp, 'LGV' : testdata3.temp, 'NONE' : testdata4.temp})
tempdata.plot(ax=ax1, legend=False)
plt.setp(ax1, ylabel='Temperature [K]', title='Noisy Force Langevin Test (HarmOsc Toy System)', yscale='log')

epotdata = pd.DataFrame({'NFL' : testdata1.epot, 'DO' : testdata2.epot, 'LGV' : testdata3.epot, 'NONE' : testdata4.epot})
epotdata.plot(ax=ax2, legend=True)
plt.setp(ax2, xlabel='Time [fs]', ylabel='Potential Energy [H]')

plt.show()
