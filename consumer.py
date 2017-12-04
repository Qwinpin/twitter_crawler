import pika
import json
import os
import time
from multiprocessing import Pool, Queue

import bypass_api as ba

def main_worker(queue):
    pid = os.getpid()
    print(pid, "working")
    while True:
        # TODO не забыть поставить timeout или отправлять в очередь пустую таску
        task = queue.get(True)
        data, err, cook = ba.parse(task['query_param'])
        if err != 0:
            task['query_param']['cookies'] = cook
            queue.put(task)

        # TODO сохранение в бд на сервере
        ba.to_csv(data, 'file_' + str(pid) + '_', task['save_param'])
        print(os.getpid(), "crawled", len(data), "tweets")


def callback(ch, method, properties, body):
    task = json.loads(body)
    print(" [x] Received ", task)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    queue.put(task)


if __name__ == '__main__':
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                           5672,
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    queue = Queue()
    pool = Pool(4, main_worker, (queue,))
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue='task_queue')

    channel.start_consuming()

    pool.close()
    pool.join()
