# python 2
from positive import positive
from negative import negative
import json
import re
import sys
from pyspark import SparkContext

positives = set(positive)
negatives = set(negative)


def word_counter(text):
    d = {}
    text = re.sub(r'[,.:?\'!();]', '', text)
    for word in text.split():
        lword = word.lower()
        if d.get(lword) is None:
            d[lword] = 1
        else:
            d[lword] += 1
    return d


def count(d, word):
    count = d.get(word)
    if count is None:
        return 0
    else:
        return count


def calculate_happiness_ratio(message):
    words = word_counter(message)
    score = 0
    total_words = 0
    for word, count in words.items():
        if word in positives:
            total_words += count
            score += count
        elif word in negatives:
            total_words += count
    if total_words == 0:
        return None
    else:
        return float(score) / total_words


def map_function(line):
    info = json.loads(line)
    r = calculate_happiness_ratio(info['text'])
    if r is None:
        return ('unclassified', {'count': 1, 'ratio': 0.5})

    computed = {'ratio': r, 'count': 1}
    return (str(info['zipcode']), computed)


def reduce_for_like_keys_function(value1, value2):
    ret = {}
    ret['ratio'] = (value1['ratio'] + value2['ratio']) / 2.0
    ret['count'] = value1['count'] + value2['count']
    return ret


json_file = sys.argv[1]  # /Users/nsundin/Dropbox/dsdata/Spark/tweets-new.json
sc = SparkContext('local', 'Twitter Aggregator')

tweets = sc.textFile(json_file).cache()

results = tweets.map(map_function)
results = results.reduceByKey(reduce_for_like_keys_function)

for result in results.collect():
    print json.dumps(result)
