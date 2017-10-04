import off_api as oa
import bypass_api as ba
from setting import set_parameters

#examples
settings = set_parameters(screen_name = 'blessmepadre', maxTweets = 3)

#off api
#api = oa.login()
#data_1, err = oa.get_tweets_3200(api, settings)
#print (data_1[0].text.encode('utf-8'))
#print(err)

#nonoff api
data_2, err = ba.get_tweets(settings)
print(data_2[0].text)
print(err)