import asyncio
from pySMFRealTime import *



async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        print("==worker",name,"before get")
        data  = await queue.get()

        # Sleep for the "sleep_for" seconds.
        #
        print(name,"length of data",len(dataa))

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

async def put(f,queue, max_records=None):
    i = 0
    print("==21_)",f.name)
    print("==22",f.debug)
    while True:
        print("===before get")
        x, rc = f.get(wait=True,debug=2)  # Blocking get
        print("===after get",len(x),rc)
        if x == "" :  # Happens after disc()
            print("Get returned Null string, exiting loop")
            break
        if rc != "OK":
            print("get returned",rc)
            print("Disconnect",f.disc())
        i += 1
        print(i, len(x))  # Process the data
        queue.put_nowait(x)
        if max_records and i >= max_records:
            print("Reached max records, stopping")
            print("Disconnect",f.disc())
            break

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    # Create a queue that we will use to store our "workload".

    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    '''
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)
    '''
    stream_name="IFASMF.INMEM"
    f = pySMFRT(stream_name, debug=2)
    f.conn(stream_name,debug=2)  # Explicit connect

    # Create three worker tasks to process the queue concurrently.
    putter = asyncio.create_task(put(f,queue, max_records=4))

    '''
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)
    '''
    try:
        # Main thread: wait for user input to stop
        input("Press Enter to stop...\n")
        print("Stopping...")
    except KeyboardInterrupt:
        print("Interrupted, stopping...")
    finally:
        f.disc()  # This unblocks the get() call
        await queue.join()

    #for task in tasks:
    #    task.cancel()
    # Wait until all worker tasks are cancelled.
    await putter
    #await asyncio.gather(*tasks, return_exceptions=True)


asyncio.run(main())
