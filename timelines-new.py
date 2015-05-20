import re
import csv
import tweepy
import sys
import json
from time import sleep

accounts = [
{   'api_key': '***',
    'api_secret': '***',
    'access_token': '***',
    'access_secret': '***'
},
{   'api_key': '***',
    'api_secret': '***',
    'access_token': '***',
    'access_secret': '***'
}
]


def authenticate(account):
    # login to api
    # create api object
    auth = tweepy.OAuthHandler(account['api_key'], account['api_secret'])
    auth.set_access_token(account['access_token'], account['access_secret'])
    return tweepy.API(auth)


def get_tweets(api, user_id):
    try:
        tweets = [SimpleTweet(tweet) for tweet in api.user_timeline(user_id)]
        print(tweets)

        json_tweets = []
        found_location = None
        for tweet in tweets:
            if tweet.coordinates != 'Coordinates not found':
                found_location = tweet.coordinates
                break

        for tweet in tweets:
            text_geo = tweet.text_geo()

            if tweet.coordinates == 'Coordinates not found':
                if found_location is None:
                    # No hope of location data...
                    return None

                text_geo['coordinates'] = found_location
            json_tweets.append(text_geo)

        d = {
            'id': user_id,
            'tweets': json_tweets
        }
        return json.dumps(d)
    except tweepy.TweepError as e:
        # over-used API code
        if e.response.status_code == 429:
            sleep(5 * 60)

            # Recurse... very very dangerous
            return get_tweets(api, user_id)
        return None


class SimpleTweet:
    def __init__(self, tweet):
        data = get_essential_data(tweet)
        self.text = clean_text(data['text'])
        self.id = data['id']
        self.screen_name = data['screen_name']
        self.coordinates = data['coordinates']
        self.fix_coordinate_order()
        self.json = tweet._json
        # self.zipcode = lat_long_to_zipcode(self.coordinates)

    def __str__(self):
        return self.txt

    def __repr__(self):
        return json.dumps({'text': self.text, 'user': self.screen_name})

    def fix_coordinate_order(self):
        """ Twitter sends coordinates in 'wrong' order.  Reverse them."""
        try:
            self.coordinates['coordinates'].reverse()
        except TypeError:
            pass # for tweets with no location

    def text_geo(self):
        return {'text': self.text, 'coordinates': self.coordinates}



def get_essential_data(tweet):
    """ Pull the data that we care about out of the tweet
    There's a lot of duplication in there
    """
    data = {}
    data['id'] = tweet.id
    data['screen_name'] = tweet.user.screen_name
    data['text'] = tweet.text
    try:
        data['coordinates'] = tweet.coordinates['coordinates']
    except TypeError:
        data['coordinates'] = "Coordinates not found"
    return data


def clean_text(text):
    emoji_regex = re.compile(u'['
                             u'\U0001F300-\U0001F64F'
                             u'\u2014'
                             u'\u2026'
                             u'\U0001F680-\U0001F6FF'
                             u'\u2600-\u26FF\u2700-\u27BF]+',
                             re.UNICODE)
    single_quote_regex = re.compile(u'[' u"\u2018" u"\u2019"']')
    double_quote_regex = re.compile(u'[' u"\u201c" u"\u201d"']')
    result = text
    result = emoji_regex.sub('', result)
    result = single_quote_regex.sub("'", result)
    result = double_quote_regex.sub("'", result)
    return result


def main():
    count = 1
    api = authenticate(accounts[int(sys.argv[2])])
    output_file = open(sys.argv[1] + '.results.txt', 'a')

    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for id, bad_location in reader:
            tw = get_tweets(api, id)
            print(count)
            if tw:
                output_file.write(str(tw) + '\n')
            count += 1

if __name__ == '__main__':
    main()
