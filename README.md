Twitter crawler

off_api - default and official Twitter API, use only for lightweight task: get less than 3200 tweets, get meta-info like followes, friends
WARN: dont forget to use your keys and secret for api auth (actually is used AppAuth for additional number of available queries: 450 against 180 in user auth)

bypass_api - use for heavy and more flexible requests: get all user's tweets, search-requests for high-popular event et al

class parameters include few settings for details

Requirements:
 - Python 2.7 (for 3.6 you need to edit the used modules, it will be later)
 - PyQuery (used to parse web-page)
 - Tweepy - https://github.com/tweepy/tweepy

Used GetOldTweets-python by Jefferson-Henrique (https://github.com/Jefferson-Henrique/GetOldTweets-python) - realy thx, u greate man

In future:
 - interface to interact with different type of modules
   - setting parameters
   - setting whitch data to save
   - setting control for exceptions
 - python 3.6 support
 - progress-bar (REALY IMPORTANT)
 - some data analysis
 - visualization