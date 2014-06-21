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


ROUTE = 'RT07'
TABLE_ID = 'Table1'
FROM_FILE = False
REFRESH_TIME = 1

class MapFrame(Frame):
  def __init__(self, master, im):
    Frame.__init__(self, master)
    self.caption = Label(self, text='Distance Map')
    self.caption.grid()
    self.image = ImageTk.PhotoImage(im)
    self.image_label = Label(self, image=self.image, bd=0)
    self.image_label.grid()
    self.grid()


'''Returns a list of tuples in the form of (bus address, travel direction)'''
def getBusData(route, debugFromFile=False, tableID='Table1'):
  if(not debugFromFile):
    mText = urlopen('http://www.geolabvirtualmaps.com/pda/metrowest.aspx')\
    .read().decode('utf-8')
  else:
    mText = open('mwrta.html').read()

  table = BeautifulSoup(mText).find(id=tableID)
  buses = []
  for i in table.children:
    if( i == '\n'): continue
    if(i.td.string == ROUTE ):
      row = [cell.string for cell in i.children if cell != '\n']
      #only bothering with 8 directions here
      bus = (row[4].replace(' ','+'), row[5].split(' ')[0])
      buses.append(bus)
  return buses

'''Takes the default request line and adds markers for the buses.'''
def getRequestLine(buses):
  request = ('''http://maps.googleapis.com/maps/api/staticmap?center=%22'''
  '''Mathworks+Natick,MA%22&size=500x500&markers=color:red|Mathworks''')

  for bus in buses:
    request += '&markers=color:green|{}'.format(bus[0])
  return request

def updateImage():
  buses = getBusData(ROUTE, FROM_FILE, TABLE_ID)
  if(buses):
    requestLine = getRequestLine(buses)
    imData = urlopen(requestLine).read()
    image = Image.open(BytesIO(imData))
    return image
  else:
    return None

def updateWindow(window):
  window.frame.destroy()
  window.frame = MapFrame(window,updateImage()) 
  window.after(1000, updateWindow, window)

def main():
  image = updateImage()
  mainw = Tk()
  mainw.frame = MapFrame(mainw, image)
  mainw.after(1000, updateWindow, mainw)
  mainw.mainloop();

if __name__ == '__main__':
  main()