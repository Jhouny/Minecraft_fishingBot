import pyscreenshot as ImGrab
import itertools
from time import time, sleep

def sumTupleTerms(tup1, tup2):
    if len(tup1) != len(tup2):
        print("Tuples have different shape, stopping process...")
        return

    out = [0]*len(tup1)
    for ind in range(len(tup1)):
        out[ind] = tup1[ind]+tup2[ind]

    return tuple(out)

def maxDifferenceTupleTerms(tup1, tup2):
    if len(tup1) != len(tup2):
        print("Tuples have different shape, stopping process...")
        return False

    max = 0
    for ind in range(len(tup1)):
        dif = abs(tup1[ind] - tup2[ind])
        if max < dif:
            max = dif

    return max

def avgDifferenceTupleTerms(tup1, tup2):
    if len(tup1) != len(tup2):
        print("Tuples have different shape, stopping process...")
        return False

    sum = 0
    n = 0
    for ind in range(len(tup1)):
        dif = abs(tup1[ind] - tup2[ind])
        sum += dif
        n +=1

    avg = sum/n
    return avg

def getKernelValues(x, y, kernel_size, img):
    var = int((kernel_size-1)/2)
    variations = list(itertools.product(range(-1*var, var+1), repeat=2))
    positions = []

    for val in variations:
        term = sumTupleTerms(val, (x, y))
        positions.append(term)

    colors = []
    for pos in positions:
        color = img.load()[pos]
        colors.append(color)

    return colors

def Screenshot(resizePercentage, box):
    im = ImGrab.grab(bbox=box)
    im = im.resize((int((box[2]-box[0])*resizePercentage),
                     int((box[3]-box[1])*resizePercentage)))

    return im


def Kernel_boxDifference(kernel_size, im1, im2):
    if im1.size != im2.size:
        print("Images' shapes are non-equivalent!\nStopping process...")
        return False

    var = int((kernel_size-1)/2)
    state = True
    max = 0
    pos = [0, 0]
    #print("1")
    for x in range(var, im1.size[0]-var, kernel_size):
        for y in range(var, im1.size[1]-var, kernel_size):
            kernel1 = getKernelValues(x, y, kernel_size, im1)
            kernel2 = getKernelValues(x, y, kernel_size, im2)
            #print("2")
            for ind in range(len(kernel1)):
                dif = avgDifferenceTupleTerms(kernel1[ind], kernel2[ind])
                #print("3")
                if max < dif:
                    max = dif
                    pos = [x, y]

    return max, pos


sleep(2)
state = 1
kernel = 3
threshold = 200
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
    difference, pos = Kernel_boxDifference(kernel, last, image)
    if difference > threshold:
        print("Difference bigger than threshold at ", pos)
        state = 0
    else:
        print("Difference is below threshold")
    t2 = time()

last.save("/home/jhony_ma/Downloads/test.png")
image.save("/home/jhony_ma/Downloads/test2.png")
