from ctypes import *
import os, sys
from PIL import Image

libvlla = CDLL("libvlla.so")

WIDTH = 60
HEIGHT = 32

class VLLA(Structure):
    _fields_=[("ser1_fd", c_int),
            ("ser2_fd", c_int),
            ("pixels", POINTER(c_uint * (WIDTH * HEIGHT)))]

vlla_init = libvlla.vlla_init
vlla_init.argtypes = [ c_char_p, c_char_p ]
vlla_init.restype = POINTER(VLLA)

vlla_create = libvlla.vlla_create
vlla_create.restype = POINTER(VLLA)

vlla_update = libvlla.vlla_update
vlla_update.argtypes = [ POINTER(VLLA) ]

def getImagePaths(gifpath):
    gifname = os.path.basename(gifpath)
    gifdir = os.path.dirname(os.path.abspath(gifpath))
    files = [ f for f in os.listdir(gifdir) if os.path.isfile(os.path.join(gifdir, f)) ]
    gifs = filter(lambda fn: gifname in fn and fn.index(gifname) == 0, files)
    gifs.sort()
    del gifs[0]
    gifs = map(lambda fn: gifdir + "/" + fn, gifs)
    return gifs

def getVLLAs(imagePaths):
    vllas = []

    root_vlla = vlla_init("/dev/ttyACM0", "/dev/ttyACM1")

    for path in imagePaths:
        im = Image.open(path)
        rgb_im = im.convert('RGB')
        width, height = im.size

        w = min(width, 60)
        h = min(height, 32)

        vlla = vlla_create()
        vlla.contents.ser1_fd = root_vlla.contents.ser1_fd
        vlla.contents.ser2_fd = root_vlla.contents.ser2_fd

        for y in range(0, h):
            for x in range(0, w):
                r, g, b = rgb_im.getpixel((x, y))
                vlla.contents.pixels.contents[y*WIDTH+x] = c_uint((r << 16)|(g << 8)|b)

        vllas.append(vlla)

    return vllas
    
if not len(sys.argv) == 2:
    print "not enough args"
    exit(1)

gifpath = sys.argv[1]
vllas = getVLLAs(getImagePaths(gifpath))

while True:
    for vlla in vllas:
        libvlla.vlla_update(vlla)
