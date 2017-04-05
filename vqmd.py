#!/usr/bin/python

"""Main script from which the simulation is run.

Deals with creation of the simulation object, reading the input file and
initialising the system.

Run using:
      i-pi input_file.xml

Where 'input_file.xml' should be replaced by the name of the xml input file from
which the system data will be read. For a description of how the input file
should be formatted, see the reference manual.

Functions:
   main: Runs the simulation.
"""

from pylab import *
from process.ipi_mddata import *
from tools.multigraph import *

def main(file_name):
   from tools.xml_io import xml_parse_file

   ifile = open(file_name,"r")
   xmlrestart = xml_parse_file(ifile) # Parses the file.
   ifile.close()

   # Checks the input and partitions it appropriately.
   print(xmlrestart.fields[0][1].fields[0][1].fields)
   
   print(" --- begin input file content --- ")
   ifile = open(file_name,"r")
   for line in ifile.readlines():
      print(line,)
   ifile.close()
   print(" ---  end input file content  --- ")
   
   datafields = xmlrestart.fields[0][1].fields[0][1].fields
   
   mymddata = []
   naml = []
   
   for dataset in datafields:
      if dataset[0]=='data':
         print(dataset[1].attribs['path'])
         print(dataset[1].attribs['name'])
         naml.append(dataset[1].attribs['name'])
         mymddata.append(ipi_mddata(dataset[1].attribs['path'], dataset[1].fields[0][1]))
   
   tempdata = []
   potdata = []
   
   for mddata in mymddata:
      tempdata.append(mddata.temp)
      potdata.append(mddata.epot)
      
   fig = figure('Sorella 64H Mol rs=1.33 T=1200K')
   ax1 = fig.add_subplot(211)
   ax2 = fig.add_subplot(212)
   
   multiGraphXY(ax1, tempdata, names = naml, ylabel='Temperature [K]', title='Sorella 64H Mol rs=1.33 T=1200K') 
   multiGraphXY(ax2, potdata, xlabel='Time [fs]', ylabel='Potential Energy [H]')

   show()
   
#This is what is run if the file is run as a script.
if __name__ == '__main__':
   import sys
   if (len(sys.argv) != 2):
      print("Exactly one argument expected: The input file name.")
   else:
      main(sys.argv[1])
