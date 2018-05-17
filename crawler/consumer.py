import json
import re
import os
import logging
import sys

import bypass_api as ba
from task_creator import create_tasks


class Worker:
    def __init__(self, db, queue):
        self.db = db
        self.queue = queue

    def crawl_tweets(self, task):
        allData = []
        for data, err, cook in ba.parse(task['query_param'],
                                        task['save_param']):
            allData += data
            task['query_param']['cookies'] = cook
        print(os.getpid(), "crawled", len(allData), "tweets")
        self.db.save_tweets(allData, task['query_param'])
        print(os.getpid(), "saved", len(allData), "tweets")
        self.recursion(allData, task)

    def crawl_profile(self, task):
        data, err, cook = ba.parse_profile(task['query_param'])
        print(data, err)
        if err == 0:
            self.db.save_profile(data, task['query_param'])
            print(os.getpid(), "saved profile")
        else:
            print('Error')

    def recursion(self, tweets, task):
        if task['recursion'] > 0:
            mentioned_names = []
            for tweet in tweets:
                namesInTweet = re.findall(r'(?<=\W)[@]\S*', tweet.text)
                mentioned_names += [n[1:].trim() for n in namesInTweet]
                mentioned_names.append(tweet.screenname)

            mentioned_names = set(mentioned_names) - self.db.get_profiles()
            mentioned_names.remove("")
            mentioned_names.remove(" ")
            mentioned_names.remove(None)

            tasks = create_tasks([
                {
                    "screen_name": list(mentioned_names),
                    "since": "2007-01-01",
                    "recursion": task['recursion'] - 1
                }
            ], task["save_param"])

            for task in tasks:
                self.queue.put(task)

    def callback(self, body):
        task = json.loads(body)
        print(os.getpid(), "Received ",
              task['type'], task['query_param']['url'])
        try:
            if task['type'] == "tweets":
                self.crawl_tweets(task)
            elif task['type'] == "profile":
                self.crawl_profile(task)
        except Exception:
            exc_type, exc_obj, tb = sys.exc_info()
            print(os.getpid(), exc_type, exc_obj, "at", tb.tb_lineno)
            self.queue.put(body)

    def run(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            self.callback(task)
        self.queue.put(None)
