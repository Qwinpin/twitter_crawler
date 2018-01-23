import pika
import json
import os
import argparse
from multiprocessing import Process
import logging

import bypass_api as ba
from database import CsvDB, SQLite3


class Worker:
    def __init__(self, db, host, port=5672, login='work', password='1234'):
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.db = db

    def crawl_tweets(self, task):
        allData = []
        while True:
            data, err, cook = ba.parse(task['query_param'], task['save_param'])
            allData += data
            if err == 0:
                break
            task['query_param']['cookies'] = cook

        self.db.save_tweets(allData, task['query_param'])
        print(os.getpid(), "crawled", len(allData), "tweets")

    def crawl_profile(self, task):
        allData = []
        data, err, cook = ba.parse_man(task['query_param'])
        self.db.save_profile(allData, task['query_param'])
        print(os.getpid(), "crawled", len(allData), "profiles")

    def callback(self, ch, method, properties, body):
        task = json.loads(body.decode('utf-8'))
        print(" [x] Received ", task)
        try:
            if task[type] == "tweets":
                self.crawl_tweets(task)
            elif task[type] == "profile":
                self.crawl_profile(task)
        except:
            pass
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)


    def run(self, clear_queue):
        logger = logging.getLogger("crawler_log.connections")
        fh = logging.FileHandler("log.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        credentials = pika.PlainCredentials(self.login, self.password)
        parameters = pika.ConnectionParameters(self.host,
                                               self.port,
                                               '/',
                                               credentials)
        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.ConnectionClosed:
            logger.error('Connection (pika) failed')
            raise
        channel = connection.channel()

        # раскоментируй этот делит если в очереди образауются задачи которые 
        # не нужно выполнять. это удалит очередь а потом она создастя снова
        if clear_queue:
            channel.queue_delete(queue='task_queue')
        
        channel.queue_declare(queue='task_queue', durable=True)
        print(os.getpid(), 'is waiting for messages. ')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback,
                              queue='task_queue')

        channel.start_consuming()


def run_worker(host, file, clear_queue):
    Worker(host=host, db=SQLite3(filename=file)).run(clear_queue)


if __name__ == '__main__':
    logger = logging.getLogger("crawler_log")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("log.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error("Start crawler")
    
    parser = argparse.ArgumentParser(description='Crawler')
    parser.add_argument('-cq', '--clear_queue', help='Clear queue', default=False, dest="cq", type=bool)
    parser.add_argument('-w', '--workers', help='Set number of workers', default=4, type=int, dest="workers_num")
    args_c = parser.parse_args()
    N = args_c.workers_num
    workers = []
    for i in range(N):
        #w = Process(target=run_worker, args=('localhost', 'file_' + str(i) + '.csv'))
        if args_c.cq:
            w = Process(target=run_worker, args=('localhost', 'twitter', True))
            args_c.cq = False
        else:
            w = Process(target=run_worker, args=('localhost', 'twitter', False))
        w.start()
        workers.append(w)

    for w in workers:
        w.join()
