import cv2
import numpy as np
from matplotlib import pyplot as plt
import util


class CardClassification(object):
  # height loc (row) / width loc (column)
  #ROI = [(0,216,575,912,1250)(0,216,575,912,1250)(0,216,575,912,1250)]
        #[0:1080,575:1250]

  def printSimilarities(self, contours):
    breakLoop = False
    for contour in contours:
      print "next contour\n"
      if breakLoop:
        break
      for cont in contours:
        if breakLoop:
          break
        print ("{:.3f}\t\t{:.3f}".format(cv2.matchShapes(contour,cont, 1, 0.0), cv2.matchShapes(contour,cont, 2, 0.0)))
        inp = raw_input()
        if not (inp  == ''):
          breakLoop = True


  def getCardContours(self, img, imgOG):
    cards = []
    minAreaThres = 4000
    maxAreaThres = 8000
    cardMinThres = 45000
    cardMaxThres = 60000
    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
      hierarchy = hierarchy[0]
    except TypeError:
      print "wtf is going on"
      return
    index = 0
    elems = ()
    contourAreas = self.getContourAreas(contours)

    for contLevel in hierarchy:
      contour = contours[index]
      contourArea = cv2.contourArea(contour)
      img2 = imgOG.copy()
      cv2.drawContours(img2, [contour], -1, (0,255,255),3)
      contourArea = contourAreas[index]
      # need to check that it is in the outter most layer
      if contourArea > cardMinThres and contourArea < cardMaxThres:
        #print contourArea
        childLoc = contLevel[2]
        hasChild = True
        print contLevel
        #if childLoc == -1:
        #  hasChild = False

        ##follow path of children
        #while hasChild:
        #  child = hierarchy[childLoc]
        #  # 
        #  sibling = child[1]

        #  if not sibling == -1:
        #    pass
        #    #cards.append((contour,hierarchy[child[)
        #  else:
        #    hasChild = False  
        #  # may need to compare agains known card contour
        
        cards.append(contour)
        pass
      elif contourArea > minAreaThres and contourArea < maxAreaThres:
        cards.append(contour)
        pass
      else:
        pass
      #util.show(img2)
      index+=1
    img2 = imgOG.copy()
    cv2.drawContours(img2,cards,-1,(255,255,0),3)
    util.show(img2)

  def getContourAreas(self, contours):
    out = []
    for contour in contours:
      out.append(cv2.contourArea(contour))
    return out

  def modEdges(self, edges):
    kernel = np.ones((1,1),np.uint8)
    #e0 = edges.copy()
    #e0 = cv2.erode(e0,kernel, iterations = 1)
    #e1 = cv2.dilate(e0,kernel, iterations =2)
    e2 = edges.copy()
    e2 = cv2.dilate(e2,kernel, iterations = 1)
    e3 = cv2.erode(e2,kernel, iterations =1)
    return e3

  def updateBoardModel(self,img):
    #util.show(img[50:1080,575:1250])
    for roi in self.rois:
      #img2 = img.copy()
      #cv2.rectangle(img2,(roi[2],roi[0]),(roi[3],roi[1]),(255,0,255),2)
      lineFill = img[roi[0]:roi[1],roi[2]:roi[3]]
      imgG  = cv2.cvtColor(lineFill, cv2.COLOR_BGR2GRAY)
      t, imgG  = cv2.threshold(imgG,175,255,cv2.THRESH_BINARY)
      util.show(imgG)
      imgMod = self.modEdges(imgG)
      util.show(imgMod)
      #util.matShow([imgMod, lineFill])
      self.getCardContours(imgMod,lineFill)
