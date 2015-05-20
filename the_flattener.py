# The Flattener

import sys
import json

file = open(sys.argv[1])

line = file.readline().strip()
tweets = []
while line:
    users_10_tweets = json.loads(line)
    for tweet in users_10_tweets['tweets']:
        tweets.append({'userId': users_10_tweets['id'], 'text': tweet['text'], 'coordinates': tweet['coordinates']})
    line = file.readline().strip()

print (json.dumps(tweets))
