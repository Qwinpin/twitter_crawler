import off_api as oa
import bypass_api as ba
from setting import set_parameters

#examples

#off api
#api = oa.login()
#data_1, err = oa.get_tweets_3200(api, settings)
#print (data_1[0].text.encode('utf-8'))
#print(err)

#nonoff api
#in net implementation - class of workers, threads
def worker():
    #Set i - use when request sender is failed, err - use for debag, cook - if we failed in some iter we start it bagen from breakpoint
    #data - data at all
    i = True
    err = 'err_request'
    cook = None
    data = None
    while ((err == 'err_request') and (i)):
        print('start')
        settings = set_parameters(maxTweets = 42, since = '2017-01-20', querySearch = 'cat', cookies = cook)
        data, err, cook = ba.parse(settings)
        i = False
    return data, err

data_2, err = worker()
if data_2 is None:
    print(err)
else:
    print(data_2[0].text)
    print(err)
