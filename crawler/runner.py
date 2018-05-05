import logging
import argparse
from multiprocessing import Process, cpu_count
import sys
import json
from consumer import Worker
from producer import Manager
from task_creator import create_tasks


if __name__ == '__main__':
    try:
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
            dest="workers_num",
            type=int)

        parser.add_argument(
            '-q',
            '--query',
            help='Search query json file',
            default='config/query.json',
            dest="query_file",
            type=str)

        parser.add_argument(
            '-s',
            '--save_set',
            help='Save settings json file',
            default='config/save_settings.json',
            dest="save_set_file",
            type=str)

        args_c = parser.parse_args()

        query = json.load(open(args_c.query_file))
        saveSet = json.load(open(args_c.save_set_file))
        tasks = create_tasks(query, saveSet)

        p = Manager(args_c.workers_num)
        p.run()
        p.send_tasks(tasks)
        p.stop()

    except Exception:
        print(sys.exc_info())
