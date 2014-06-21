"""
A script designed to give information about MWRTA buses close to the 
Mathworks from the MWRTA mobile site, get a representative static image from 
Google maps, and calculate an estimated ETA using the Google distance matrix API.

Resources used: 
  http://code.google.com/apis/maps/documentation/staticmaps/
  https://developers.google.com/maps/documentation/distancematrix/
  http://www.geolabvirtualmaps.com/pda/metrowest.aspx

Adapted from: 
    http://hci574.blogspot.com/2010/04/using-google-maps-static-images.html
"""

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
#from Tkinter import *
#import Image, ImageTk

import re

ROUTE = 'RT01'
TABLE_ID = 'Table1'

mText = urlopen('http://www.geolabvirtualmaps.com/pda/metrowest.aspx')\
.read().decode('utf-8')

table = BeautifulSoup(mText).find(id=TABLE_ID)
buses = []

#need to get rid of tbody
for i in table.tbody.children:
  if( i == '\n'): continue
  if(i.td.string == ROUTE ):
    row = [cell.string for cell in i.children if cell != '\n']
    #only bothering with 8 directions here
    bus = (row[4].replace(' ','+'), row[5].split(' ')[0])
    buses.append(bus)


request = '''http://maps.googleapis.com/maps/api/staticmap?center=%22Mathworks+\
Natick,MA%22&size=640x640&markers=color:red|Mathworks&markers=color:green|{}'''\
.format(buses[0][0])

