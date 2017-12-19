import pika
import json
import os
from multiprocessing import Process

import bypass_api as ba
from database import CsvDB


class Worker:
    def __init__(self, db, host, port=5672, login='guest', password='guest'):
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.db = db

    def callback(self, ch, method, properties, body):
        task = json.loads(body)
        print(" [x] Received ", task)

        allData = []
        while True:
            data, err, cook = ba.parse(task['query_param'])
            allData += data
            if err == 0:
                break
            task['query_param']['cookies'] = cook

        # TODO сохранение в бд на сервере
        self.db.save(allData, task['save_param'])
        print(os.getpid(), "crawled", len(allData), "tweets")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        credentials = pika.PlainCredentials(self.login, self.password)
        parameters = pika.ConnectionParameters(self.host,
                                               self.port,
                                               '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)
        print(os.getpid(), 'is waiting for messages. ')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback,
                              queue='task_queue')

        channel.start_consuming()


def run_worker(host, file):
    Worker(host=host, db=CsvDB(filename=file)).run()


if __name__ == '__main__':
    N = 4
    workers = []
    for i in range(N):
        w = Process(target=run_worker, args=('localhost', 'file_' + str(i) + '.csv'))
        w.start()
        workers.append(w)

    for w in workers:
        w.join()
