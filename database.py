import csv
import sqlite3 as sql
from tqdm import tqdm

class DataBase:
    def save(self, tweets, settings):
        pass


# TODO сохранение в бд на сервере
class CsvDB(DataBase):
    def __init__(self, filename, rewrite=False):
        self.filename = filename
        self.rewrite = rewrite

    def save(self, tweets):
        mode = 'wb' if self.rewrite else 'a'
        with open(self.filename, mode=mode, encoding='utf-8') as csv_file:
            wr = csv.writer(csv_file, delimiter=',')
            for tweet in tweets:
                wr.writerow(list(tweet))

class SQLite3(DataBase):
    def __init__(self, filename):
        self.table = filename
        self.db = sql.connect('.//twitter.db')
        self.cursor = self.db.cursor()
    
    def save(self, tweets, query):
        for row in tqdm(tweets):
            try:
                self.cursor.execute('''INSERT INTO tweets(id_str, screenname, created_at, text, \
                    url, reply_to, favorites, replies, retweets, likes_users, retweet_users, pic)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', (row.id_str,row.screenname, row.created_at, \
                    row.text, query['url'], row.reply_to, row.favorites, row.reply, row.retweets, \
                    ', '.join(['-'.join('{} : {}'.format(key, value) for key, value in d.items()) \
                                for d in row.likes_users]), 
                    ', '.join(['-'.join('{} : {}'.format(key, value) for key, value in d.items()) \
                                for d in row.retweet_users]), 
                    row.pic
                ))
            except sql.IntegrityError as e:
                pass
        self.db.commit()