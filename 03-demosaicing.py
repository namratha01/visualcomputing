import numpy
import cv2

# this exercise references "Interactions Between Color Plane Interpolation and Other Image Processing Functions in Electronic Photography" by Adams

numpyInput = cv2.imread(filename='./samples/demosaicing.png', flags=cv2.IMREAD_GRAYSCALE).astype(numpy.float32) / 255.0

numpyOutput = numpy.zeros([numpyInput.shape[0] - 2, numpyInput.shape[1] - 2, 3], numpy.float32)

# demosaic numpyInput by using bilinear interpolation as shown in the slides and described in section 3.3

# the input has the following beyer pattern, id est that the top left corner is red

# RGRGRG ....
# GBGBGB ....
# RGRGRG ....
# GBGBGB ....
# ...........
# ...........

# the straightforward way that i see for doing this (there are others as well though) is to iterate over each pixel and resolving each of the four possible cases
# to simplify this, you can iterate from (1 to numpyInput.shape[0] - 1) and (1 to numpyInput.shape[1] - 1) to avoid corner cases, numpyOutput is accordingly one pixel smaller on each side

# notice that to fill in the missing greens, you will always be able to take the average of four neighboring values
# however, depending on the case, you either get four or only two neighboring values for red and blue
# this is perfectly fine, in this case you can simply use the average of two values if only two neighbors are available

def findSensorType(i,j) : 
  iVal = i % 2
  jVal = j % 2
  if (iVal == 0) and (jVal == 0) :
    return 'red'
  elif (iVal == 1) and (jVal == 1) :
    return 'blue'
  elif (iVal == 1) and (jVal == 0) :
    return 'green1'
  elif (iVal == 0) and (jVal == 1) :
    return 'green2'

def pixelUpdate(i,j,sensorType) : 
  if sensorType == 'blue' : 
    bValue = numpyInput[i][j]
    gValue = ( numpyInput[i-1][j] + numpyInput[i][j-1] + numpyInput[i][j+1] + numpyInput[i+1][j] )/4.0
    rValue = ( numpyInput[i-1][j-1] + numpyInput[i-1][j+1] + numpyInput[i+1][j-1] + numpyInput[i+1][j+1] )/4.0
  elif sensorType == 'green1' :
    bValue = ( numpyInput[i][j-1] + numpyInput[i][j+1] )/2.0
    gValue = numpyInput[i][j]
    rValue = ( numpyInput[i-1][j] + numpyInput[i+1][j] )/2.0
  elif sensorType == 'green2' :
    bValue = ( numpyInput[i-1][j] + numpyInput[i+1][j] )/2.0
    gValue = numpyInput[i][j]
    rValue = ( numpyInput[i][j-1] + numpyInput[i][j+1] )/2.0
  else : 
    bValue = ( numpyInput[i-1][j-1] + numpyInput[i-1][j+1] + numpyInput[i+1][j-1] + numpyInput[i+1][j+1] )/4.0
    gValue = ( numpyInput[i-1][j] + numpyInput[i][j-1] + numpyInput[i][j+1] + numpyInput[i+1][j] )/4.0
    rValue = numpyInput[i][j]
  return [bValue,gValue,rValue]  

for i in range(1,numpyInput.shape[0] - 1) : 
  for j in range(1,numpyInput.shape[1] - 1) : 
    sensorType = findSensorType(i,j)
    numpyOutput[i-1][j-1] = pixelUpdate(i,j,sensorType)

cv2.imwrite(filename='./03-demosaicing.png', img=(numpyOutput * 255.0).clip(0.0, 255.0).astype(numpy.uint8))
