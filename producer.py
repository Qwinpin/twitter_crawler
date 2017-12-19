import pika
import json

from setting import set_parameters, set_save_parameters


class Producer:
    def __init__(self, host, port=5672, login='guest', password='guest'):
        self.login = login
        self.password = password
        self.host = host
        self.port = port

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)

    def stop(self):
        self.connection.close()

    def send_tasks(self, tasks):
        for task in tasks:
            self.channel \
                .basic_publish(exchange='',
                               routing_key='task_queue',
                               body=task)
            print(" [x] Sent %r" % (task,))


if __name__ == '__main__':
    p = Producer('localhost')
    p.run()
    tasks = []
    for i in range(10, 30):
        message = {
            'query_param': set_parameters(maxTweets=300,
                                          since=('2017-01-' + str(i)),
                                          until=('2017-01-' + str(i + 1)),
                                          screen_name='xbox'),

            'save_param': set_save_parameters()
        }
        tasks.append(json.dumps(message))
    p.send_tasks(tasks)
    p.stop()
