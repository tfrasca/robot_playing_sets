import time, vision, util, robot
from camera import Camera
# height loc (row) / width loc (column)
#ROI = [(0,216,575,912,1250)(0,216,575,912,1250)(0,216,575,912,1250)]
      #[0:1080,575:1250]

class SetGame(object):

  def __init__(self):
    self.colorThresholds = [ \
                            [[136,40,154],[193,201,212]], \
                            [[58,58,148],[94,189,177]], \
                            [[113,51,131],[153,193,200]]]
    self.rois = util.createCardROIs(5,2,50,1080,575,1250)
    self.stillPlaying = True
    self.cam = Camera()
    util.show(self.cam.getImage())
    #print self.rois
    print "Ready to play!! :)"

  def play(self):
    cards = []
    stillPlaying = True
    while stillPlaying:
      print "woot still playing"
      img = self.cam.getImage()
      newCards = self.updateBoardModel(img)
      # if the cards are the same as previous capture,
      # then no need to find sets
      if not newCards == cards:
        cards = newCards
        sets = robot.findSets(cards)
        #if len(sets) > 0:
        #  robot.pickUpSet(sets[0])
      time.sleep(1)
      ret = raw_input("keep playing y/[n]: ")
      if ret == 'n' or ret == '':
        stillPlaying = False

  def test(self):
    loadImage = raw_input("Load image y/[n]: ")
    if loadImage == 'n' or loadImage =='':
      imgOG = self.cam.getImage()
      #cv2.imwrite("set_test.png",imgOG)
    else:
      imgOG = cv2.imread("set_test.png")
    print self.cam.getResolution()
    util.show(imgOG)
    self.updateBoardModel(imgOG)

  def updateBoardModel(self,img):
    #util.show(img[50:1080,575:1250])
    print "updating card classification"
    cards = []
    for roi in self.rois:
      cards.append(vision.classifyCard(img[roi[0]:roi[1],roi[2]:roi[3]]))
    return cards

  def setColorThresholds(self):
    img = self.cam.getImage()
    self.colorThresholds= util.initializeColorThresholds(img)
    
if __name__ == "__main__":
  game = SetGame()
  game.test()
  #game.setColorThresholds()
  #game.play()
