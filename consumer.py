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
        data, err, cook = ba.parse_profile(task['query_param'])
        self.db.save_profile(data, task['query_param'])
        print(os.getpid(), "crawled", len(data), "profiles")

    def callback(self, ch, method, properties, body):
        task = json.loads(body.decode('utf-8'))
        print(" [x] Received ", task)
        try:
            if task['type'] == "tweets":
                self.crawl_tweets(task)
            elif task['type'] == "profile":
                self.crawl_profile(task)
        except:
            pass
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)


    def run(self):
        logger = logging.getLogger("crawler_log.connections")
        fh = logging.FileHandler("log.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        credentials = pika.PlainCredentials(self.login, self.password)
        parameters = pika.ConnectionParameters(host=self.host,
                                               port=self.port,
                                               virtual_host='/',
                                               credentials=credentials,
                                               heartbeat=60*60)
        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.ConnectionClosed:
            logger.error('Connection (pika) failed')
            raise

        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        print(os.getpid(), 'is waiting for messages. ')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback,
                              queue='task_queue')

        channel.start_consuming()


def run_worker(host, file):
    Worker(host=host, db=SQLite3(filename=file)).run()


if __name__ == '__main__':
    logger = logging.getLogger("crawler_log")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("log.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("Start crawler")
    
    parser = argparse.ArgumentParser(description='Crawler')
    parser.add_argument('-w', '--workers', help='Set number of workers', default=4, type=int, dest="workers_num")
    args_c = parser.parse_args()

    workers = []
    for i in range(args_c.workers_num):
        w = Process(target=run_worker, args=('localhost', 'twitter'))
        w.start()
        workers.append(w)

    for w in workers:
        w.join()
