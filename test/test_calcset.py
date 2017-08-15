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

testdata1.cellmat = [[1,0,0],[0,1,0],[0,0,1]]

testdata1.calcset_volume()
print(testdata1.volume)
