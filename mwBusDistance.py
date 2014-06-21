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

Uses BeautifulSoup for html and xml parsing, and pillow to display the images.
"""

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import BytesIO
from tkinter import *
from PIL import Image
from PIL import ImageTk


class MapFrame(Frame):
  def __init__(self, master, im):
    Frame.__init__(self, master)
    self.caption = Label(self, text='Distance Map')
    self.caption.grid()
    self.image = ImageTk.PhotoImage(im)
    self.image_label = Label(self, image=self.image, bd=0)
    self.image_label.grid()
    self.grid()

ROUTE = 'RT07'
TABLE_ID = 'Table1'
fromFile = False

if(fromFile):
  mText = urlopen('http://www.geolabvirtualmaps.com/pda/metrowest.aspx')\
  .read().decode('utf-8')
else:
  mText = open('mwrta.html').read()

table = BeautifulSoup(mText).find(id=TABLE_ID)
buses = []

#need to get rid of tbody
for i in table.children:
  if( i == '\n'): continue
  if(i.td.string == ROUTE ):
    row = [cell.string for cell in i.children if cell != '\n']
    #only bothering with 8 directions here
    bus = (row[4].replace(' ','+'), row[5].split(' ')[0])
    buses.append(bus)


request = '''http://maps.googleapis.com/maps/api/staticmap?center=%22Mathworks+\
Natick,MA%22&size=500x500&markers=color:red|Mathworks&markers=color:green|{}'''\
.format(buses[0][0])

imData = urlopen(request).read()
image = Image.open(BytesIO(imData))

mainw = Tk()
mainw.frame = MapFrame(mainw, image)
mainw.mainloop()


