import urllib, urllib2, json, re, datetime, sys, cookielib
from pyquery import PyQuery
import csv
import requests

class Tweet:
    def __init__(self):
        pass

def getJsonReponse(parameters, refreshCursor, cookieJar, proxy):
    url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"
        
    urlGetData = ''
        
    if hasattr(parameters, 'username'):
        urlGetData += ' from:' + parameters.username
        
    if hasattr(parameters, 'querySearch'):
        urlGetData += ' ' + parameters.querySearch
        
    if hasattr(parameters, 'near'):
        urlGetData += "&near:" + parameters.near + " within:" + parameters.within
        
    if hasattr(parameters, 'since'):
        urlGetData += ' since:' + parameters.since
            
    if hasattr(parameters, 'until'):
        urlGetData += ' until:' + parameters.until
        

    if hasattr(parameters, 'topTweets'):
        if parameters.topTweets:
            url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"
        
        
        
    url = url % (urllib.quote(urlGetData), refreshCursor)

    headers = [
        ('Host', "twitter.com"),
        ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
        ('Accept', "application/json, text/javascript, */*; q=0.01"),
        ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
        ('X-Requested-With', "XMLHttpRequest"),
        ('Referer', url),
        ('Connection', "keep-alive")
    ]

    if proxy:
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxy, 'https': proxy}), urllib2.HTTPCookieProcessor(cookieJar))
    else:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    opener.addheaders = headers

    try:
        response = opener.open(url)
        jsonResponse = response.read()
        #print(jsonResponse)
    except:
        print("Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd", urllib.quote(urlGetData))
        sys.exit()
        return
    
    dataJson = json.loads(jsonResponse)
    print(dataJson)
    return dataJson

def getTweets(parameters, receiveBuffer=None, bufferLength=100, proxy=None):
    refreshCursor = ''
    
    results = []
    resultsAux = []
    cookieJar = cookielib.CookieJar()
    
    name = parameters.username
    if hasattr(parameters, 'username') and (parameters.username.startswith("\'") or parameters.username.startswith("\"")) and (parameters.username.endswith("\'") or parameters.username.endswith("\"")):
        parameters.username = parameters.username[1:-1]

    active = True
    while active:
        print('Still alive')
        try:
            json = getJsonReponse(parameters, refreshCursor, cookieJar, proxy)
        except:
            return results
        if len(json['items_html'].strip()) == 0:
            break
        refreshCursor = json['min_position']            
        tweets = PyQuery(json['items_html'])('div.js-stream-tweet')
        
        if len(tweets) == 0:
            break
        
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
            
            #geo = ''
            #geoSpan = tweetPQ('span.Tweet-geo')
            #if len(geoSpan) > 0:
            #    geo = geoSpan.attr('title')
            
            tweet.id_str = id
            #tweet.permalink = 'https://twitter.com' + permalink
            tweet.screenname = usernameTweet
            tweet.text = txt.encode('utf-8')
            tweet.created_at = datetime.datetime.fromtimestamp(dateSec)
            #tweet.retweets = retweets
            #tweet.favorites = favorites
            #tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
            #tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
            #tweet.geo = geo
                
            results.append(tweet)
            resultsAux.append(tweet)
            
            if receiveBuffer and len(resultsAux) >= bufferLength:
                receiveBuffer(resultsAux)
                resultsAux = []
            
            if parameters.maxTweets > 0 and len(results) >= parameters.maxTweets:
                active = False
                break
                
    
    if receiveBuffer and len(resultsAux) > 0:
        receiveBuffer(resultsAux)

    return results

def date_prepare(parameters):

    start = parameters.since
    end = parameters.until
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')

    days_between = (end - start).days
    date_list = [[str(end - datetime.timedelta(days=x))[:10], str(end - datetime.timedelta(days=(x + 1)))[:10]] for x in range(days_between)]
    print(date_list)

def param_prep(username = None, maxTweets = 0, since = None, until = None, querySearch = None, 
    topTweets = False, near = None, within = '15mi', refreshCursor = ''):
    param_url = dict.fromkeys(['s&src=typd&max_position','from:', ' ', '&near:', 'within:', ' since:', ' until', 'refreshCursor'], ['=', username, querySearch, near, within, since, until, refreshCursor])
    param_search = dict.fromkeys(['maxTweets', 'topTweets'], [maxTweets, topTweets])

    print(param_url)
    return param_url, param_search