import json, re, datetime, sys
from pyquery import PyQuery
import requests

class Tweet:
    def __init__(self):
        pass
#send request to twitter, get json-data
def getJsonReponse(parameters, refreshCursor, cookieJar, proxy):
    try:
        response = requests.get((parameters['url'] + refreshCursor), cookies = cookieJar, headers = parameters['headers'])
        jsonResponse = response.json()
        print(response.status_code)
    except:
        print("Twitter weird response. Try to see on browser: ", response.url)
        sys.exit()
    
    return jsonResponse

#parse json data, refresh 'page' to download new tweets
def parse(parameters, receiveBuffer = None, bufferLength = 100, proxy = None, cookieJar = None):
    refreshCursor = ''
    results = []
    resultsAux = []

    if cookieJar is None:
        cookieJar = requests.cookies.RequestsCookieJar()
    i = 0

    active = True
    while active:
        if i % 100 == 0:
            print(len(results))
        i += 1

        try:
            json = getJsonReponse(parameters, refreshCursor, cookieJar, proxy)
        except:
            return results, 'err_request', cookieJar
        
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
            tweet.text = txt.encode('utf-8')
            tweet.created_at = datetime.datetime.fromtimestamp(dateSec)
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

#prepare url, headers, numbers of tweets, create dict, call parse function
def get_tweets(parameters):
    #if element is None just dont use it
    url = 'https://twitter.com/i/search/timeline?f=tweets&q='
    for i in parameters[1]:
        if i[1] is not None:
            url += i[0] + i[1]

    headers = {
        'Host': "twitter.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Language': "ru-RU,de,en-US;q=0.7,en;q=0.3",
        'X-Requested-With': "XMLHttpRequest",
        'Referer': url,
        'Connection': "keep-alive"
    }

    maxTweets = parameters[0]['maxTweets']
    topTweets = parameters[0]['topTweets']
    cookieJar = parameters[0]['cookies']
    query = {'headers': headers, 'url': url, 'maxTweets': maxTweets, 'topTweets': topTweets}
    return parse(query, cookieJar)
