from ctypes import *

msvcrt = cdll.msvcrt
msg_string = "Pyfun"
msvcrt.printf("Testing: %s\n", msg_string)