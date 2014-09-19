from math import log

from scipy.cluster.vq import whiten
import numpy as np

import item_clustering


def compute_features(dataset, test_dataset):
    print('Computing FFTs...')
    ffts, ffts_labels = item_clustering.compute_fft_full(dataset)

    # running k-means
    print('Clustering items...')
    k = 3
    whitened = whiten(ffts)
    codebook = item_clustering.run_kmeans(whitened, k)
    clusters = item_clustering.assign_clusters(whitened, ffts_labels, codebook)

    print('Calculating statistics...')
    cluster_avg_engs = dict()
    tweets_with_engagement_count = dict()
    tweets_with_engagement_sum = dict()
    users_stats = dict()
    items_stats = dict()

    for tweet in dataset:
        user_id = tweet['user_id']
        if not user_id in users_stats:
            users_stats[user_id] = dict()
            users_stats[user_id]['count'] = 0.0
            users_stats[user_id]['eng_count'] = 0.0

    for i in range(k):
        cluster_avg_engs[i] = dict()
        cluster_avg_engs[i]['eng_count'] = 0.0
        cluster_avg_engs[i]['eng_sum'] = 0.0
        cluster_avg_engs[i]['count'] = 0.0
        cluster_avg_engs[i]['item_count'] = 0.0

    count = 0
    has_retweets_train = set()
    has_retweets_test = set()
    for tweet in dataset:
        if tweet['tweet_is_retweet']:
            has_retweets_train.add(tweet['tweet_retweet_of'])
            has_retweets_test.add(tweet['tweet_retweet_of'])
    for tweet in test_dataset:
        if tweet['tweet_is_retweet']:
            has_retweets_test.add(tweet['tweet_retweet_of'])

    for tweet in dataset:
        count += 1
        item_id = tweet['imdb_item_id']
        rating = tweet['imdb_rating']

        if rating < 1 or rating > 10:
            continue

        num_engagements = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])

        if not item_id in items_stats:
            items_stats[item_id] = dict()
            items_stats[item_id]['count'] = 0
            items_stats[item_id]['ratings_count'] = dict()
            items_stats[item_id]['pop'] = 0
            for r in range(10):
                items_stats[item_id]['ratings_count'][r + 1] = 0.0
            tweets_with_engagement_count[item_id] = 1.0
            tweets_with_engagement_sum[item_id] = 1.0

        items_stats[item_id]['pop'] += 1
        if num_engagements > 0:
            items_stats[item_id]['count'] += 1.0
            items_stats[item_id]['ratings_count'][rating] += 1.0

    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']

        if rating < 1 or rating > 10:
            continue

        num_engagements = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])

        cluster = clusters[item_id]

        cluster_avg_engs[cluster]['count'] += 1.0
        users_stats[user_id]['count'] += 1.0
        if num_engagements > 0:
            users_stats[user_id]['eng_count'] += 1.0
            if not tweet['tweet_is_retweet']:
                cluster_avg_engs[cluster]['eng_count'] += 1.0
                cluster_avg_engs[cluster]['eng_sum'] += int(tweet['tweet_favourite_count']) + int(
                    tweet['tweet_retweet_count'])
            if item_id in tweets_with_engagement_count:
                tweets_with_engagement_count[item_id] += 1.0
                if not tweet['tweet_is_retweet']:
                    tweets_with_engagement_sum[item_id] += int(tweet['tweet_favourite_count']) + int(
                        tweet['tweet_retweet_count'])
                else:
                    tweets_with_engagement_sum[item_id] += 1.0
            else:
                tweets_with_engagement_count[item_id] = 1.0
                if not tweet['tweet_is_retweet']:
                    tweets_with_engagement_sum[item_id] = int(tweet['tweet_favourite_count']) + int(
                        tweet['tweet_retweet_count'])
                else:
                    tweets_with_engagement_sum[item_id] = 1.0

    for item_id in clusters:
        cluster_avg_engs[clusters[item_id]]['item_count'] += 1.0

    clusters_coeff = list()
    for i in range(k):
        clusters_coeff.append(float(log(cluster_avg_engs[i]['eng_sum'] / cluster_avg_engs[i]['eng_count'])))
    clusters_coeff_sorted = np.argsort(clusters_coeff)

    train_features = list()
    train_labels = list()
    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        rating = float(tweet['imdb_rating'])
        if rating < 1 or rating > 10:
            continue

        if item_id in clusters:
            cluster = clusters[item_id]
        else:
            cluster = 0

        num_engagements = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])

        num_engagements = int(num_engagements > 0)
        if num_engagements == 0:
            num_engagements = 2

        if item_id in items_stats and items_stats[item_id]['count'] > 0:
            lis = log(items_stats[item_id]['count'])
        else:
            lis = 0

        if item_id in tweets_with_engagement_sum:
            twe = log(tweets_with_engagement_sum[item_id])
        else:
            twe = 0

        train_features.append((
            rating * int(rating < 2),
            rating * int(rating > 6),
            rating * int(rating >= 2 and rating <= 6),
            twe - lis,
            int(tweet['tweet_is_retweet']),
            clusters_coeff_sorted[cluster] + 1,
            int(int(tweet['user_mentions_count']) > 0),
            int(tweet['tweet_id'] in has_retweets_train)
        ))
        train_labels.append(num_engagements)

    test_features = list()
    for tweet in test_dataset:
        item_id = tweet['imdb_item_id']
        rating = float(tweet['imdb_rating'])

        if item_id in clusters:
            cluster = clusters[item_id]
            cluster_id = clusters_coeff_sorted[cluster] + 1
        else:
            cluster_id = 0

        if item_id in items_stats and items_stats[item_id]['count'] > 0:
            lis = log(items_stats[item_id]['count'])
        else:
            lis = 0

        if item_id in tweets_with_engagement_sum:
            twe = log(tweets_with_engagement_sum[item_id])
        else:
            twe = 0

        test_features.append((
            rating * int(rating < 2),
            rating * int(rating > 6),
            rating * int(rating >= 2 and rating <= 6),
            twe - lis,
            int(tweet['tweet_is_retweet']),
            cluster_id,
            int(int(tweet['user_mentions_count']) > 0),
            int(tweet['tweet_id'] in has_retweets_test)
        ))
    return train_features, train_labels, test_features