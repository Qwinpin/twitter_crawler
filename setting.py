from requests.utils import quote

def set_parameters(screen_name=None, maxTweets=1, since=None, until=None, querySearch=None, 
    topTweets=False, near=None, within=None, cookies=None):
    print(quote(querySearch))
    parameters_url = (
        (' from:', screen_name),
        ('', quote(querySearch)),
        ('&near:', near),
        (' within:', within),
        (' since:', since),
        (' until:', until),
        ('&src=typd&max_position=', '')
    )

    parameters_api = {
        'screen_name': screen_name, 
        'maxTweets': maxTweets,
        'topTweets': topTweets,
        'cookies': cookies
    }

    url = 'https://twitter.com/i/search/timeline?f=tweets&q='
    for i in parameters_url:
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

    maxTweets = maxTweets
    topTweets = topTweets
    cookieJar = cookies
    query = {'headers': headers, 'url': url, 'maxTweets': maxTweets, 'topTweets': topTweets, 'cookies': cookieJar}

    return query

def set_save_parameters(id_str=True, permalink=False, screenname=True,text=True,
                        created_at=True, retweets=False, favorites=False,
                        mentions=False, hashtags=False, geo=True):
    return (
        ('id_str', id_str),
        ('permalink', permalink),
        ('screenname', screenname),
        ('text', text),
        ('created_at', created_at),
        ('retweets', retweets),
        ('favorites', favorites),
        ('mentions', mentions),
        ('hashtags', hashtags),
        ('geo', geo)
    )
    