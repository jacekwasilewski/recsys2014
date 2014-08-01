from datetime import datetime
from math import log
from scipy.cluster.vq import whiten
import item_clustering
import solution
import subprocess


def run_model(tweets_train, tweets_test):
    tweets_train_per_day = item_clustering.compute_occurrences(tweets_train)
    tweets_test_per_day = item_clustering.compute_occurrences(tweets_test)

    # calculating FFT
    ffts, ffts_labels = item_clustering.compute_fft(tweets_train_per_day)
    ffts_test, ffts_test_labels = item_clustering.compute_fft(tweets_test_per_day)

    # running k-means
    k = 3
    whitened = whiten(ffts)
    codebook = item_clustering.run_kmeans(whitened, k)
    clusters = item_clustering.assign_clusters(whitened, ffts_labels, codebook)
    whitened_test = whiten(ffts_test)
    clusters_test = item_clustering.assign_clusters(whitened_test, ffts_test_labels, codebook)

    cluster_avg_engs = dict()
    cluster_user_eng = dict()
    tweets_with_engagement_count = dict()
    tweets_with_engagement_sum = dict()
    user_had_engagement = dict()
    for tweet in tweets_train:
        user_id = tweet['user_id']
        user_had_engagement[user_id] = 0
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

    for tweet in tweets_train:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        cluster = clusters[item_id]
        cluster_avg_engs[cluster]['count'] += 1.0
        if int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count']) > 0:
            user_had_engagement[user_id] = 1.0
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

    for item_id in clusters:
        cluster_avg_engs[clusters[item_id]]['item_count'] += 1.0

    # for i in range(k):
    #     print(str(cluster_avg_engs[i]['eng_sum']) + " " + str(cluster_avg_engs[i]['eng_count']) + " " + str(cluster_avg_engs[i]['count']) + " " + str(cluster_avg_engs[i]['item_count']))

    solutions = list()
    for tweet in tweets_test:
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
        # if clusters_test[item_id] == 0:
        #     base = 20
        # elif clusters_test[item_id] == 1:
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
        # if item_id in tweets_with_engagement_count:
        #     engagement_coefficient = 1.05 + 0.26 * log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])
        # else:
        #     engagement_coefficient = 1.0
        #
        # if tweet['tweet_is_retweet']:
        #     base = 500
        #     rating_base = 500
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
        # 0.8376633688877837
        cluster = clusters_test[item_id]

        if clusters_test[item_id] == 0:
            base = 7
        elif clusters_test[item_id] == 1:
            base = 5
        else:
            base = 4

        cluster_base = 1.0 + log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])

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

        engagement = base + item_rating * cluster_coefficient * engagement_coefficient * cluster_base

        if tweet_age > 22:
            engagement = 0.0

        if user_followers_count < 10:
            engagement = 0.0

        if user_statuses_count < 40:
            engagement = 0.0

        # wyliczyc ile top tweetow moglo miec engagement - reszte wyzerowac

        # ------------------
        solutions.append((user_id, tweet['tweet_id'], engagement))
        # solutions.append((user_id, tweet['tweet_id'], engagement, cluster_base, item_rating, engagement_coefficient, cluster_coefficient))

    solutions = solution.sort_the_solution(solutions)
    solution.write_the_solution_file(solutions, '/Users/jwasilewski/RecSys2014/solution.dat')
    print('done.')

    p = subprocess.Popen('java -jar /Users/jwasilewski/RecSys2014/rscevaluator-0.14-jar-with-dependencies.jar /Users/jwasilewski/RecSys2014/test_solution.dat /Users/jwasilewski/RecSys2014/solution.dat', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line)
    p.wait()