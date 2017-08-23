"""
Main functions which start the data analysis and visualization tasks according to the given input XML file/node. 

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
