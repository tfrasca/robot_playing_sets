import cv2
import numpy as np
from matplotlib import pyplot as plt

everySet = []
def matShow(imgs):
  num = len(imgs)
  full = num/2
  if num%2 == 1:
    full += 1
  plt.axis("off")
  for x in xrange(num):
    plt.subplot(full,2,x+1)
    plt.imshow(imgs[x],'gray')
    plt.xticks([])
    plt.yticks([])
  plt.show()

def show(img, title="image", timeout=0):
  cv2.imshow(title, img)
  cv2.waitKey(timeout)
  cv2.destroyAllWindows()

def initializeColorThresholds(img):
  print "image to get colors from"
  show(img)
  print "image to get colors from"
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  cv2.namedWindow('image')
  redHSV = []     #136,40,154       193,201,212
  greenHSV = []   #58,58,148        94,189,177
  purpleHSV = []  #113,51,131       153,193,200
    
  # create trackbars for color change
  cv2.createTrackbar('minH red=136 green=58 purple=113','image',0,255,nothing)
  cv2.createTrackbar('maxH red=193 green=94 purple=153','image',255,255,nothing)
  cv2.createTrackbar('minS red=40 green=58 purple=51','image',0,255,nothing)
  cv2.createTrackbar('maxS red=201 green=189 purple=193','image',255,255,nothing)
  cv2.createTrackbar('minV red=154 green=148 purple=131','image',0,255,nothing)
  cv2.createTrackbar('maxV red=212 green=177 purple=200','image',255,255,nothing)
  print """move the trackbars to change thresholds\nonce sufficient threshold found, with image in focus,
         hit 'r' to set the red threshold
         hit 'g' to set the green theshold
         hit 'p' to set the purple theshold
         hit 'esc' to finish and return thesholds """
  while True:
    minH = cv2.getTrackbarPos('minH red=136 green=58 purple=113','image')
    maxH = cv2.getTrackbarPos('maxH red=193 green=94 purple=153','image')
    minS = cv2.getTrackbarPos('minS red=40 green=58 purple=51','image')
    maxS = cv2.getTrackbarPos('maxS red=201 green=189 purple=193','image')
    minV = cv2.getTrackbarPos('minV red=154 green=148 purple=131','image')
    maxV = cv2.getTrackbarPos('maxV red=212 green=177 purple=200','image')

    minHSV = np.array([minH,minS,minV])
    maxHSV = np.array([maxH,maxS,maxV])

    colorImg = cv2.inRange(hsv, minHSV, maxHSV)
    cv2.imshow('image',colorImg)
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == 10:
      break
    elif k == 103:
      print "setting green"
      greenHSV.append(minHSV)
      greenHSV.append(maxHSV)
      print greenHSV
    elif k == 112:
      print "setting purple"
      purpleHSV.append(minHSV)
      purpleHSV.append(maxHSV)
      print purpleHSV
    elif k == 114:
      print "setting red"
      redHSV.append(minHSV)
      redHSV.append(maxHSV)
      print redHSV

  cv2.destroyAllWindows()
  return [redHSV,greenHSV,purpleHSV]
  
def nothing(x):
  pass

def initializeGrayThresholds(img):
  print "image to get colors from"
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  cv2.namedWindow('image')
  out = [166,255]
  # create trackbars for color change
  cv2.createTrackbar('min','image',out[0],255,nothing)
  cv2.createTrackbar('max','image',out[1],255,nothing)
  print """move the trackbars to change thresholds\nonce sufficient threshold found, with image in focus,
         hit 'h' to set the high threshold
         hit 'l' to set the low theshold
         hit 'esc' to finish and return thesholds """
  while True:
    low = cv2.getTrackbarPos('min','image')
    high = cv2.getTrackbarPos('max','image')
    out = []
    t,colorImg = cv2.threshold(hsv, low, high, cv2.THRESH_BINARY)
    cv2.imshow('image',colorImg)
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == 10:
      break
    elif k == 108:
      print "setting low"
      out.append(low)
      print low
    elif k == 104:
      print "setting high"
      out.append(high)
      print high
  cv2.destroyAllWindows()
  return [low,high]

def createCardROIs(numRows, numCols, startY=0, endY=1080, startX=0, endX=1920):
  roi = []
  deltaX = (endX - startX)/numCols
  deltaY = (endY - startY)/numRows
  print startY, endY, startX, endX
  for row in xrange(numRows):
    yStart = startY + deltaY * row
    yEnd   = yStart + deltaY
    for col in xrange(numCols):
      xStart = startX + deltaX * col
      xEnd = xStart + deltaX
      roi.append((yStart,yEnd,xStart,xEnd))
  return roi

def readAllSets():
  with open("sets.txt") as f:
    x = f.readline()
    while x:
      vals = x.strip("\n").split(",")
      out = []
      for v in vals:
        out.append(int(v))
      everySet.append(out)
      x = f.readline()

def findSets(cards):
  allSets = []
  for i in range(len(cards)-2):
    for j in range(i+1,(len(cards)-1)):
      for k in range(j+1,len(cards)):
        isSet = [cards[i], cards[j], cards[k]]
        try:
          if everySet.index(isSet) > 0:
            allSets.append([i, j, k])
        except ValueError:
          pass 
  return allSets
