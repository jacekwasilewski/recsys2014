from datetime import datetime
from math import log
from scipy.cluster.vq import whiten
import item_clustering
import solution


def run_model(dataset, model_parameters):
    codebook = model_parameters['codebook']
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']
    cluster_user_eng = model_parameters['cluster_user_eng']

    ffts_test, ffts_test_labels = item_clustering.compute_fft(dataset)
    whitened_test = whiten(ffts_test)
    clusters_test = item_clustering.assign_clusters(whitened_test, ffts_test_labels, codebook)

    print('Applying model...')
    solutions = list()
    solutions_debug = list()
    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])

        user_followers_count = int(tweet['user_followers_count'])
        user_statuses_count = int(tweet['user_statuses_count'])

        scraping_date = datetime.fromtimestamp(int(tweet['tweet_scraping_time']))
        tweet_date = datetime.strptime(tweet['tweet_created_at'], '%Y-%m-%d')
        user_date = datetime.strptime(tweet['user_created_at'], '%Y-%m-%d')
        user_age = (scraping_date - user_date).days
        tweet_age = (scraping_date - tweet_date).days
        relative_tweet_age = (tweet_date - user_date).days

        cluster = clusters_test[item_id]

        # ------------------
        # 0.8184845269398118
        # if rating > 6:
        #     engagement = 2 * rating
        # elif rating < 2:
        #     engagement = 6 * rating
        # else:
        #     engagement = 2 * ceil(rating / 2)
        # ------------------

        # ------------------
        # 0.821692078312203
        # if clusters_test[item_id] == 0:
        #     base = 100
        # elif clusters_test[item_id] == 1:
        #     base = 10
        # else:
        #     base = 1
        #
        # if rating > 6:
        #     engagement = base + 100 * rating
        # elif rating < 2:
        #     engagement = base + 10 * rating
        # else:
        #     engagement = base + 1 * rating
        # ------------------

        # ------------------
        # 0.8370632566756109
        # if cluster == 0:
        #     base = 20
        # elif cluster == 1:
        #     base = 5
        # else:
        #     base = 4
        #
        # if rating > 6:
        #     rating_base = 50 * rating
        # elif rating < 2:
        #     rating_base = 490 * rating
        # else:
        #     rating_base = 5 * rating
        #
        # if tweet['tweet_is_retweet']:
        #     base = 500
        #     rating_base = 500
        #
        # if item_id in tweets_with_engagement_count:
        #     engagement_coefficient = 1.05 + 0.26 * log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])
        # else:
        #     engagement_coefficient = 1.0
        #
        # engagement = (base + rating_base) * engagement_coefficient
        #
        # if tweet_age > 22:
        #     engagement = 0
        #
        # if user_followers_count < 10:
        #     engagement = 0
        #
        # if user_statuses_count < 40:
        #     engagement = 0
        # ------------------

        # ------------------
        # 0.8176913563666429

        # if clusters_test[item_id] == 0:
        #     base = 10
        #     multiplier = 1.07
        # elif clusters_test[item_id] == 1:
        #     base = 60
        #     multiplier = 1.31
        # else:
        #     base = 1
        #     multiplier = 1.04
        #
        # if rating > 6:
        #     engagement = base + 10 * rating  # * multiplier
        # elif rating < 2:
        #     engagement = base + 60 * rating  # * multiplier
        # else:
        #     engagement = base + 1 * rating  # * multiplier

        # if clusters_test[item_id] == 0:
        #     engagement *= 0.06714759
        # elif clusters_test[item_id] == 1:
        #     engagement *= 0.3096683
        # else:
        #     engagement *= 0.03994073
        # ------------------
        # 0.8378181152694995
        if cluster == 0:
            base = 7
        elif cluster == 1:
            base = 5
        else:
            base = 4

        cluster_base = 1.0 + 0.99 * log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])

        if tweet['tweet_is_retweet']:
            rating = 10
            cluster_base = 2.0

        if rating > 6:
            item_rating = 50 * rating
        elif rating < 2:
            item_rating = 490 * rating
        else:
            item_rating = 5 * rating

        if item_id in tweets_with_engagement_count:
            engagement_coefficient = 1.1 + 0.26 * log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])
        else:
            engagement_coefficient = 1.0

        if user_id in cluster_user_eng and cluster_user_eng[user_id][cluster]['eng_count'] > 0:
            cluster_coefficient = 1.031 + 0.26 * log(cluster_user_eng[user_id][cluster]['eng_sum'] / cluster_user_eng[user_id][cluster]['eng_count'])
        else:
            cluster_coefficient = 1.0

        engagement = base + item_rating * engagement_coefficient * cluster_base * cluster_coefficient

        if tweet_age > 22:
            engagement = 0.0

        if user_followers_count < 10:
            engagement = 0.0

        if user_statuses_count < 40:
            engagement = 0.0

        engagement = round(engagement)

        if engagement <= 40:
            engagement = 0.0

        # wyliczyc ile top tweetow moglo miec engagement - reszte wyzerowac

        # ------------------
        solutions.append((user_id, tweet['tweet_id'], engagement))
        solutions_debug.append((user_id, tweet['tweet_id'], engagement, cluster_base, item_rating, engagement_coefficient, cluster_coefficient))

    print('Sorting solution...')
    solutions = solution.sort_the_solution(solutions)
    solutions_debug = solution.sort_the_solution(solutions_debug)
    print('Saving solution...')
    solution.write_the_solution_file(solutions, '/Users/jwasilewski/RecSys2014/solution.dat')
    solution.write_the_solution_file_debug(solutions_debug, '/Users/jwasilewski/RecSys2014/solution_debug.dat')
    print('done.')