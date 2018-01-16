import csv
import sqlite3 as sql

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
        for row in tweets:
            self.cursor.execute('''INSERT INTO tweets(id, screen_name, date, text, query)
                  VALUES(?,?,?,?,?)''', (row.id_str,row.screenname, row.created_at, row.text, '_'.join(query)))
        self.db.commit()