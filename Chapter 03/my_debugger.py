from ctypes import *
from my_debugger_defines import *
from _subprocess import CREATE_NEW_CONSOLE

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        pass
    
    def load(self, path_to_exe):
        # dwCreation flag determines how to create the process
        # set creation_flags = CREATE_NEW_CONSOLE if you want
        # to see the calculator GUI
        # creation_flags = CREATE_NEW_CONSOLE
        creation_flags = DEBUG_PROCESS
        
        # instantiate the structs
        startup_info = STARTUPINFO()
        process_info = PROCESS_INFO()
        
        # The following two options allow the started process
        # to be shown as a separate window. This also illustrates
        # how different settings in the STARTUPINFO struct can affect
        # the debugger.
        startup_info.dwFlags = 0x1
        startup_info.wShowWindow = 0x0
        
        # We then initialize the cb variable in the STARTUPINFO struct
        # which is just the size of the struct itself
        startup_info.cb = sizeof(startup_info)
        
        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startup_info),
                                   byref(process_info)):
            print "[*] We have successfully launched the process!"
            print "PID: %d" % process_info.dwProcessID
            
        else:
            print "[*] Error: 0x%08x." % kernel32.GetLastError()