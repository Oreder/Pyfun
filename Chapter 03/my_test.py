import my_debugger as db

debugger = db.debugger()

pid = int(raw_input("Enter the PID of the process to attach to: "))

debugger.attach(pid)

debugger.detach()

thread_list = debugger.enumerate_threads()
# For each thread in this list we want to grab the value of the registers
for thread in thread_list:
    thread_context = debugger.get_thread_context(thread)
    
    # Now let's output the contents of some registers
    print "[*] Dumping registers for thread ID: 0x%08x" % thread
    print "[+] EIP: 0x%08x" % thread_context.Eip
    print "[+] ESP: 0x%08x" % thread_context.Esp
    print "[+] EBP: 0x%08x" % thread_context.Ebp
    print "[+] EAX: 0x%08x" % thread_context.Eax
    print "[+] EBX: 0x%08x" % thread_context.Ebx
    print "[+] ECX: 0x%08x" % thread_context.Ecx
    print "[+] EDX: 0x%08x" % thread_context.Edx
    print "[*] End DUMP."