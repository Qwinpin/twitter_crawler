#import off_api as oa
import bypass_api as ba
from task_creator import set_parameters, set_save_parameters
#examples

def worker():
    #Set i - use when request sender is failed, err - use for debag, 
    #cook - if we failed in some iter we start it bagen from breakpoint
    #data - data at all
    i = True
    err = 'err_request'
    cook = None
    data = None
    while err == 'err_request' and i:
        print('start')
        settings = set_parameters(since='2016-10-12', until='2016-12-14', querySearch='Путин')
        data, err, cook = ba.parse(settings)
        i = False
    return data, err

def main():
    data_2, err = worker()
    if data_2 is None:
        print(err)
    else:
        print(data_2[0].text)
        ba.to_csv(data_2, 'tweets.csv', set_save_parameters())
        print(err)

if __name__ == '__main__':
    main()
