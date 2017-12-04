# -*- coding: utf-8 -*-
"""
Test module for overload requests
"""
import csv

import bypass_api as ba
from setting import set_parameters

res = []

lis2 = ['bitch', 'fuck', 'whore', 'suck', 'asshole', 'shit', 'cunt', 'putin']
lis3 = ['любовь', 'cunt', 'putin']
lis4 = ['bitcoin law', 'law', 'bitcoin']
lll = ['уфа']

for word in lll:
    time = ['2015-11-21', '2017-12-17']
    settings = set_parameters(maxTweets=0, since=time[0], until=time[1], querySearch=word)
    data, err, cookies = ba.parse(settings)
    for tweets in data:
        res.append([tweets.text, tweets.screenname, tweets.created_at, tweets.geo])
    print(res, err)
    name = './data/' + time[0] + '_' + word + '.csv'
    with open('C:\\github\\twitter_crawler\\mattestr2.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([word, len(data), time[0]])

    with open(name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in res:
            csv_writer.writerow(item)
    res = []
