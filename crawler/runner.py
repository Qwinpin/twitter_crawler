import logging
import argparse
from multiprocessing import Process, cpu_count
import sys
import json
from consumer import Worker
from producer import Manager
from task_creator import create_tasks


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
        help='Number of workers. Default: 4',
        default=4,
        dest="workers_num",
        type=int)

    parser.add_argument(
        '-q',
        '--query',
        help='Search query json file. Default: ../config/query.json',
        default='../config/query.json',
        dest="query_file",
        type=str)

    parser.add_argument(
        '-s',
        '--save_set',
        help='Save settings json file.\nDefault: ../config/save_settings.json',
        default='../config/save_settings.json',
        dest="save_set_file",
        type=str)

    parser.add_argument(
        '-d',
        '--database',
        help='SQLite database file path. Default: ./twitter.db',
        default='./twitter.db',
        dest="db",
        type=str)

    args_c = parser.parse_args()

    query = json.load(open(args_c.query_file))
    saveSet = json.load(open(args_c.save_set_file))
    tasks = create_tasks(query, saveSet)

    p = Manager(db_file=args_c.db, proc_n=args_c.workers_num)
    p.send_tasks(tasks)
    p.run()
    p.stop()
