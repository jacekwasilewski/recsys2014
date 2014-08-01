from datetime import datetime
from numpy import array
import numpy
from scipy.cluster.vq import kmeans, vq


def compute_fft(dataset):
    tweets_per_day = compute_occurrences(dataset)
    ffts = list()
    ffts_labels = list()
    for item_id in tweets_per_day:
        ffts_labels.append(item_id)
        ffts.append(numpy.abs(numpy.fft.fft(tweets_per_day[item_id])))
    return ffts, ffts_labels


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
            tweets_per_day[item_id] = [0] * 390
            tweets_per_day[item_id][day_number] = 1
    return tweets_per_day