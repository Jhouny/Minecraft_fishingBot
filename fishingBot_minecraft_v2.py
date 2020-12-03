import pyscreenshot as ImGrab
from PIL import Image
import itertools
from time import time, sleep
from numba import jit, cuda
from math import sqrt


#@jit(target ="cuda")
def Score_inSum(c, target_index):
    color = list(c)
    s0 = color[target_index]*len(color)
    color.pop(target_index)

    sumRest = 0
    for ind in range(len(color)):
        sumRest += color[ind]

    return (s0-sumRest)

def Score_inPercentage(c, target_index):
    color = list(c)
    sum = 0
    for val in color:
        sum += val

    s0 = color[target_index]
    if sum >= 10:
        perc = (s0/sum)*1080
    else:
        perc = 0

    return perc

def Score_inPercentageNLuminosity(c, target_index):
    color = list(c)
    sum = 0
    for val in color:
        sum += val

    s0 = color[target_index]
    if sum >= 10:
        perc = (s0/sum)*100
    else:
        perc = 0

    luminosityPerc = (s0/255)*100
    return (perc*90+luminosityPerc*10)/100


def Screenshot(resizePercentage, box):
    im = ImGrab.grab(bbox=box)
    im = im.resize((int((box[2]-box[0])*resizePercentage),
                     int((box[3]-box[1])*resizePercentage)))

    return im


def findTarget(img, target_index):
    max = (0,0,0)
    pos = [0,0]
    pix = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            score_pixel = Score_inPercentageNLuminosity(pix[x,y], target_index)
            if score_pixel > Score_inPercentageNLuminosity(max, target_index):
                max = pix[x, y]
                pos = [x, y]

    return max, pos

def measureChange(im1, im2, target_index, resizePercentage, threshold):
    c1, target1 = findTarget(im1, target_index)
    c2, target2 = findTarget(im2, target_index)
    d = sqrt((target2[0]-target1[0])**2+(target2[1]-target1[1])**2)
    standardizedPixelDistance = d*(1/resizePercentage)
    if standardizedPixelDistance >= threshold:
        return True, standardizedPixelDistance
    else:
        return False, standardizedPixelDistance


sleep(2)

#Choose color to be found with maximum value in image
target = "Red"
opt = ["Red", "Green", "Blue"]
ind = opt.index(target)
threshold = 100
state = 1
resizePercentage = 0.2
last = Screenshot(resizePercentage, (0,0, 1920, 1080))
image = Screenshot(resizePercentage, (0,0, 1920, 1080))
t1 = time()
t2 = time()
while state:
    print("Delay: ", (t2-t1))
    t1 = time()
    last = image
    image = Screenshot(resizePercentage, (0,0, 1920, 1080))
    activation, d = measureChange(last, image, ind, resizePercentage, threshold)
    if activation == True:
        print("Distance bigger than threshold = ", d)
        state = 0
    else:
        print("Distance is below threshold")
    t2 = time()

last.save("/home/jhony_ma/Downloads/test.png")
image.save("/home/jhony_ma/Downloads/test2.png")


"""
#Choose color to be found with maximum value in image
target = "Red"
opt = ["Red", "Green", "Blue"]
ind = opt.index(target)
source = "/home/jhony_ma/Downloads/2020-11-30_12.11.13.png"
img = Image.open(source)
pix = img.load()
#print(pix[643, 456])
#print(Score(pix[643, 456], ind))
c, p = findTarget(img, ind)
print("Found color ", c, " at Position ", p, "\nwith a Score of ", Score_inPercentageNLuminosity(c, ind))
"""
