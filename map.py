from PIL import Image
from opennoise3 import OpenSimplex
import math as Math
import datetime
import numpy as np
import noise

shape = (2**9, 2**8)
channels = 3
scale = 3

now = datetime.datetime.now()
unix = now.timestamp()

noise3 = OpenSimplex(seed = int(unix))

#imMap = np.zeros( (shape[1], shape[0], shape[2]) )
imMap = Image.new('RGB', shape)

cHex = [
    '82B675',
    '97C480',
    'A7D580',
    'BFE47A',
    'FFFF8B',
    'F1DB6C',
    'EBC36C',
    'D7A95E',
    'C2874D',
    '9F744F',
    '85694B',
    '65513E',
    '897264',
    'A49780',
    'C2BBAA',
    'D3CEC4',
    'E1E1E1',
    'FFFFF']

cRGB = [
	[-1.00,	(195, 228, 255)],
	[ 0.00,	(195, 228, 255)],
	[ 0.10,	(130, 182, 117)],
	[ 0.20,	(151, 196, 128)],
	[ 0.25,	(167, 213, 128)],
	[ 0.30,	(191, 228, 122)],
	[ 0.35,	(255, 255, 139)],
	[ 0.40,	(241, 219, 108)],
	[ 0.45,	(235, 195, 108)],
	[ 0.50,	(215, 169,  94)],
	[ 0.55,	(194, 135,  77)],
	[ 0.60,	(159, 116,  79)],
	[ 0.65,	(113, 105,  75)],
	[ 0.70,	(101,  81,  62)],
	[ 0.75,	(137, 114, 100)],
	[ 0.80,	(164, 151, 128)],
	[ 0.85,	(194, 187, 170)],
	[ 0.90,	(211, 206, 196)],
	[ 0.95,	(225, 225, 225)],
	[ 1.00,	(255, 255, 255)]]

    
def transform(n):
    return np.real((n**2.6))

def getScale(n, scheme):

    mn = -1
    mx =  1

    if n < mn:
        n = mn
        print('Uh oh! {}'.format(n))
    elif n > mx:
        n = mx
        print('Uh oh! {}'.format(n))

    maxIdx = 0
    for i in scheme:
        if n < i[0]:
            return scheme[maxIdx][1]
        else:
            maxIdx = maxIdx+1


for y in range(0, shape[1]):
    for x in range(0, shape[0]):

        xT = (x / shape[0]) - 0.5
        yT = (y / shape[1]) - 0.5

        lat = xT * Math.pi * 2
        lon = yT * Math.pi

        pX = Math.cos(lon)*Math.cos(lat) * scale
        pY = Math.cos(lon)*Math.sin(lat) * scale
        pZ = Math.sin(lon)               * scale

        val = noise3.noise3d(pX, pY, pZ)
        #val = transform(val)

        SCALE = 0
        THRESH = 1
        
        mode = SCALE
        
        c = None
        if mode == SCALE:
            #c = 255 * transform(val)
            c = getScale(transform(val), cRGB)
            
        elif mode == THRESH:
            if val <= 0.25:
                c = int(255 * (0.3))
            elif val <= 0.4:
                c = int(255 * (1/3))
            elif val <= 0.6:
                c = int(255 * (2/3))
            elif val <= 1.00:
                c = int(255 * (3/3))

        imMap.putpixel( (x, y), c)
        #imMap[y, x] = c


#imMap = Image.fromarray(imMap, 'RGB')

imMap.save('testImage.png')
imMap.show()