from pylab import *

from vqmd import *

testdata1 = ipi_mddata('test', 'sigtau1')
testdata2 = ipi_mddata('test', 'sigtau5')
testdata3 = ipi_mddata('test', 'sigtau10')
testdata4 = ipi_mddata('test', 'sigtau50')

fig = figure()
ax1 = fig.add_subplot(111)

naml = ['sigtau=1','sigtau=5','sigtau=10','sigtau=50']

multiGraphXY(ax1, [testdata1.temp, testdata2.temp, testdata3.temp, testdata4.temp], names = naml, ylabel='Temperature [K]', xlabel='Time [fs]') 

#savefig('test/sigtau_temp.pdf')
fig.show()
