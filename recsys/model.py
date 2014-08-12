from math import log
import solution


def run_model(test, statistics, model_parameters, is_debug=False):
    items_mean_engagement = statistics['items_mean_engagement']
    clusters_mean_engagement = statistics['clusters_mean_engagement']
    users_clusters_mean_engagement = statistics['users_clusters_mean_engagement']

    cluster_mean_engagement = None
    users_mean_engagement = dict()
    if model_parameters[0] in clusters_mean_engagement:
        cluster_mean_engagement = clusters_mean_engagement[model_parameters[0]]
    if model_parameters[0] in users_clusters_mean_engagement:
        users_mean_engagement = users_clusters_mean_engagement[model_parameters[0]]

    solutions = list()
    debug = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(tweet['user_mentions_count'] > 0)
        user_mentions1 = int(tweet['user_mentions_count'] > 1)

        rating_1 = 0
        rating_2 = 0
        rating_3 = 0
        rating_4 = 0
        rating_5 = 0
        rating_6 = 0
        rating_7 = 0
        rating_8 = 0
        rating_9 = 0
        rating_10 = 0
        if rating == 1:
            rating_1 = 1
        elif rating == 2:
            rating_2 = 1
        elif rating == 3:
            rating_3 = 1
        elif rating == 4:
            rating_4 = 1
        elif rating == 5:
            rating_5 = 1
        elif rating == 6:
            rating_6 = 1
        elif rating == 7:
            rating_7 = 1
        elif rating == 8:
            rating_8 = 1
        elif rating == 9:
            rating_9 = 1
        elif rating == 10:
            rating_10 = 1

        item_score = model_parameters[2][rating - 1]

        item_had_engagement = int(item_id in items_mean_engagement)
        user_had_engagement = int(user_id in users_mean_engagement)

        log_cluster_mean_engagement = 0.0
        log_item_mean_engagement = 0.0
        log_user_mean_engagement = 0.0

        if cluster_mean_engagement:
            log_cluster_mean_engagement = log(cluster_mean_engagement)
        if item_had_engagement:
            log_item_mean_engagement = log(items_mean_engagement[item_id])
        if user_had_engagement:
            log_user_mean_engagement = log(users_mean_engagement[user_id])

        engagement = model_parameters[10]
        engagement += model_parameters[1] * log_cluster_mean_engagement
        engagement += item_score
        engagement += model_parameters[3] * item_had_engagement
        engagement += model_parameters[4] * log_item_mean_engagement
        engagement += model_parameters[5] * user_had_engagement
        engagement += model_parameters[6] * log_user_mean_engagement
        engagement += model_parameters[7] * user_mentions0
        engagement += model_parameters[8] * user_mentions1
        engagement += model_parameters[9] * tweet_is_retweet

        solutions.append((user_id, tweet['tweet_id'], engagement))
        if is_debug:
            debug.append((
                item_id,
                tweet['tweet_id'],
                user_id,
                log(cluster_mean_engagement),
                rating_1,
                rating_2,
                rating_3,
                rating_4,
                rating_5,
                rating_6,
                rating_7,
                rating_8,
                rating_9,
                rating_10,
                log_item_mean_engagement,
                log_user_mean_engagement,
                tweet_is_retweet,
                user_mentions0,
                user_mentions1,
                str((tweet['tweet_engagement'] > 0))
            ))
    return solutions, debug


def run_model_clustered(test, statistics, is_debug=False):
    clusters = statistics['clusters']
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

    model_parameters_0 = [0,  # cluster
                          1.0,  # log_cluster_mean_engagement
                          [0.98769, 0.0, 0.01122, 0.01122, 0.03366, 0.04488, 0.76318, 0.836, 0.99, 1.1],
                          0.1,  # item_had_engagement
                          0.5,  # log_item_mean_engagement
                          0.0,  # user_had_engagement
                          0.0,  # log_user_mean_engagement
                          1.0,  # user_mentions0
                          0.0833,  # user_mentions1
                          1.0,  # tweet_is_retweet
                          0.0]  # free variable
    model_parameters_1 = [1,  # cluster
                          0.9,  # log_cluster_mean_engagement
                          [0.9387, 0.8, 0.0102, 0.0204, 0.0306, 0.0408, 0.67, 0.79, 0.88, 1.0],
                          0.2,  # item_had_engagement
                          0.1,  # log_item_mean_engagement
                          0.0,  # user_had_engagement
                          0.2,  # log_user_mean_engagement
                          1.0,  # user_mentions0
                          0.0833,  # user_mentions1
                          1.0,  # tweet_is_retweet
                          0.0]  # free variable
    model_parameters_2 = [2,
                          1.6,
                          [1.0, 0.0, 0.0102, 0.0204, 0.0306, 0.0408, 0.6938, 0.7959, 0.8979, 1.0],
                          0.0,
                          0.1,
                          0.0,
                          0.1,
                          1.0,
                          0.0833,
                          1.0,
                          0.0]
    model_parameters_new = [None,
                            0.0,
                            [1.5, 0.0, 0.0153, 0.0306, 0.0459, 0.0612, 1.0407, 1.19385, 1.41, 1.5],
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.0,
                            0.0833,
                            1.0,
                            0.0]
    solutions_0, debug_0 = run_model(tweets_0, statistics, model_parameters_0, is_debug)
    solutions_1, debug_1 = run_model(tweets_1, statistics, model_parameters_1, is_debug)
    solutions_2, debug_2 = run_model(tweets_2, statistics, model_parameters_2, is_debug)
    solutions_new, debug_new = run_model(tweets_new, statistics, model_parameters_new, is_debug)

    sol = list()
    for (user_id, tweet_id, engagement) in solutions_0:
        sol.append((user_id, tweet_id, engagement))
    for (user_id, tweet_id, engagement) in solutions_1:
        sol.append((user_id, tweet_id, engagement))
    for (user_id, tweet_id, engagement) in solutions_2:
        sol.append((user_id, tweet_id, engagement))
    for (user_id, tweet_id, engagement) in solutions_new:
        sol.append((user_id, tweet_id, engagement))

    if is_debug:
        debug = list()
        for d in debug_0:
            debug.append(d)
        for d in debug_1:
            debug.append(d)
        for d in debug_2:
            debug.append(d)
        for d in debug_new:
            debug.append(d)
        solution.write_debug(debug, '/Users/jwasilewski/RecSys2014/debug.csv')

    sol = solution.sort_the_solution(sol)
    solution.write_the_solution_file(sol, '/Users/jwasilewski/RecSys2014/solution.dat')