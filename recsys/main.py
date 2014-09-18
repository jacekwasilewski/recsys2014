from math import log

from scipy.cluster.vq import whiten

import dataset
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

    lines = list()
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

        lines.append("%s %s %s %s %s %s %s\n"
                     % (items_stats[item_id]['count'],
                        tweets_with_engagement_sum[item_id],
                        rating,
                        int(tweet['tweet_is_retweet']),
                        float(log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])),
                        int(tweet['user_mentions_count']),
                        num_engagements))
        train_features.append((rating * int(rating < 2),
                               rating * int(rating > 6),
                               rating * int(rating >= 2 and rating <= 6),
                               -log(items_stats[item_id]['count']) + log(tweets_with_engagement_sum[item_id]),
                               int(tweet['tweet_is_retweet']),
                               float(
                                   log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])),
                               int(tweet['user_mentions_count'])))
        train_labels.append(num_engagements)

    with file('lr.out', 'w') as outfile:
        outfile.writelines(lines)

    print('And here ...')
    lines = list()
    test_features = list()
    for tweet in test_dataset:
        item_id = tweet['imdb_item_id']
        rating = float(tweet['imdb_rating'])

        if item_id in clusters:
            cluster = clusters[item_id]
        else:
            cluster = 0

        num_engagements = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])

        if item_id in items_stats:
            lines.append("%s %s %s %s %s %s %s\n"
                         % (items_stats[item_id]['count'],
                            tweets_with_engagement_sum[item_id],
                            rating,
                            int(tweet['tweet_is_retweet']),
                            float(log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])),
                            int(tweet['user_mentions_count']),
                            num_engagements))
            test_features.append((items_stats[item_id]['count'],
                                  tweets_with_engagement_sum[item_id],
                                  rating,
                                  int(tweet['tweet_is_retweet']),
                                  float(log(
                                      cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])),
                                  int(tweet['user_mentions_count']),
                                  num_engagements))
        else:
            lines.append("%s %s %s %s %s %s %s\n"
                         % (0,
                            0,
                            rating,
                            int(tweet['tweet_is_retweet']),
                            0,
                            int(tweet['user_mentions_count']),
                            num_engagements))
            test_features.append((0,
                                  0,
                                  rating,
                                  int(tweet['tweet_is_retweet']),
                                  0,
                                  int(tweet['user_mentions_count']),
                                  num_engagements))

    with file('lrtest.out', 'w') as outfile:
        outfile.writelines(lines)
    return train_features, train_labels, test_features


if __name__ == "__main__":
    print('Loading datasets...')
    tweets_train, tweets_test = dataset.read_datasets()
    train_features, train_labels, test_features = compute_features(tweets_train, tweets_test)
    # lrmodel = model.learn_model(tweets_train)
    # predictions = model.apply_model(tweets_test, lrmodel)
    # solution.prepare_solutions(tweets_test, predictions)
    # model_parameters = statistics.compute_statistics(tweets_train)

    # solutions = model.run_model_article(tweets_test, list())