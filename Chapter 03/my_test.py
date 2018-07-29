import my_debugger as db

debugger = db.debugger()

pid = int(raw_input("Enter the PID of the process to attach to: "))

debugger.attach(pid)

debugger.detach()