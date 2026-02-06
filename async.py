import sys
import locale
import os
import threading
import time
from pySMFRealTime import *

# Blocking SMF data retrieval with graceful shutdown
# Use one thread for blocking gets, main thread for handling stop (e.g., input or interrupt).
# Calling disc() from main will unblock the get() and allow clean exit.

def blocking_get_loop(f, timeout=10, event=None,max_records=None,):
    i = 0
    while True:
        #t = Timer(timeout, timerpop(f))
        x, rc = f.get(wait=True)  # Blocking get
        #t.cancel()
        if x == "" :  # Happens after disc()
            print("Get returned Null string, exiting loop")
            break
        if rc != "OK":
            print("get returned",rc)
            print("Disconnect",f.disc())
        i += 1
        print(i, len(x))  # Process the data
        if max_records and i >= max_records:
            print("Reached max records, stopping")
            print("Disconnect",f.disc())
            break
    if event is not None:
        event.set() # wake up the main task    
        
        

def timerpop(f):
    f.disc()

#t = Timer(30.0, hello)
#t.start()  # after 30 seconds, "hello, world" will be printed        

def blocking_smf(stream_name="IFASMF.INMEM", debug=0, max_records=None):
    f = pySMFRT(stream_name, debug=debug)
    f.conn(stream_name,debug=2)  # Explicit connect
    myevent = threading.Event()
    print("myevent",myevent.__class__.__name__)
    # Start the blocking loop in a separate thread
    get_thread = threading.Thread(target=blocking_get_loop, args=(f,),
                                  kwargs={"max_records": max_records,"timeout":20,"event":myevent})
    get_thread.start()
    if myevent.wait(timeout=30) is False:
        print("We timed out")
        f.disc()  # make the loop end
        get_thread.join
    
    '''
    try:
        # Main thread: wait for user input to stop
        input("Press Enter to stop...\n")
        print("Stopping...")
    except KeyboardInterrupt:
        print("Interrupted, stopping...")
    finally:
        f.disc()  # This unblocks the get() call
        get_thread.join()  # Wait for thread to exit
    '''
# Usage example: run until Enter or interrupt, or max_records
if __name__ == "__main__":
    blocking_smf(max_records=6)