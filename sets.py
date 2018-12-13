import time, vision, util
from camera import Camera
import random
import cv2
import serial
# height loc (row) / width loc (column)
#ROI = [(0,216,575,912,1250)(0,216,575,912,1250)(0,216,575,912,1250)]
      #[0:1080,575:1250]

class SetGame(object):

  def __init__(self):
    self.xmin = 360
    self.xmax = 1430
    self.ymin = 40
    self.ymax = 965
    self.colorThresholds = [ \
                            [[136,40,154],[193,201,212]], \
                            [[58,58,148],[94,189,177]], \
                            [[113,51,131],[153,193,200]]]
    self.grayThresholds = [155,255]
    # break up the image into regions for each card
    self.rois = util.createCardROIs(3,5,self.ymin,self.ymax,self.xmin,self.xmax)
    self.stillPlaying = True
    self.cam = Camera(1)
    self.classifier = vision.CardClassifier()
    # get all the possible sets
    util.readAllSets()
    self.rng = random.Random(15)
    print "Ready to play!! :)"
    # connect to the robot
    self.robotController = serial.Serial("/dev/ttyUSB0",115200)
    #self.robotController = serial.Serial("/dev/tty",115200)

  def play(self):
    cards = []
    stillPlaying = True
    while stillPlaying:
      shouldUpdate = raw_input("should update the image? [y]/n")
      if shouldUpdate == "y" or shouldUpdate == "":
        img = self.cam.getImage()
        # update the image of the cards in play
        newCards = self.updateBoardModel(img)
      # with these cards, find any sets
      sets = util.findSets(newCards)
      if len(sets) > 1:
        val = self.rng.randint(0,len(sets)-1)
        # pick up the set of cards
        self.pickUp(sets[val])
      elif len(sets) == 1:
        self.pickUp(sets[0])
      time.sleep(1)
      #ret = raw_input("keep playing [y]/n: ")
      #if ret == 'n':
      #  stillPlaying = False

  def pickUp(self, cards):
    finishingPickUp = True
    while finishingPickUp:
      val = self.rng.random()
      if val > .8:
        if len(cards) > 1:
          finishingPickUp = False
          outString = ""
          outString += str(cards[0])
          outString += ","
          outString += str(cards[1])
          outString += ","
          outString += str(cards[2])
          print outString
          self.robotController.reset_output_buffer()
          time.sleep(.2)
          self.robotController.write(outString)
          time.sleep(1)
          print "waiting for robot to respond"
          #self.robotController.reset_input_buffer()
          #time.sleep(1)
          #self.robotController.reset_input_buffer()
          #time.sleep(1)
          while True:
            # wait for the robot to respond
            # doesn't fully work when the human tries to pick up a set
            x = self.robotController.readline()
            try:
              y = x.strip()
              print "response ", y
              if y == "pic" or y == "pic\n" or y =="pic \n" or y == "pic ":
                print "ready to go to the next round"
                break
              elif y == "picB" or y == "picB " or y == "picB\n":
                cards = []
                print "waiting for human to finish"
                finishingPickUp = False
                break
              else:
                print "interesting"

            except AttributeError:
              pass
            time.sleep(2)
      else:
        time.sleep(2)

  def updateBoardModel(self,img):
    #print "updating card classification"
    cards = []
    for roi in self.rois:
      try:
        # find the value for each card
        cards.append(self.classifier.classifyCard(img[roi[0]:roi[1],roi[2]:roi[3]], self.colorThresholds, self.grayThresholds))
      except AttributeError:
        cards.append(-1111)
    return cards

  def setColorThresholds(self):
    img = self.cam.getImage()
    self.colorThresholds= util.initializeColorThresholds(img)
    
  def setGrayThreshold(self):
    img = self.cam.getImage()
    self.grayThresholds = util.initializeGrayThresholds(img)

  def createTrainingShapes(self):
    img  = self.cam.getImage()
    for roi in self.rois[:14]:
      try:
        self.classifier.createTrainingShapes(img[roi[0]:roi[1],roi[2]:roi[3]], self.grayThresholds)
      except AttributeError:
        pass

if __name__ == "__main__":
  game = SetGame()
  #game.test()
  #game.setColorThresholds()
  game.setGrayThreshold()
  game.createTrainingShapes()
  game.play()
