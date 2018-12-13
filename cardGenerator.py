import csv
#colors = ['Green', 'Red', 'Purple']
colors = [1,2,3]
#shapes = ['Diamond', 'Oval', 'Squiggle']
shapes = [1,2,3]
#fills = ['Full', 'Lines', 'None']
#fills = [1,2,3]
counts = [1,2,3]

possibleCards = []

#for color in colors:
#  for shape in shapes:
#    for fill in fills:
#      for count in counts:
#        possibleCards.append([color,shape,fill,count])

for color in colors:
  for shape in shapes:
    for count in counts:
      possibleCards.append([shape,count,color])


print len(possibleCards)
#print possibleCards

sets = []
f =open('sets.txt',"w")

def evalSet(fc, sc, tc):
  for x in xrange(len(fc)):
    if not((fc[x] == sc[x] and fc[x] == tc[x]) or
         (fc[x] != sc[x] and fc[x] != tc[x] and sc[x] != tc[x])):
      return False

  for v in fc:
    f.write(str(v))
  f.write(',')
  for v in sc:
    f.write(str(v))
  f.write(",")
  for v in tc:
    f.write(str(v))
  f.write("\n")
  sets.append([fc,sc,tc])
  return True


for i in xrange(len(possibleCards)):
  firstCard = possibleCards[i]
  for j in xrange(len(possibleCards)):
    secondCard = possibleCards[j]
    for k in xrange(len(possibleCards)):
      thirdCard = possibleCards[k]
      isSet = evalSet(firstCard,secondCard, thirdCard)
  


#while i <= len(possibleCards)-3:
#  firstCard = possibleCards[i]
#  k = 0 
#  while k <= len(possibleCards)-2:
#    secondCard = possibleCards[k]
#    j = 0
#    while j <= len(possibleCards)-3: 
#      thirdCard = possibleCards[j]
#      isSet = evalSet(firstCard,secondCard, thirdCard)
#      tot +=1
#      #if pauseprint   and not fin:
#      #  x = raw_input()
#      #  if  x == 'a':
#      #    pause = False
#      #  elif x =='s':
#      #    fin = True
#      #  elif x == 'd':
#      #    topPause = False
#      #    fin = True
#      j+=1
#    k+=1
#  i+=1
#
