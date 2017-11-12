import json, re, datetime, sys
from pyquery import PyQuery
import requests

class Tweet:
    def __init__(self):
        pass
    def to_csv(self, save_settings):
        #TODO нужен другой сепаратор csv файла
        return ",".join([self.__dict__[field[0]] for field in save_settings if field[1] is True])

def to_csv(tweets, filename, save_settings, rewrite=True):
    mode = 'w' if rewrite else 'a'
    with open(filename, mode=mode, encoding='utf-8') as file:
        for tweet in tweets:
            file.write(tweet.to_csv(save_settings) + '\n')

        
#parse json data, refresh 'page' to download new tweets
def parse(parameters, receiveBuffer = None, bufferLength = 100, proxy = None):
    refreshCursor = ''
    results = []
    resultsAux = []

    if parameters['cookies'] is None:
        cookieJar = requests.cookies.RequestsCookieJar()
    else:
        cookieJar = parameters['cookies']
    i = 0

    active = True
    while active:
        if i % 100 == 0:
            print(len(results))
        i += 1

        try:
            response = requests.get((parameters['url'] + refreshCursor), cookies = cookieJar, headers = parameters['headers'])
        except:
            return results, 'err_request', cookieJar
        
        json = response.json()

        try:
            if len(json['items_html'].strip()) == 0:
                break
        except:
            break

        refreshCursor = json['min_position']
        tweets = PyQuery(json['items_html'])('div.js-stream-tweet')
        
        if len(tweets) == 0:
            break
        #parse and add to object to return
        for tweetHTML in tweets:
            tweetPQ = PyQuery(tweetHTML)
            tweet = Tweet()
            usernameTweet = tweetPQ("span:first.username.u-dir b").text()
            txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
            #retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
            #favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
            dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
            id = tweetPQ.attr("data-tweet-id")
            #permalink = tweetPQ.attr("data-permalink-path")
            
            geo = ''
            geoSpan = tweetPQ('span.Tweet-geo')
            if len(geoSpan) > 0:
                geo = geoSpan.attr('title')
            
            tweet.id_str = id
            #tweet.permalink = 'https://twitter.com' + permalink
            tweet.screenname = usernameTweet
            #TODO пофиксить кодировку. encode возвращает массив байтов. русский не робит
            tweet.text = txt#.encode('utf-8')
            tweet.created_at = datetime.datetime.fromtimestamp(dateSec).strftime("%Y-%m-%d %H:%M:%S")
            #tweet.retweets = retweets
            #tweet.favorites = favorites
            #tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
            #tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
            tweet.geo = geo
            results.append(tweet)
            resultsAux.append(tweet)
            
            if receiveBuffer and len(resultsAux) >= bufferLength:
                receiveBuffer(resultsAux)
                resultsAux = []
            #if we set limit for number of tweets
            if parameters['maxTweets'] > 0 and len(results) >= parameters['maxTweets']:
                active = False
                break

    if receiveBuffer and len(resultsAux) > 0:
        receiveBuffer(resultsAux)

    return results, 0, cookieJar

#for future, return sets of date-range, like [(2016-12-12, 2016-12-24), (2016-12-24, 2016-12-31)]
def date_prepare(parameters):

    start = parameters.since
    end = parameters.until
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')

    days_between = (end - start).days
    date_list = [(str(end - datetime.timedelta(days=x))[:10], str(end - datetime.timedelta(days=(x + 1)))[:10]) for x in range(days_between)]
    print(date_list)

