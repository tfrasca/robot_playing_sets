import cv2
from matplotlib import pyplot as plt

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

def show(img, title="image"):
  cv2.imshow(title, img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def getColors(img):
  print 33
  #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  #cv2.namedWindow('image')
  #redHSV = []     #136,40,154       193,201,212
  #greenHSV = []   #58,58,148        94,189,177
  #purpleHSV = []  #113,51,131       153,193,200

  # create trackbars for color change
  cv2.createTrackbar('minH','image',0,255,nothing)
  cv2.createTrackbar('maxH','image',255,255,nothing)
  cv2.createTrackbar('minS','image',0,255,nothing)
  cv2.createTrackbar('maxS','image',255,255,nothing)
  cv2.createTrackbar('minV','image',0,255,nothing)
  cv2.createTrackbar('maxV','image',255,255,nothing)
  print """move the trackbars to change thresholds\nonce sufficient threshold found, with image in focus,
         hit 'r' to set the red threshold
         hit 'g' to set the green theshold
         hit 'p' to set the purple theshold
         hit 'esc' to finish and return thesholds """
  while True:
    minH = cv2.getTrackbarPos('minH','image')
    maxH = cv2.getTrackbarPos('maxH','image')
    minS = cv2.getTrackbarPos('minS','image')
    maxS = cv2.getTrackbarPos('maxS','image')
    minV = cv2.getTrackbarPos('minV','image')
    maxV = cv2.getTrackbarPos('maxV','image')

    minHSV = np.array([minH,minS,minV])
    maxHSV = np.array([maxH,maxS,maxV])

    colorImg = cv2.inRange(hsv, minHSV, maxHSV)
    cv2.imshow('image',colorImg)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
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
