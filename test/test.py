#!/usr/bin/python

import os
import sys

# Check if vqmd is in path and add if not
dir_root = os.path.realpath(
               os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
if not dir_root in sys.path:
    sys.path.insert(0, dir_root)

from vqmd import vqmd_node
from vqmd.lib.xml_io import xml_parse_file

if __name__ == '__main__':
    import test_mddata as tm
    import test_ipi_mddata as tim
    with open('test_ipi_mddata.xml','r') as xmlfile:
        xmlin = xml_parse_file(xmlfile)
        vqmd_node(xmlin)
    import test_ipi_tdata as tit
