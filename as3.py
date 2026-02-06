from pySMFRealTime import *
from queue import Queue
from threading import Thread


#for i in range(num_threads):
#  worker = Thread(target=do_stuff, args=(q,))
#  worker.setDaemon(True)
#  worker.start()


def worker(name, qname):
    while True:
        # Get a "work item" out of the queue.
        print("==worker",name,"before queueget")
        data  = qname.get()
        if data is None:
            print("Worker",name,"data is None")
            break

        # Sleep for the "sleep_for" seconds.
        #
        print(name,"length of data",len(data))

        # Notify the queue that the "work item" has been processed.
        qname.task_done()
    print("==========End of worker=========")    

def smfget(f,qname, max_records=2,xx="NONSPECIFIED",countofwaiters=None):
    if countofwaiters is None:
        raise ValueError('countofwaiters must be specified -  the number of waiting tasks.')
    i = 0

    while True:
        print("===before smf get")
        x, rc = f.get(wait=True,debug=2)  # Blocking get
        print("===after smf get",len(x),rc)
        if x == "" :  # Happens after disc()
            print("Get returned Null string, exiting loop")
            break

        if rc != "OK":
            print("get returned",rc)
            print("Disconnect",f.disc())
            break
        i += 1
        print(i, len(x))  # Process the data
        qname.put(x)
        if max_records and i >= max_records:
            print("Reached max records, stopping")
            print("Disconnect",f.disc())
            break
    #print(dir(qname))    
    #  qname.shutdown()   python 3.13
    for i in range(countofwaiters):
        qname.put(None)
    return      




def runit():
    # Create a queue that we will use to store our "workload".

    qname = Queue(maxsize=10)

    stream_name="IFASMF.INMEM"
    f = pySMFRT(stream_name, debug=2)
    f.conn(stream_name,debug=2)  # Explicit connect
    
    smfGetter = Thread(target=smfget, args=(f, qname,), kwargs={"max_records": 2, "countofwaiters":3})
    smfGetter.start()
    worker1 = Thread(target=worker, args=("worker1",qname))
    worker1.start()
    worker2 = Thread(target=worker, args=("worker2",qname))
    worker2.start()
    worker3 = Thread(target=worker, args=("worker3",qname))
    worker3.start()

    try:
        # Main thread: wait for user input to stop
        qname.join()
    except KeyboardInterrupt:
        print("Interrupted, stopping...")
        f.disc()  # This unblocks the get() call
        qname.join()
    finally:
        f.disc()  # This unblocks the get() call
        qname.join()

    #for task in tasks:
    #    task.cancel()
    # Wait until all worker tasks are cancelled.
    #qname.join()


runit()