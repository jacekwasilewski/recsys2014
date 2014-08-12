from math import log
import solution


def run_model_0(test, model_parameters):
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    cluster_user_eng = model_parameters['cluster_user_eng']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']

    solutions = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        user_mentions_count = tweet['user_mentions_count']
        cluster_mean_engagement = cluster_avg_engs[0]['eng_sum'] / cluster_avg_engs[0]['eng_count']

        item_score = 0.0
        engagement_coefficient = 0.0
        cluster_coefficient = 0.0

        cluster_base = 0.0 + 1.0 * log(cluster_mean_engagement)

        if rating == 1:
            item_score = 0.8979
        elif rating == 2:
            item_score = 0.0
        elif rating == 3:
            item_score = 0.0102
        elif rating == 4:
            item_score = 0.0204
        elif rating == 5:
            item_score = 0.0306
        elif rating == 6:
            item_score = 0.0408
        elif rating == 7:
            item_score = 0.6938
        elif rating == 8:
            item_score = 0.76
        elif rating == 9:
            item_score = 0.9
        elif rating == 10:
            item_score = 1.0

        if item_id in tweets_with_engagement_count:
            engagement_coefficient = 0.1 + 0.5 * log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])

        if user_id in cluster_user_eng and cluster_user_eng[user_id][0]['eng_count'] > 0:
            cluster_coefficient = 0.0 + 0.0 * log(cluster_user_eng[user_id][0]['eng_sum'] / cluster_user_eng[user_id][0]['eng_count'])

        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 1.0 * cluster_base
        engagement += 1.0 * cluster_coefficient
        engagement += 1.0 * engagement_coefficient
        engagement += 1.1 * item_score
        engagement += 1.0 * user_mentions0
        engagement += 1.0/12 * user_mentions1
        engagement += 1.0 * tweet_is_retweet

        solutions.append((user_id, tweet['tweet_id'], engagement))
    return solutions


def run_model_1(test, model_parameters):
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    cluster_user_eng = model_parameters['cluster_user_eng']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']

    solutions = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        user_mentions_count = tweet['user_mentions_count']
        cluster_mean_engagement = cluster_avg_engs[1]['eng_sum'] / cluster_avg_engs[1]['eng_count']

        item_score = 0.0
        engagement_coefficient = 0.0
        cluster_coefficient = 0.0

        cluster_base = 0.0 + 1.0 * log(cluster_mean_engagement)

        if rating == 1:
            item_score = 0.9387
        elif rating == 2:
            item_score = 0.8
        elif rating == 3:
            item_score = 0.0102
        elif rating == 4:
            item_score = 0.0204
        elif rating == 5:
            item_score = 0.0306
        elif rating == 6:
            item_score = 0.0408
        elif rating == 7:
            item_score = 0.67
        elif rating == 8:
            item_score = 0.79
        elif rating == 9:
            item_score = 0.88
        elif rating == 10:
            item_score = 1.0

        if item_id in tweets_with_engagement_count:
            engagement_coefficient = 0.2 + 0.1 * log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])

        if user_id in cluster_user_eng and cluster_user_eng[user_id][1]['eng_count'] > 0:
            cluster_coefficient = 0.0 + 0.2 * log(cluster_user_eng[user_id][1]['eng_sum'] / cluster_user_eng[user_id][1]['eng_count'])

        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 0.9 * cluster_base
        engagement += 1.0 * cluster_coefficient
        engagement += 1.0 * engagement_coefficient
        engagement += 1.0 * item_score
        engagement += 1.0 * user_mentions0
        engagement += 1.0/12 * user_mentions1
        engagement += 1.0 * tweet_is_retweet

        solutions.append((user_id, tweet['tweet_id'], engagement))

    return solutions


