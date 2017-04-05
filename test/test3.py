from pylab import *

from vqmd import *

testdata1 = ipi_mddata('test', 'hcpnoopt')
testdata2 = ipi_mddata('test', 'hcpwfopt')
testdata3 = ipi_mddata('test', 'mixwfopt')
testdata4 = ipi_mddata('test', 'atmwfopt')

fig = figure()
ax1 = fig.add_subplot(211)

naml = ['HCP-NOOPT-S0','HCP-WFOPT-S0','Mixed-WFOPT-S003','Atom-WFOPT-S003']

multiGraphXY(ax1, [testdata1.temp, testdata2.temp, testdata3.temp, testdata4.temp], names = naml, ylabel='Temperature [K]') 

ax2 = fig.add_subplot(212)

multiGraphXY(ax2, [testdata1.epot, testdata2.epot, testdata3.epot, testdata4.epot], ylabel='Potential Energy [H]', xlabel='Time [fs]')

#fig.savefig('test/wfopt_T_Epot.pdf')
fig.show()
