import cv2


class Camera(object):

  def __init__(self, camera=0, width=1920, height = 1080, **kwargs):
    print "initializing camera to {}x{}".format(width,height)
    self.cam = camera
    self.width = width
    self.height = height
    self.camera = cv2.VideoCapture(self.cam)
    self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
    self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
  
  def getImage(self):
    if not self.camera.isOpened():
      print "camera is not open, trying to open it"
      self.camera.open(self.cam)
      self.__setResoultion()
      #throw some exception
    ret, img = self.camera.read()
    self.camera.release()
    return img

  def setResolution(self, width, height):
    self.width = width
    self.height = height
    
  def getResolution(self):
    return (self.width,self.height)

  def __setResoultion(self):
    self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
    self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
