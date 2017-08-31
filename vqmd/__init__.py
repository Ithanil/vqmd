"""
Main functions which start the data analysis and visualization tasks according to the given input XML file/node

Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.

Functions:
   vqmd_node: Runs the tool by XML node object.
   vqmd_file: Runs the tool by XML input file.
"""

from vqmd.core import core
from lib.xml_io import xml_parse_file

def vqmd_node(xmlin):

   mycore = core(xmlin)

def vqmd_file(filename):

   with open(filename,"r") as ifile:
      print(" --- begin input file content --- ")
      for line in ifile.readlines():
         print(line,)
      print(" ---  end input file content  --- ")
      ifile.seek(0)
      xmlin = xml_parse_file(ifile) # Parses the file.

   vqmd_node(xmlin)
