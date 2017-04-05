from pylab import *

from vqmd import *

testdata1 = ipi_mddata('test', 'test1')
testdata2 = ipi_mddata('test', 'test2')

fig = figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

naml = ['test1','test2']

multiGraphXY(ax1, [testdata1.temp, testdata2.temp], names = naml, ylabel='Temperature [K]') 
multiGraphXY(ax2, [testdata1.epot, testdata2.epot], names = naml, xlabel='Time [fs]', ylabel='Pot. Energy [H]') 

fig.show()
