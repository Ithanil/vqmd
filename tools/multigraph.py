from pylab import *
from tools.helpers import *


def axplot(ax, xdata=None, ydata=array([])):
    
    if xdata is None:
        ax.plot(ydata)
    else:
        ax.plot(xdata, ydata)
    
    return ax


def setax(ax, names, **kwargs):

    if names is not None:
        ax.legend(names)
    ax.set(**kwargs)
    
    return ax


def multiGraphS(ax, xdata=None, ydata=array([]), names=None, **kwargs):
    
    axplot(ax, xdata, ydata)
    setax(ax, names, **kwargs)
    
    return ax


def multiGraphM(ax, xdata=None, ydata=[], names=None, **kwargs):
    
    ngraphs = len(ydata)
    
    for itg in range(ngraphs):
        axplot(ax, xdata[itg], ydata[itg])
    
    setax(ax, names, **kwargs)
    
    return ax


def multiGraph(ax, xdata=None, ydata=[], names=None, **kwargs):

    if iter_ndim(ydata) == 1:
        multiGraphS(ax, xdata, array(ydata), names, **kwargs)
    
    elif iter_ndim(ydata) == 2:
        multiGraphM(ax, xdata, ydata, names, **kwargs)
    
    else:
        raise ValueError('multiGraph: ydata dimension must be 1 or 2')
    
    return ax


def multiGraphXY(ax, xydata=[], names=None, **kwargs):

    xhelp = []
    yhelp = []

    if iter_ndim(xydata) == 2:
        xhelp.append(xydata[:,0])
        yhelp.append(xydata[:,1])
        
    elif iter_ndim(xydata) == 3:
        for xyline in xydata:
            xhelp.append(xyline[:,0])
            yhelp.append(xyline[:,1])
        
    multiGraph(ax, array(xhelp), array(yhelp), names, **kwargs)
        
    return ax


def testGraph():
    fig = figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    multiGraph(ax1, array([1,2,3]), array([1,2,3]), title=r'$H_2$ Test MD', ylabel='Temperature [K]', xscale='log', yscale='log', xlim=[0.9,3], ylim=[0.9,3])
    multiGraph(ax2, array([[1,2,3], [4,5,6], [7,8,9]]), array([[1,2,3], [4,5,6], [7,8,9]]), ['123','456','789'], xlabel='Time [fs]', ylabel='Temperature [K]', xlim=[0.9,10], ylim=[0.9,10])
    multiGraphXY(ax3, array([[[1,1],[2,2],[3,3]], [[4,4],[5,5],[6,6]], [[7,7],[8,8],[9,9]]]), ['123','456','789'], xlabel='Time [fs]', ylabel='Temperature [K]', xlim=[0.9,10], ylim=[0.9,10])
    show()

#testGraph()
