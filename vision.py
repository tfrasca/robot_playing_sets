import cv2
import numpy as np
from matplotlib import pyplot as plt
import util
from colorlabeler import ColorLabeler
import imutils

shapes = [0,0]

class CardClassifier(object):
  def __init__(self, **kwargs):
    self.trainingShapes = []
  def getCardContours(self,img, imgOG):
    cards = []
    minAreaThresh = 1500
    maxAreaThresh = 8000
    cardMinThresh = 23000
    cardMaxThresh = 33000
    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
      hierarchy = hierarchy[0]
    except TypeError:
      print "no contours found"
      return []
    index = 0
    contourAreas = self.getContourAreas(contours)
    elems = []
    for contLevel in hierarchy:
      if contLevel[3] == -1:
        contourArea = contourAreas[index]
        if contourArea > cardMinThresh and contourArea < cardMaxThresh:
          hasChild = True
          nextChild = contLevel[2]
          if nextChild == -1:
            hasChild = False
          while hasChild:
            child = hierarchy[nextChild]
            contour = contours[nextChild]
            if contourAreas[nextChild] > minAreaThresh:
              elems.append(contour)
              img2 = imgOG.copy()
              cv2.drawContours(img2, [contour], -1, (0,255,255),3)
              #util.show(img2)
            nextChild = child[0]
            if nextChild == -1:
              hasChild = False
      index+=1
    return elems

  def getContourAreas(self,contours):
    out = []
    for contour in contours:
      out.append(cv2.contourArea(contour))
    return out


  def detectColor(self,contours, img):
    colors = [0,0,0]
    for contour in contours:
      mom = cv2.moments(contour)
      cx = int(mom['m10']/mom['m00'])
      cy = int(mom['m01']/mom['m00'])
      i2 = cv2.drawContours(img,[contour],-1,(255,0,255),3)
      cv2.circle(img,(cx,cy),5,(0,255,255),3)
      #print cy,cx
      pix = img[cy,cx]
      #print pix
      if pix[2] > 150:
        color = "red"
        colors[0] = colors[0] + 1
      elif pix[1] > 110 and 3:
        color = "green"
        colors[1] = colors[1] + 1
      else:
        color = "purple"
        colors[2] = colors[2] + 1
      print color
      #util.show(img)
    #print colors
    if colors[0] > colors[1]:
      if colors[0] > colors[2]:
        return 1
      return 3
    else:
      if colors[1] > colors[2]:
        return 2
      return 3

  def modEdges(self,edges):
    kernel = np.ones((1,1),np.uint8)
    #e0 = edges.copy()
    #e0 = cv2.erode(e0,kernel, iterations = 1)
    #e1 = cv2.dilate(e0,kernel, iterations =2)
    e2 = edges.copy()
    e2 = cv2.dilate(e2,kernel, iterations = 1)
    e3 = cv2.erode(e2,kernel, iterations =1)
    return e3

  def classifyColor(self,img, colorThresholds):
    index = 0
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    util.show(hsv)
    for colorThresh in colorThresholds:
      minHSV = np.array(colorThresh[0])
      maxHSV = np.array(colorThresh[1])
      colorImg = cv2.inRange(hsv, minHSV, maxHSV)
      util.show(colorImg)
      imgout, contours, hierarchy = cv2.findContours(colorImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      try:
        #print "trying"
        for contour in contours:
          #print "contour"
          cv2.drawContours(colorImg, [contour], -1, (0,255,255),3)
          #x,y,w,h = cv2.boundingRec(contour)
          #cv2.rectangle(colorImg,(x,y),(x+w,y+h),(0,255,0),2)
          util.show(colorImg)
        contourAreas = self.getContourAreas(contours)
        contourAreas.sort()
        contourAreas.reverse()
        if len(contourAreas) >0:
          #print "there are contours for this color"
          if contourAreas[0] > 750:
            return index
      except TypeError:
        print "passing"
        pass
      index += 1


  def nn(self,contours,k):
  # shape, contour
    similarities = []
    shapeClass = [0,0,0]
    for contour in contours:

      for shape in self.trainingShapes:
        similar = cv2.matchShapes(contour,shape[1], 2, 0.0)
        similarities.append([similar,shape[0]])
      similarities.sort()
      if len(similarities) >= k:
        for x in xrange(k):
          #print similarities[x]
          try:
            c = int(similarities[x][1])-1
          except ValueError:
            continue
          shapeClass[c] = shapeClass[c] +1
    if shapeClass[0] > shapeClass[1]:
      if shapeClass[0] > shapeClass[2]:
        return 1
      return 2
    else:
      if shapeClass[1] > shapeClass[2]:
        return 2
      return 3

  def createTrainingShapes(self, img, grayThresh):
    imgog = img.copy()
    imgG  = cv2.cvtColor(imgog, cv2.COLOR_BGR2GRAY)
    t, imgG  = cv2.threshold(imgG, grayThresh[0],grayThresh[1],cv2.THRESH_BINARY)
    imgMod = self.modEdges(imgG)
    contours = self.getCardContours(imgMod,img)
    util.show(img)
    shape = raw_input("shape")
    for contour in contours:
      a = raw_input("add shape? [y]/n")
      if a =="y" or a =="":
        self.trainingShapes.append((shape,contour))

  def classifyCard(self,img, colorThresh, grayThresh):
    # get color
    #print "class cards"
    #colorimg = img.copy()
    #color = self.classifyColor(colorimg, colorThresh)
    #print "color",color

    # find number of elements and the shape
    imgog = img.copy()
    imgG  = cv2.cvtColor(imgog, cv2.COLOR_BGR2GRAY)
    t, imgG  = cv2.threshold(imgG, grayThresh[0],grayThresh[1],cv2.THRESH_BINARY)
    imgMod = self.modEdges(imgG)
    contours = []
    contours = self.getCardContours(imgMod,img)
    #mask = np.zeros(imgray.shape,np.uint8)
    shape = self.nn(contours,3)*100
    shape += len(contours)*10
    #print "shape,number",shape
    shape += self.detectColor(contours, img)
    print "shape,number, color",shape
    #util.show(img)
    #act_shape = raw_input("what is color/fill ")
    #if act_shape == "":
    #  return shape
    #else:
    #  try:
    #    if int(act_shape) > 1000:
    #      return int(act_shape)
    #    shape += int(act_shape)
    #  except ValueError:
    #    return shape
    print "code ",shape
    return shape
