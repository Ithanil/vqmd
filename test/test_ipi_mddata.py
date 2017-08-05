from pylab import *
from vqmd import *

testdata1 = ipi_mddata('test', 'NFL')
testdata2 = ipi_mddata('test', 'DO')
testdata3 = ipi_mddata('test', 'LGV')
testdata4 = ipi_mddata('test', 'NONE')

fig = figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

tempdata = pd.DataFrame({'NFL' : testdata1.temp, 'DO' : testdata2.temp, 'LGV' : testdata3.temp, 'NONE' : testdata4.temp})
tempdata.plot(ax=ax1)
setp(ax1, ylabel='Temperature [K]', title='Noisy Langevin Thermostat Test (HarmOsc Toy System)', yscale='log')

epotdata = pd.DataFrame({'NFL' : testdata1.epot, 'DO' : testdata2.epot, 'LGV' : testdata3.epot, 'NONE' : testdata4.epot})
epotdata.plot(ax=ax2)
setp(ax2, xlabel='Time [fs]', ylabel='Potential Energy [H]')

legend(['NFL','DO','LGV','NONE'])

fig.show()
