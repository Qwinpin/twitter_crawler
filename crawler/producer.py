from multiprocessing import Process, Queue
from consumer import Worker
from database import CsvDB, SQLite3


def work(db_file, queue):
    Worker(db=SQLite3(filename=db_file), queue=queue).run()


class Manager:
    def __init__(self, db_file, proc_n=1):
        self.queue = Queue()
        self.db_file = db_file
        self.NUMBER_OF_PROCESSES = proc_n

    def run(self):
        print("starting %d workers" % self.NUMBER_OF_PROCESSES)
        self.workers = []
        for _ in range(self.NUMBER_OF_PROCESSES):
            w = Process(target=work, args=(self.db_file, self.queue,))
            w.start()
            self.workers.append(w)

    def stop(self):
        self.queue.put(None)
        for i in range(self.NUMBER_OF_PROCESSES):
            self.workers[i].join()
        self.queue.close()

    def send_tasks(self, tasks):
        for task in tasks:
            self.queue.put(task)
