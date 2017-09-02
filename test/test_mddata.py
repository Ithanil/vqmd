import os
import sys

# Check if vqmd is in path and add if not
dir_root = os.path.realpath(
               os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
if not dir_root in sys.path:
    sys.path.insert(0, dir_root)

from vqmd.mddata import mddata

if __name__ == '__main__':
    mydata1 = mddata('mydata1', 1, 2, 3, volume = 1.0, density = 1.0, tcellmat = [[0,1],[[[1,0,0],[0,1,0],[0,0,1]], [[1,1,0],[0,1,0],[0,0,1]]]], temp=[[0,1,2],[100,200,300]])
    mydata2 = mddata('mydata2', 1, 2, 3, cellmat = [[1,0,0],[0,1,0],[0,0,1]], cmasses = [1.0])
    mydata3 = mddata('mydata3', 1, 2, 3, cellmat = [[1,0,0],[0,1,0],[0,0,1]], bmasses = [[0.5,0.5]])    

    mydata1.volume
    mydata2.volume

    mydata1.density
    mydata2.density
    mydata3.density
