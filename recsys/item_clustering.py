from datetime import datetime
from numpy import array
import numpy
from scipy.cluster.vq import kmeans, vq


def compute_fft_full(dataset):
    tweets_per_day = compute_occurrences_full(dataset)
    ffts = list()
    ffts_labels = list()
    for item_id in tweets_per_day:
        ffts_labels.append(item_id)
        ffts.append(numpy.abs(numpy.fft.fft(tweets_per_day[item_id])))
    return ffts, ffts_labels


def compute_fft(dataset):
    tweets_per_day = compute_occurrences(dataset)
    ffts = list()
    ffts_labels = list()
    for item_id in tweets_per_day:
        ffts_labels.append(item_id)
        ffts.append(numpy.abs(numpy.fft.fft(tweets_per_day[item_id])))
    return ffts, ffts_labels, tweets_per_day


def compute_fft_for_test(train_tweets_per_day, test, tweet):
    tweets_per_day = compute_occurrences_for_test(train_tweets_per_day, test, tweet)
    return numpy.abs(numpy.fft.fft(tweets_per_day))


def run_kmeans(whitened, k=3):
    book = list()
    for i in range(k):
        book.append(whitened[i])
    codebook, distortion = kmeans(whitened, array(book))
    return codebook


def assign_clusters(whitened, labels, codebook):
    (codes, dist) = vq(whitened, codebook)

    clusters = dict()
    i = 0
    for label in labels:
        clusters[label] = codes[i]
        i += 1
    return clusters


def assign_clusters_for_test(whitened, codebook):
    (codes, dist) = vq(whitened, codebook)
    return codes[0]


def compute_occurrences_full(tweets):
    tweets_per_day = dict()
    for tweet in tweets:
        item_id = tweet['imdb_item_id']

        start_date_str = '2013-02-28'
        tweet_date_str = tweet['tweet_created_at']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        tweet_date = datetime.strptime(tweet_date_str, '%Y-%m-%d')
        day_number = (tweet_date - start_date).days

        if item_id in tweets_per_day:
            tweets_per_day[item_id][day_number] += 1
        else:
            tweets_per_day[item_id] = [0] * 390
            tweets_per_day[item_id][day_number] = 1
    return tweets_per_day


def compute_occurrences(tweets):
    tweets_per_day = dict()
    for tweet in tweets:
        item_id = tweet['imdb_item_id']

        start_date_str = '2013-02-28'
        tweet_date_str = tweet['tweet_created_at']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        tweet_date = datetime.strptime(tweet_date_str, '%Y-%m-%d')
        day_number = (tweet_date - start_date).days

        if item_id in tweets_per_day:
            tweets_per_day[item_id][day_number] += 1
        else:
            tweets_per_day[item_id] = [0] * 315
            tweets_per_day[item_id][day_number] = 1
    return tweets_per_day


def compute_occurrences_for_test(train_tweets_per_day, test, tweet):
    test_tweet_id = float(tweet['tweet_id'])
    test_item_id = tweet['imdb_item_id']
    test_tweet_date_str = tweet['tweet_created_at']

    tweets_per_day_for_item = [0] * 315

    start_date = datetime.strptime('2013-02-28', '%Y-%m-%d')
    from_date = datetime.strptime(test_tweet_date_str, '%Y-%m-%d')
    total_day_number = (from_date - start_date).days
    train_day_number = (total_day_number - 315) + 1
    if test_item_id in train_tweets_per_day:
        for day in range(0, 315 - train_day_number):
            tweets_per_day_for_item[315 - train_day_number - day - 1] += train_tweets_per_day[test_item_id][day]

    for tweet in test:
        tweet_id = float(tweet['tweet_id'])
        item_id = tweet['imdb_item_id']
        if item_id == test_item_id and tweet_id <= test_tweet_id:
            tweet_date = datetime.strptime(tweet['tweet_created_at'], '%Y-%m-%d')
            day_number = (from_date - tweet_date).days
            if day_number < 315:
                tweets_per_day_for_item[day_number] += 1
    return tweets_per_day_for_item