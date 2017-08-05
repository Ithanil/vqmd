#!/usr/bin/python

from vqmd import vqmd
from libs.xml_io import xml_parse_file

import test.test_ipi_mddata

with open('test/test_ipi_mddata.xml','r') as xmlfile:
    xmlin = xml_parse_file(xmlfile)
    vqmd(xmlin)
