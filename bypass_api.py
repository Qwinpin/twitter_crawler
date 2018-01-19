import re
import datetime
from pyquery import PyQuery
import requests


class Tweet:
    def __init__(self, save_settings):
        self.save_settings = save_settings

    def __iter__(self):
        return iter([self.__dict__[field]
                     for field in self.save_settings
                     if hasattr(self, field) and self.save_settings[field]])

    def to_csv(self):
        return ",".join([self.__dict__[field]
                         for field in self.save_settings
                         if self.save_settings[field]])

def parse_page(tweetHTML, parameters, save_settings, id_origin=''):
    if id_origin != '':
        print('5 WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP')
    tweetPQ = PyQuery(tweetHTML)
    tweet = Tweet(save_settings)
    usernameTweet = tweetPQ("span:first.username.u-dir b").text()
    txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
    retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count"))
    favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count"))
    try:
        dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
    except:
        dateSec = 0
    ids = tweetPQ.attr("data-tweet-id")
    permalink = tweetPQ.attr("data-permalink-path")

    geo = ''
    geoSpan = tweetPQ('span.Tweet-geo')
    if len(geoSpan) > 0:
        geo = geoSpan.attr('title')


    likes_users = []
    likes_url = 'https://twitter.com/i/activity/favorited_popup?id=' + str(ids)
    likes_headers = parameters['headers']
    likes_headers['Referer'] = likes_url
    likes_cookieJar = requests.cookies.RequestsCookieJar()
    try:
        likes_response = requests.get((likes_url), cookies=likes_cookieJar,
                            headers=likes_headers)
    except:
        likes_users = []
    else:
        likes = PyQuery(likes_response.json()['htmlUsers'])('ol')
        for i in likes[0]:
            likes_users.append({'id': PyQuery(i)('div.account').attr('data-user-id'), \
                                'screenname': PyQuery(i)('div.account').attr('data-name')})

    retweet_users = []
    retweet_url = 'https://twitter.com/i/activity/retweeted_popup?id=' + str(ids)
    retweet_headers = parameters['headers']
    retweet_headers['Referer'] = retweet_url
    retweet_cookieJar = requests.cookies.RequestsCookieJar()
    try:
        retweet_response = requests.get((retweet_url), cookies=retweet_cookieJar,
                            headers=retweet_headers)
    except:
        retweet_users = []
    else:
        retweet = PyQuery(retweet_response.json()['htmlUsers'])('ol')
        for i in retweet[0]:
            retweet_users.append({'id': PyQuery(i)('div.account').attr('data-user-id'), \
                                'screenname': PyQuery(i)('div.account').attr('data-name')})

    tweet.id_str = ids
    tweet.permalink = 'https://twitter.com' + permalink
    tweet.screenname = usernameTweet
    tweet.text = txt.encode('utf-8').decode('utf-8')
    if dateSec != 0:
        tweet.created_at = datetime.datetime.fromtimestamp(dateSec).strftime("%Y-%m-%d %H:%M:%S")
    else:
        tweet.created_at = '1970-01-01'
    tweet.retweets = retweets
    tweet.favorites = favorites
    tweet.retweet_users = retweet_users
    tweet.likes_users = likes_users
    tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
    tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
    tweet.geo = geo
    tweet.reply_to = id_origin
    return {'tweet': tweet, 'id': ids, 'name': usernameTweet}

# parse json data, refresh 'page' to download new tweets
def parse(parameters, save_settings, receiveBuffer=None, bufferLength=100, proxy=None):
    refreshCursor = ''
    results = []
    resultsAux = []
    # if cookies in not None - it's mean repeating of the task
    if parameters['cookies'] is None:
        cookieJar = requests.cookies.RequestsCookieJar()
    else:
        cookieJar = parameters['cookies']
    active = True
    while active:
        # if any error - return current results and cookies for task manager
        try:
            response = requests.get((parameters['url'] + refreshCursor), cookies=cookieJar,
                                    headers=parameters['headers'])
        except:
            return results, 'err_request', cookieJar
        try:
            json = response.json()
        except:
            json = {'items_html': ''}

        try:
            if len(json['items_html'].strip()) == 0:
                break
        except:
            break

        refreshCursor = json['min_position']
        tweets = PyQuery(json['items_html'])('div.js-stream-tweet')

        if len(tweets) == 0:
            break
        # parse and add to object to return
        for tweetHTML in tweets:
            data = parse_page(tweetHTML, parameters, save_settings)
            results.append(data['tweet'])
            resultsAux.append(data['tweet'])

            reply_refreshCursor = ''
            reply_url ='https://twitter.com/' + data['name'] + '/status/' + data['id'] + '?conversation_id=' + data['id']
            reply_headers = parameters['headers']
            reply_headers['Referer'] = reply_url
            reply_cookieJar = requests.cookies.RequestsCookieJar()
            try:
                reply_response = requests.get((reply_url), cookies=reply_cookieJar,
                                        headers=reply_headers)
            except:
                print('1 WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP')
                reply_tweets = []
            else:
                reply_active = True
                while reply_active:
                    try:
                        reply_json = reply_response.json()
                    except:
                        print('2 WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP')
                        break
                    
                    try:
                        if len(json['items_html'].strip()) == 0:
                            reply_tweets = []
                    except:
                        print('3 WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP')
                        break
                    if reply_refreshCursor == '':
                        reply_refreshCursor = PyQuery(json['page'])('div.stream-container').attr('data-min-position')
                        reply_tweets = PyQuery(json['page'])('div.js-stream-tweet')
                    else:
                        reply_refreshCursor = json['descendants']['min_position']
                        reply_tweets = PyQuery(json['items_html'])('div.js-stream-tweet')

                    for reply_tweetHTML in reply_tweets:
                        reply_data = parse_page(tweetHTML, parameters, save_settings, data['id'])
                        results.append(reply_data['tweet'])

                    if parameters['maxTweets'] is not None:
                        if 0 < parameters['maxTweets'] <= len(results):
                            reply_active = False
                            break
                    
                    reply_url = 'https://twitter.com/i/' + data['name'] + '/conversation/' + data['id'] + \
                            '?include_available_features=1&include_entities=1&max_position=' + \
                            reply_refreshCursor + '&reset_error_state=false'
                    try:
                        reply_response = requests.get((reply_url + reply_refreshCursor), cookies=reply_cookieJar,
                                        headers=reply_headers)
                    except:
                        print('4 WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP')
                        break

            if receiveBuffer and len(resultsAux) >= bufferLength:
                receiveBuffer(resultsAux)
                resultsAux = []
            # if we set limit for number of tweets
            # if parameters['maxTweets'] is not None:
            if parameters['maxTweets'] is not None:
                if 0 < parameters['maxTweets'] <= len(results):
                    active = False
                    break

    if receiveBuffer and len(resultsAux) > 0:
        receiveBuffer(resultsAux)

    return results, 0, cookieJar


# for future, return sets of date-range, like [(2016-12-12, 2016-12-24), (2016-12-24, 2016-12-31)]
def date_prepare(parameters):
    start = parameters.since
    end = parameters.until
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')

    days_between = (end - start).days
    date_list = [(str(end - datetime.timedelta(days=x))[:10], str(end - datetime.timedelta(days=(x + 1)))[:10]) for x in
                 range(days_between)]
    print(date_list)
