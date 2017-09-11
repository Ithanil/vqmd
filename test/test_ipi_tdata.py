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

testdata1 = ipi_mddata('.', 'H2')

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

tempdata = pd.DataFrame({'H2' : testdata1.temp})
tempdata.plot(ax=ax1, legend=False)
plt.setp(ax1, ylabel='Temperature [K]', title='Noisy Force Langevin Test (HarmOsc Toy System)')

epotdata = pd.DataFrame({'H2' : testdata1.epot})
epotdata.plot(ax=ax2, legend=False)
plt.setp(ax2, ylabel='Potential Energy [H]')

etotdata = pd.DataFrame({'H2' : testdata1.etot})
etotdata.plot(ax=ax3, legend=False)
plt.setp(ax3, xlabel='Time [fs]', ylabel='Total Energy [H]')

plt.show()

