import pika
import sys
import json
from setting import set_parameters, set_save_parameters
import numpy as np

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

for i in range(10, 30):
    message = {
        'query_param': set_parameters(maxTweets=300,
                             since=('2017-01-' + str(i)),
                             until=('2017-01-' + str(i + 1)),
                             screen_name='xbox'),

        'save_param': set_save_parameters()
    }

    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print(" [x] Sent %r" % (message,))

connection.close()
