import bypass_api
import setting
import os
import time
from multiprocessing import Pool, Queue

def main_worker(queue):
    print(os.getpid()," working")
    while True:
        item = queue.get(True)
        print(os.getpid(), "got", item)
        time.sleep(1) # simulate a "long" operation

def main():
    queue = Queue()
    pool = Pool(4, main_worker, (queue,))
    for i in range(5):
        queue.put("hello")

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()