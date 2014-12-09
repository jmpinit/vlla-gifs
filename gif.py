from ctypes import *

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

vlla_update = libvlla.vlla_update
vlla_update.argtypes = [ POINTER(VLLA) ]

vlla = libvlla.vlla_init("/dev/ttyACM0", "/dev/ttyACM1")
vlla.contents.pixels.contents[240] = c_uint(0xFFFFFF00)

libvlla.vlla_update(vlla)
