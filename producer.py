import pika
import sys
import json

from task_creator import create_tasks


class Producer:
    def __init__(self, host, port=5672, login='serv', password='1234'):
        self.login = login
        self.password = password
        self.host = host
        self.port = port

    def run(self):
        credentials = pika.PlainCredentials(self.login, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host, credentials=credentials))
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


def read_query(filename):
    return json.load(open(filename))


def parse_argv(argv):
    if len(argv) != 2:
        raise Exception('Two input settings files are required')

    return read_query(argv[0]), read_query(argv[1])


if __name__ == '__main__':
    p = Producer('localhost')
    p.run()
    try:
        # query = parse_argv(sys.argv[1:])
        query, saveSet = parse_argv(['query.json', 'save_settings.json'])
        tasks = create_tasks(query, saveSet)
        p.send_tasks(tasks)
        p.stop()

    except Exception:
        print(sys.exc_info())
