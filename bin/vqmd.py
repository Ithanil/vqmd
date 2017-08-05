#!/usr/bin/python

"""
Main script which starts the data analysis and visualization tasks according to the given input XML file. 
Instead vqmd can also be imported as a python module and used as library, or instead as tool by passing a XML node object as input.

As a script run it on a terminal by:
    $ vqmd input.xml
where 'input.xml' should be replaced by the name of the xml input file which specifies the to-be-executed tasks. 
For an explanation of the XML input file format, see the documentation.

Functions:
   main: Runs the tool standalone, by XML input file.
   vqmd: Runs the tool after import, by XML node object.
"""

from pylab import *
from core.core import *

def vqmd(xmlin):

   mycore = core(xmlin)

def runfile(filename):
   from libs.xml_io import xml_parse_file

   with open(filename,"r") as ifile:
      print(" --- begin input file content --- ")
      for line in ifile.readlines():
         print(line,)
      print(" ---  end input file content  --- ")
      ifile.seek(0)
      xmlin = xml_parse_file(ifile) # Parses the file.

   vqmd(xmlin)


#This is what is run if the file is run as a script.
if __name__ == '__main__':
   import sys
   if (len(sys.argv) != 2):
      print("Exactly one argument expected: The input file name.")
   else:
      runfile(sys.argv[1])
