import cv2
import numpy as np
from matplotlib import pyplot as plt
import util
from colorlabeler import ColorLabeler
import imutils

shapes = [0,0]

# classify the cards
class CardClassifier(object):
  def __init__(self, **kwargs):
    self.trainingShapes = []

  # get the contours on the cards which are on the second hierarchical layer
  # this filters out noise and returns only the contours for the elements on the card
  def getCardContours(self,img, imgOG):
    cards = []
    minAreaThresh = 1500
    maxAreaThresh = 8000
    cardMinThresh = 23000
    cardMaxThresh = 33000
    # get contours
    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
      hierarchy = hierarchy[0]
    except TypeError:
      print "no contours found"
      return []
    index = 0
    # find the areas for each contour
    contourAreas = self.getContourAreas(contours)
    elems = []
    # evaluate the hierarchical level of the contour
    # contours [next contour on same level, previous, first child, parent]
    for contLevel in hierarchy:
      # if there is no parent, then it is on the top level
      if contLevel[3] == -1:
        contourArea = contourAreas[index]
        # only keep the cards on the top level if area is within threshold
        if contourArea > cardMinThresh and contourArea < cardMaxThresh:
          hasChild = True
          nextChild = contLevel[2]
          # check to see if this card has any children
          if nextChild == -1:
            hasChild = False
          # find all the children contours
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
      pix = img[cy,cx]
      # very naive color checking
      # find the center and evaluate the rgb values
      if pix[2] > 150:
        color = "red"
        colors[0] = colors[0] + 1
      elif pix[1] > 110 and 3:
        color = "green"
        colors[1] = colors[1] + 1
      else:
        color = "purple"
        colors[2] = colors[2] + 1
      #print color
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
    # this method does nothing need to change the kernel size if it should work
    kernel = np.ones((1,1),np.uint8)
    e2 = edges.copy()
    e2 = cv2.dilate(e2,kernel, iterations = 1)
    e3 = cv2.erode(e2,kernel, iterations =1)
    return e3

  #def classifyColor(self,img, colorThresholds):
  #  index = 0
  #  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  #  util.show(hsv)
  #  for colorThresh in colorThresholds:
  #    minHSV = np.array(colorThresh[0])
  #    maxHSV = np.array(colorThresh[1])
  #    colorImg = cv2.inRange(hsv, minHSV, maxHSV)
  #    util.show(colorImg)
  #    imgout, contours, hierarchy = cv2.findContours(colorImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #    try:
  #      #print "trying"
  #      for contour in contours:
  #        #print "contour"
  #        cv2.drawContours(colorImg, [contour], -1, (0,255,255),3)
  #        #x,y,w,h = cv2.boundingRec(contour)
  #        #cv2.rectangle(colorImg,(x,y),(x+w,y+h),(0,255,0),2)
  #        util.show(colorImg)
  #      contourAreas = self.getContourAreas(contours)
  #      contourAreas.sort()
  #      contourAreas.reverse()
  #      if len(contourAreas) >0:
  #        #print "there are contours for this color"
  #        if contourAreas[0] > 750:
  #          return index
  #    except TypeError:
  #      #print "passing"
  #      pass
  #    index += 1


  # simple nearest neighbor classifier
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

  #create the training samples for nearest neighbors
  def createTrainingShapes(self, img, grayThresh):
    imgog = img.copy()
    imgG  = cv2.cvtColor(imgog, cv2.COLOR_BGR2GRAY)
    t, imgG  = cv2.threshold(imgG, grayThresh[0],grayThresh[1],cv2.THRESH_BINARY)
    imgMod = self.modEdges(imgG)
    contours = self.getCardContours(imgMod,img)
    util.show(img)
    waitForShape = True
    while waitForShape:
      shape = raw_input("shape: ")
      print shape
      if not shape == "":
        waitForShape= False
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
    #print "shape,number, color",shape
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
    #print "code ",shape
    return shape
