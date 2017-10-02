from parameters import Parameters
import off_api as oa
import bypass_api as ba
#api = oa.login()
para = Parameters().setUsername('blessmepadre').setSince('2017-09-01').setUntil('2017-09-03').setMaxTweets(30000)
#ba.get_tweets_by_data(para)
#a, b = oa.get_followers(api, para)
#print(b)
#c, d = oa.get_tweets_3200(api, para)
#print(d)
twe = ba.getTweets(para)
print(twe[0].text)
print(len(twe))
