import logging
import argparse
from multiprocessing import Process
import sys
import json

from producer import Producer
from consumer import Worker
from database import CsvDB, SQLite3
from task_creator import create_profile_tasks, create_task


def run_worker(host, file):
    Worker(db=SQLite3(filename=file)).run()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Crawler')
        parser.add_argument(
            '-q',
            '--query',
            help='Search query json file',
            default='query.json',
            dest="query_file",
            type=str)

        parser.add_argument(
            '-s',
            '--save_set',
            help='Save settings json file',
            default='save_settings.json',
            dest="save_set_file",
            type=str)

        parser.add_argument(
            '-cq',
            '--clear_queue',
            help='Clear queue',
            default=True,
            dest="cq",
            type=bool)
        args_c = parser.parse_args()

        query = json.load(open(args_c.query_file))
        saveSet = json.load(open(args_c.save_set_file))
        tasks = create_tasks(query, saveSet)

        p = Producer('localhost')
        p.run(args_c.cq)
        p.send_tasks(tasks)
        p.stop()

    except Exception:
        print(sys.exc_info())


if __name__ == '__main__':
    logger = logging.getLogger("crawler_log")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("log.log")
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("Start crawler")

    parser = argparse.ArgumentParser(description='Crawler')
    parser.add_argument(
        '-w',
        '--workers',
        help='Set number of workers',
        default=4,
        type=int,
        dest="workers_num")
    args_c = parser.parse_args()

    workers = []
    for i in range(args_c.workers_num):
        w = Process(target=run_worker, args=('localhost', 'twitter'))
        w.start()
        workers.append(w)

    for w in workers:
        w.join()
