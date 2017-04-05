from pylab import *

from vqmd import *

testdata1 = ipi_mddata('test', 'sorella64_batopt')
testdata2 = ipi_mddata('test', 'sorella64_atmopt')
testdata3 = ipi_mddata('test', 'sorella64_batfix')

naml = ['BAT_OPT','ATM_OPT','BAT_FIX']

fig1 = figure()
ax1 = fig1.add_subplot(311)

multiGraphXY(ax1, [testdata1.epot, testdata2.epot, testdata3.epot], ylabel='Potential Energy [H]', title='Sorella 64H Mol rs=1.33 T=1200K') 

ax2 = fig1.add_subplot(312)

multiGraphXY(ax2, [testdata1.temp, testdata2.temp, testdata3.temp], names = naml, ylabel='Temperature [K]') 

ax3 = fig1.add_subplot(313)

multiGraphXY(ax3, [testdata1.pressmd, testdata2.pressmd, testdata3.pressmd], xlabel='Time [fs]', ylabel='Pressure [Pa]')

fig1.show()
