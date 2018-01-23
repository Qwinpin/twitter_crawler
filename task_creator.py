from requests.utils import quote
import json
import itertools
import datetime


def create_query(screen_name=None, maxTweets=None, since=None, until=None, querySearch='',
                 topTweets=False, near=None, within=None, cookies=None):
    parameters_url = (
        ('', querySearch),
        (' from:', screen_name),
        (' near:', near),
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
    if parameters_url[0][1] != '':
        url = 'https://twitter.com/i/search/timeline?l=&q='
    else:
        url = 'https://twitter.com/i/search/timeline?l=&q='

    for i in parameters_url:
        if i[1] is not None:
            url += i[0] + i[1]

    headers = {
        'Host': "twitter.com",\
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",\
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
        'Accept-Language': "en-US,en;q=0.5", \
        'Connection': "keep-alive" }    

    maxTweets = maxTweets
    topTweets = topTweets
    cookieJar = cookies

    query = {
        'headers': headers,
        'url': url,
        'maxTweets': maxTweets,
        'topTweets': topTweets,
        'cookies': cookieJar
    }

    return query


def parse_location(geo):
    if geo is None:
        return None
    lon = geo["lon"] if "lon" in geo else 0
    lat = geo["lat"] if "lat" in geo else 0
    return ",".join([str(lon), str(lat)])


def date_range(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
    yield end


def create_tasks(queries, saveParam):
    tasks = []
    for q in queries:
        print(q)
        maxTweets = q['maxTweets'] if ('maxTweets' in q) else None
        now = datetime.datetime.today()
        topTweets = q['topTweets'] if 'topTweets' in q else None

        a = []
        if 'querySearch' in q:
            a.append([('querySearch', geo) for geo in q['querySearch']])
        if 'locations' in q:
            a.append([('geo', geo) for geo in q['locations']])
        if 'screen_name' in q:
            a.append([('screen_name', geo) for geo in q['screen_name']])

        since = datetime.datetime.strptime(q['since'], '%Y-%m-%d') \
            if ('since' in q) \
            else now - datetime.timedelta(weeks=4 * 6)

        until = datetime.datetime.strptime(q['until'], '%Y-%m-%d') \
            if ('until' in q) \
            else now

        dates = list(map(lambda d: str(d.date()), date_range(since, until, datetime.timedelta(weeks=1))))
        intervals = [('interval', (d1, d2)) for d1, d2 in zip(dates[:-1], dates[1:])]
        a.append(intervals)

        params = itertools.product(*a)

        for element in params:
            p = dict([(a, b) for a, b in element])
            mes = create_query(
                screen_name=p.get('screen_name'),
                near=parse_location(p.get('geo')),
                within=str(p['geo']['radius']) + 'km' if 'geo' in p else None,
                maxTweets=maxTweets,
                since=p.get('interval')[0],
                until=p.get('interval')[1],
                querySearch=p['querySearch'] if 'querySearch' in p else '',
                topTweets=topTweets)

            tasks.append(json.dumps({
                'query_param': mes,
                'save_param': saveParam
            }))

    return tasks
