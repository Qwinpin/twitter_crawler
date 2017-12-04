import bypass_api as ba
from setting import set_parameters, set_save_parameters
import os
import time
from multiprocessing import Pool, Queue

def main_worker(queue):
    pid = os.getpid()
    print(pid,"working")
    while True:
        #TODO не забыть поставить timeout или отправлять в очередь пустую таску
        task = queue.get(True)
        query = task[0]
        saving_params = task[1]
        data, err, cook = ba.parse(query)
        if err != 0:
            task['cookies'] = cook
            queue.put((task, saving_params))

        #TODO сохранение в бд на сервере
        ba.to_csv(data, 'file_' + str(pid)+ '_', saving_params)
        print(os.getpid(), "crawled", len(data), "tweets")

def main():
    queue = Queue()
    pool = Pool(4, main_worker, (queue,))
    save_param = set_save_parameters()
    for i in range(10,18):
        task = set_parameters(maxTweets = 300,
                              since=('2017-01-' + str(i)),
                              until=('2017-01-' + str(i+1)),
                              screen_name='xbox')
        queue.put((task, save_param))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()