Twitter crawler

off_api - default and official Twitter API, use only for lightweight task: get less than 3200 tweets, get meta-info like followes, friends
WARN: dont forget to use your keys and secret for api auth (actually is used AppAuth for additional number of available queries: 450 against 180 in user auth)

bypass_api - use for heavy and more flexible requests: get all user's tweets, search-requests for high-popular event et al

Requirements:
 - Python 2.7/3.6
 - PyQuery
 - pika
 - rabbitmq-server
 - sqlite3
 - Tweepy - https://github.com/tweepy/tweepy
