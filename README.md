# ![logo](./logo_mini.png) Twitter crawler

Python-based crawler for tweets and profiles:

1.  **Without limitations** of the official API
2.  Multithreaded
3.  Support for recursive crawling
4.  **Flexible query**

If you need data, i mean A LOT of data - welcome!
Distributed, scaling and without any (almost) limitation crawler for Twitter.
Easy to use, allow to collect more than 1.000.000 tweets per day (depends on you network and resources).
Do not judge us.

Supported collecting:

1.  Tweets:
    1.  Text
    2.  Id, Screen name
    3.  Retweets
    4.  Favorites
    5.  Replies
    6.  Geo
2.  Profiles:
    1.  Id, Screen name, Name
    2.  Date of creation
    3.  Date of birthday
    4.  Bio
    5.  Place
    6.  Site
    7.  Followers, followings, favorites (just numbers)

## Installation:

`pip install -r requirements.txt`

## How to

1.  Use `empty.db` file as a database for crawler. Set a route to file in code or using cmd args. Please dont push changes of this file.
2.  Use `config/save_settings.json` to set what data to save. Dont touch this.
3.  Use `config/query.json` to set what to crawl. Change screen_name array here.

```json
[
  {
    "screen_name": ["nickname1", "nickname2"],
    "since": "2007-01-01",
    "recursion": 4
  }
]
```

4.  **Run `python crawler/runner.py` with cmd args is needed**

**FULL USAGE INSTRUCTIONS TBD**
