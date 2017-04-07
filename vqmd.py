#!/usr/bin/python

"""
Main script which starts the data analysis and visualization tasks according to the given input XML file. 
Instead vwmd can also be imported as a python module and used as library, or instead as tool by passing a XML node object as input.

As a script run it on a terminal by:
    $ vqmd input.xml
where 'input.xml' should be replaced by the name of the xml input file which specifies the to-be-executed tasks. 
For an explanation of the XML input file format, see the reference documentation.

Functions:
   main: Runs the tool standalone, by XML input file.
   vqmd: Runs the tool after import, by XML node object.
"""

from pylab import *
from process.ipi_mddata import *
from tools.multigraph import *
   
#This is what is run if the file is run as a script.
if __name__ == '__main__':
   import sys
   if (len(sys.argv) != 2):
      print("Exactly one argument expected: The input file name.")
   else:
      main(sys.argv[1])

def main(file_name):
   from tools.xml_io import xml_parse_file

   ifile = open(file_name,"r")
   xmlin = xml_parse_file(ifile) # Parses the file.
   ifile.close()

   vqmd(xmlin)

def vqmd(xmlin):

   print(xmlin.fields[0][1].fields[0][1].fields)
   
   print(" --- begin input file content --- ")
   ifile = open(file_name,"r")
   for line in ifile.readlines():
      print(line,)
   ifile.close()
   print(" ---  end input file content  --- ")
   
   datafields = xmlin.fields[0][1].fields[0][1].fields
   
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
