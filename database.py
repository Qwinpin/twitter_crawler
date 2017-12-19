class DataBase:
    def save(self, tweets):
        print('dssd')


class CsvDB(DataBase):
    def __init__(self, filename, rewrite=False):
        self.filename = filename
        self.rewrite = rewrite

    def save(self, tweets, settings):
        mode = 'w' if self.rewrite else 'a'
        with open(self.filename, mode=mode, encoding='utf-8') as file:
            for tweet in tweets:
                file.write(tweet.to_csv(settings) + '\n')

