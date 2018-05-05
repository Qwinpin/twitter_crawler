
from multiprocessing import Process, Queue
from consumer import Worker
from database import CsvDB, SQLite3


def work(id, db, queue):
    Worker(db=db, queue=queue).run()


class Manager:
    def __init__(self, db_file, proc_n=1):
        self.queue = Queue()
        self.db_file = db_file
        self.NUMBER_OF_PROCESSES = proc_n

    def run(self):
        print("starting %d workers" % self.NUMBER_OF_PROCESSES)
        self.workers = [Process(target=work, args=(i, SQLite3(filename=self.db_file), self.queue,))
                        for i in range(self.NUMBER_OF_PROCESSES)]
        for w in self.workers:
            w.start()

    def stop(self):
        self.queue.put(None)
        for i in range(self.NUMBER_OF_PROCESSES):
            self.workers[i].join()
        self.queue.close()

    def send_tasks(self, tasks):
        pass
