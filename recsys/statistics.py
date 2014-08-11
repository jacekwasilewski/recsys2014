from scipy.cluster.vq import whiten
import item_clustering


def compute_statistics(dataset):
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
    cluster_user_eng = dict()
    tweets_with_engagement_count = dict()
    tweets_with_engagement_sum = dict()
    users_stats = dict()
    items_stats = dict()
    for tweet in dataset:
        user_id = tweet['user_id']
        users_stats[user_id] = dict()
        users_stats[user_id]['count'] = 0.0
        users_stats[user_id]['eng_count'] = 0.0
        cluster_user_eng[user_id] = dict()
        for i in range(k):
            cluster_user_eng[user_id][i] = dict()
            cluster_user_eng[user_id][i]['eng_sum'] = 0.0
            cluster_user_eng[user_id][i]['eng_count'] = 0.0

    for i in range(k):
        cluster_avg_engs[i] = dict()
        cluster_avg_engs[i]['eng_count'] = 0.0
        cluster_avg_engs[i]['eng_sum'] = 0.0
        cluster_avg_engs[i]['count'] = 0.0
        cluster_avg_engs[i]['item_count'] = 0.0

    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        if rating < 1:
            rating = 1

        cluster = clusters[item_id]
        cluster_avg_engs[cluster]['count'] += 1.0
        users_stats[user_id]['count'] += 1.0
        if int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count']) > 0:
            users_stats[user_id]['eng_count'] += 1.0
            if not tweet['tweet_is_retweet']:
                cluster_avg_engs[cluster]['eng_count'] += 1.0
                cluster_avg_engs[cluster]['eng_sum'] += int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
                cluster_user_eng[user_id][cluster]['eng_count'] += 1.0
                cluster_user_eng[user_id][cluster]['eng_sum'] += int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
            if item_id in tweets_with_engagement_count:
                tweets_with_engagement_count[item_id] += 1.0
                if not tweet['tweet_is_retweet']:
                    tweets_with_engagement_sum[item_id] += int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
                else:
                    tweets_with_engagement_sum[item_id] += 1.0
            else:
                tweets_with_engagement_count[item_id] = 1.0
                if not tweet['tweet_is_retweet']:
                    tweets_with_engagement_sum[item_id] = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
                else:
                    tweets_with_engagement_sum[item_id] = 1.0

        if item_id in items_stats:
            items_stats[item_id]['count'] += 1.0
            items_stats[item_id]['ratings_count'][rating] += 1.0
        else:
            items_stats[item_id] = dict()
            items_stats[item_id]['count'] = 1.0
            items_stats[item_id]['ratings_count'] = dict()
            for r in range(10):
                items_stats[item_id]['ratings_count'][r + 1] = 0.0
            items_stats[item_id]['ratings_count'][rating] = 1.0

    for item_id in clusters:
        cluster_avg_engs[clusters[item_id]]['item_count'] += 1.0

    print('Clustering item popularity...')
    items_count = list()
    items_count_labels = list()
    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        items_count.append(items_stats[item_id]['count'])
        items_count_labels.append(item_id)

    ip_whitened = whiten(items_count)
    ip_codebook = item_clustering.run_kmeans(ip_whitened, 5)
    ip_clusters = item_clustering.assign_clusters(ip_whitened, items_count_labels, ip_codebook)

    return {
        'codebook': codebook,
        'clusters': clusters,
        'ip_codebook': ip_codebook,
        'ip_clusters': ip_clusters,
        'cluster_avg_engs': cluster_avg_engs,
        'cluster_user_eng': cluster_user_eng,
        'tweets_with_engagement_count': tweets_with_engagement_count,
        'tweets_with_engagement_sum': tweets_with_engagement_sum,
        'users_stats': users_stats,
        'items_stats': items_stats,
        'tweets_per_day': []
    }


def compute_statistics_0(dataset):
    print('Calculating statistics...')
    cluster_user_eng = dict()
    tweets_with_engagement_count = dict()
    tweets_with_engagement_sum = dict()
    users_stats = dict()
    items_stats = dict()
    for tweet in dataset:
        user_id = tweet['user_id']
        users_stats[user_id] = dict()
        users_stats[user_id]['count'] = 0.0
        users_stats[user_id]['eng_count'] = 0.0
        cluster_user_eng[user_id] = dict()
        cluster_user_eng[user_id]['eng_sum'] = 0.0
        cluster_user_eng[user_id]['eng_count'] = 0.0

    cluster_avg_engs = dict()
    cluster_avg_engs['eng_count'] = 0.0
    cluster_avg_engs['eng_sum'] = 0.0
    cluster_avg_engs['count'] = 0.0
    cluster_avg_engs['item_count'] = 0.0

    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        if rating < 1:
            rating = 1

        cluster_avg_engs['count'] += 1.0
        users_stats[user_id]['count'] += 1.0
        if int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count']) > 0:
            users_stats[user_id]['eng_count'] += 1.0
            if not tweet['tweet_is_retweet']:
                cluster_avg_engs['eng_count'] += 1.0
                cluster_avg_engs['eng_sum'] += int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
                cluster_user_eng[user_id]['eng_count'] += 1.0
                cluster_user_eng[user_id]['eng_sum'] += int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
            if item_id in tweets_with_engagement_count:
                tweets_with_engagement_count[item_id] += 1.0
                if not tweet['tweet_is_retweet']:
                    tweets_with_engagement_sum[item_id] += int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
                else:
                    tweets_with_engagement_sum[item_id] += 1.0
            else:
                tweets_with_engagement_count[item_id] = 1.0
                if not tweet['tweet_is_retweet']:
                    tweets_with_engagement_sum[item_id] = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
                else:
                    tweets_with_engagement_sum[item_id] = 1.0

        if item_id in items_stats:
            items_stats[item_id]['count'] += 1.0
            items_stats[item_id]['ratings_count'][rating] += 1.0
        else:
            items_stats[item_id] = dict()
            items_stats[item_id]['count'] = 1.0
            items_stats[item_id]['ratings_count'] = dict()
            for r in range(10):
                items_stats[item_id]['ratings_count'][r + 1] = 0.0
            items_stats[item_id]['ratings_count'][rating] = 1.0

    print('Clustering item popularity...')
    items_count = list()
    items_count_labels = list()
    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        items_count.append(items_stats[item_id]['count'])
        items_count_labels.append(item_id)

    ip_whitened = whiten(items_count)
    ip_codebook = item_clustering.run_kmeans(ip_whitened, 5)
    ip_clusters = item_clustering.assign_clusters(ip_whitened, items_count_labels, ip_codebook)

    items_mean_engagement = dict()
    for item_id in tweets_with_engagement_count:
        if tweets_with_engagement_count[item_id] > 0:
            items_mean_engagement[item_id] = tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id]

    return {
        'cluster_avg_engs': cluster_avg_engs,
        'cluster_user_eng': cluster_user_eng,
        'tweets_with_engagement_count': tweets_with_engagement_count,
        'tweets_with_engagement_sum': tweets_with_engagement_sum,
        'users_stats': users_stats,
        'items_stats': items_stats,
        'items_mean_engagement': items_mean_engagement,
        'ip_clusters': ip_clusters,
    }