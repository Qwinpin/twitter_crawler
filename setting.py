def set_parameters(screen_name = None, maxTweets = 1, since = None, until = None, querySearch = None, 
    topTweets = False, near = None, within = None, cookies = None):
    parameters_url = (
        (' from:', screen_name),
        ('', querySearch),
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