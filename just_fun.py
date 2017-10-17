import bypass_api as ba
from setting import set_parameters
import csv
#from pandas import read_csv

#settings = set_parameters(querySearch = 'fuck', maxTweets = 300)
res = []

#lis = read_csv('C:\github\\twitter_crawler\mat2.csv', names = ['w', 'i'])
lis2 = ['bitch','fuck','whore','suck', 'asshole', 'shit', 'cunt', 'putin']
lis3 = ['asshole','shit','cunt', 'putin']
lis4 = ['bitcoin law', 'law', 'bitcoin']

lll = ['putin']
for word in lll:
    time = ['2017-07-20', '2017-05-21']
    settings = set_parameters(maxTweets = 500, since = time[0], querySearch = word)
    data, err, cookies = ba.get_tweets(settings)
    for tweets in data:
        res.append([tweets.text, tweets.screenname, tweets.created_at, tweets.geo])
    print(res, len(res))
    name = './data/' + time[0] + '_' + word + '.csv'
    with open('C:\\github\\twitter_crawler\\mattestr2.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([word, len(data), time[0]])

    with open(name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in res:
            csv_writer.writerow(item)
    res = []
