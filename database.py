import csv

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
