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

    return parameters_api, parameters_url