def run_model_2(test, model_parameters):
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    cluster_user_eng = model_parameters['cluster_user_eng']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']

    solutions = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        user_mentions_count = tweet['user_mentions_count']
        cluster_mean_engagement = cluster_avg_engs[2]['eng_sum'] / cluster_avg_engs[2]['eng_count']

        item_score = 0.0
        engagement_coefficient = 0.0
        cluster_coefficient = 0.0

        cluster_base = 0.0 + 1.0 * log(cluster_mean_engagement)

        if rating == 1:
            item_score = 1.0
        elif rating == 2:
            item_score = 0.0
        elif rating == 3:
            item_score = 0.0102
        elif rating == 4:
            item_score = 0.0204
        elif rating == 5:
            item_score = 0.0306
        elif rating == 6:
            item_score = 0.0408
        elif rating == 7:
            item_score = 0.6938
        elif rating == 8:
            item_score = 0.7959
        elif rating == 9:
            item_score = 0.8979
        elif rating == 10:
            item_score = 1.0

        if item_id in tweets_with_engagement_count:
            engagement_coefficient = 0.0 + 0.1 * log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])

        if user_id in cluster_user_eng and cluster_user_eng[user_id][2]['eng_count'] > 0:
            cluster_coefficient = 0.0 + 0.1 * log(cluster_user_eng[user_id][2]['eng_sum'] / cluster_user_eng[user_id][2]['eng_count'])

        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 1.6 * cluster_base
        engagement += 1.0 * cluster_coefficient
        engagement += 1.0 * engagement_coefficient
        engagement += 1.0 * item_score
        engagement += 1.0 * user_mentions0
        engagement += 1.0/12 * user_mentions1
        engagement += 1.0 * tweet_is_retweet

        solutions.append((user_id, tweet['tweet_id'], engagement))
    return solutions


def run_model_new(test):
    solutions = list()
    for tweet in test:
        rating = tweet['imdb_rating']
        user_mentions_count = tweet['user_mentions_count']

        item_score = 0.0
        if rating == 1:
            item_score = 1.0
        elif rating == 2:
            item_score = 0.0
        elif rating == 3:
            item_score = 0.0102
        elif rating == 4:
            item_score = 0.0204
        elif rating == 5:
            item_score = 0.0306
        elif rating == 6:
            item_score = 0.0408
        elif rating == 7:
            item_score = 0.6938
        elif rating == 8:
            item_score = 0.7959
        elif rating == 9:
            item_score = 0.94
        elif rating == 10:
            item_score = 1.0

        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 1.5 * item_score
        engagement += 1.0 * user_mentions0
        engagement += 1.0/12 * user_mentions1
        engagement += 1.0 * tweet_is_retweet

        solutions.append((tweet['user_id'], tweet['tweet_id'], engagement))
    return solutions


def run_model_clustered(test, model_parameters_all):
    clusters = model_parameters_all['clusters']
    tweets_0 = list()
    tweets_1 = list()
    tweets_2 = list()
    tweets_new = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        if item_id in clusters:
            cluster = clusters[item_id]
            if cluster == 0:
                tweets_0.append(tweet)
            elif cluster == 1:
                tweets_1.append(tweet)
            elif cluster == 2:
                tweets_2.append(tweet)
        else:
            tweets_new.append(tweet)

    solutions_0 = run_model_0(tweets_0, model_parameters_all)
    solutions_1 = run_model_1(tweets_1, model_parameters_all)
    solutions_2 = run_model_2(tweets_2, model_parameters_all)
    solutions_new = run_model_new(tweets_new)

    sol = list()
    for (user_id, tweet_id, engagement) in solutions_0:
        sol.append((user_id, tweet_id, engagement))
    for (user_id, tweet_id, engagement) in solutions_1:
        sol.append((user_id, tweet_id, engagement))
    for (user_id, tweet_id, engagement) in solutions_2:
        sol.append((user_id, tweet_id, engagement))
    for (user_id, tweet_id, engagement) in solutions_new:
        sol.append((user_id, tweet_id, engagement))
    sol = solution.sort_the_solution(sol)
    solution.write_the_solution_file(sol, '/Users/jwasilewski/RecSys2014/solution.dat')