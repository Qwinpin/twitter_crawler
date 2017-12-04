import pika
import sys
import json
import numpy as np

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = {
    'name': 'Ilya',
    'age' : np.random.randint(60)
}
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=json.dumps(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % (message,))
connection.close()