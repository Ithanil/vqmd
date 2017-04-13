from pylab import *

from vqmd import *

testdata1 = ipi_mddata('test', 'mdfile_NFL')
testdata2 = ipi_mddata('test', 'mdfile_DO')
testdata3 = ipi_mddata('test', 'mdfile_LGV')
testdata4 = ipi_mddata('test', 'mdfile_NONE')

naml = ['NFL','DO','LGV','NONE']

fig1 = figure()
ax1 = fig1.add_subplot(111)

multiGraphXY(ax1, [testdata1.temp, testdata2.temp, testdata3.temp, testdata4.temp], names = naml, xlabel='Time [fs]', ylabel='Temperature [K]', title='Noisy Langevin Thermostat Test (HarmOsc Toy System)', yscale='log') 

#fig1.savefig('test/ThermoTest_log.pdf')
fig1.show()

fig2 = figure()
ax2 = fig2.add_subplot(111)

multiGraphXY(ax2, [testdata1.temp, testdata2.temp], names = naml, xlabel='Time [fs]', ylabel='Temperature [K]', title='Noisy Langevin Thermostat Test (HarmOsc Toy System)') 

#fig2.savefig('test/ThermoTest.pdf')
fig2.show()
