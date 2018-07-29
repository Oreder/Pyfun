from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False
    
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
        # the debuggee.
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
            
            # Obtain a valid handle to the newly created process
            # and store it for future access
            self.h_process = self.open_process(process_info.dwProcessID)
        else:
            print "[*] Error: 0x%08x." % kernel32.GetLastError()
            
    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process
    
    def attach(self, pid):
        self.h_process = self.open_process(pid)
        
        # We attempt to attach to the process
        # if this fails we exit the call
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            self.run()
        else:
            print "[*] Unable to attach to the process."
            
    def run(self):
        # Now we have to poll the debuggee for
        # debugging events
        while self.debugger_active == True:
            self.get_debug_event()
        
    def get_debug_event(self):
        debug_event     = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            # We aren't going to build any event handlers
            # just yet. Let's just resume the process for now.
            raw_input("Press a key to continue...")
            self.debugger_active = False
            kernel32.ContinueDebugEvent(debug_event.dwProcessID,\
                                        debug_event.dwThreadID,\
                                        continue_status)
            
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print "[*] Finished debugging. Exiting..."
            return True
        else:
            print "Error."
            return False