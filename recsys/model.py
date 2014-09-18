from math import log
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import solution
import numpy as np


def run_model(test, statistics, model_parameters, is_debug=False):
    items_mean_engagement = statistics['items_mean_engagement']
    clusters_mean_engagement = statistics['clusters_mean_engagement']
    users_clusters_mean_engagement = statistics['users_clusters_mean_engagement']
    item_engagement_probability = statistics['item_engagement_probability']
    user_cluster_engagement_probability = statistics['user_cluster_engagement_probability']
    user_engagement_probability = statistics['user_engagement_probability']
    cluster_engagement_probability = statistics['cluster_engagement_probability']

    cluster_mean_engagement = None
    users_mean_engagement = dict()
    cep = None
    users_cluster_engagement_probability = dict()
    if model_parameters[0] in clusters_mean_engagement:
        cluster_mean_engagement = clusters_mean_engagement[model_parameters[0]]
    if model_parameters[0] in users_clusters_mean_engagement:
        users_mean_engagement = users_clusters_mean_engagement[model_parameters[0]]
    if model_parameters[0] in user_cluster_engagement_probability:
        users_cluster_engagement_probability = user_cluster_engagement_probability[model_parameters[0]]
    if model_parameters[0] in cluster_engagement_probability:
        cep = cluster_engagement_probability[model_parameters[0]]

    solutions = list()
    debug = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(tweet['user_mentions_count'] > 0)
        user_mentions1 = int(tweet['user_mentions_count'] > 1)

        iep = 0.0
        uep = 0.0
        ucep = 0.0
        if item_id in item_engagement_probability:
            iep = item_engagement_probability[item_id]
        if user_id in user_engagement_probability:
            uep = user_engagement_probability[user_id]
        if cep is None:
            cep = 0.0
        if user_id in users_cluster_engagement_probability:
            ucep = users_cluster_engagement_probability[user_id]

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
                model_parameters[0],
                item_id,
                tweet['tweet_id'],
                user_id,
                log_cluster_mean_engagement,
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
                item_had_engagement,
                user_had_engagement,
                rating,
                iep,
                uep,
                cep,
                ucep,
                tweet['user_mentions_count'],
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
                          0.001]  # free variable
    model_parameters_2 = [2,  # cluster
                          1.6,  # log_cluster_mean_engagement
                          [1.0, 0.0, 0.0102, 0.0204, 0.0306, 0.0408, 0.6938, 0.7959, 0.8979, 1.0],
                          0.0,  # item_had_engagement
                          0.1,  # log_item_mean_engagement
                          0.0,  # user_had_engagement
                          0.1,  # log_user_mean_engagement
                          1.0,  # user_mentions0
                          0.0833,  # user_mentions1
                          1.0,  # tweet_is_retweet
                          0.0]  # free variable
    model_parameters_new = [None,  # cluster
                            0.0,  # log_cluster_mean_engagement
                            [1.5, 0.0, 0.0153, 0.0306, 0.0459, 0.0612, 1.0407, 1.19385, 1.41, 1.5],
                            0.0,  # item_had_engagement
                            0.0,  # log_item_mean_engagement
                            0.0,  # user_had_engagement
                            0.0,  # log_user_mean_engagement
                            1.0,  # user_mentions0
                            0.0833,  # user_mentions1
                            1.0,  # tweet_is_retweet
                            0.0]  # free variable
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
        debug0 = list()
        debug1 = list()
        debug2 = list()
        debugnew = list()
        for d in debug_0:
            debug.append(d)
            debug0.append(d)
        for d in debug_1:
            debug.append(d)
            debug1.append(d)
        for d in debug_2:
            debug.append(d)
            debug2.append(d)
        for d in debug_new:
            debug.append(d)
            debugnew.append(d)
        solution.write_debug(debug, '/Users/jwasilewski/RecSys2014/debug.csv')
        solution.write_debug(debug0, '/Users/jwasilewski/RecSys2014/debug0.csv')
        solution.write_debug(debug1, '/Users/jwasilewski/RecSys2014/debug1.csv')
        solution.write_debug(debug2, '/Users/jwasilewski/RecSys2014/debug2.csv')
        solution.write_debug(debugnew, '/Users/jwasilewski/RecSys2014/debugnew.csv')

    sol = solution.sort_the_solution(sol)
    solution.write_the_solution_file(sol, '/Users/jwasilewski/RecSys2014/solution.dat')


def run_model_mentions(test):
    solutions = list()
    for tweet in test:
        user_id = tweet['user_id']
        user_mentions = int(tweet['user_mentions_count'] > 0)

        engagement = user_mentions

        solutions.append((user_id, tweet['tweet_id'], engagement))

    return solutions


def learn_model(train):
    features = list()
    labels = list()
    for tweet in train:
        rating = tweet['imdb_rating']

        rating_low = 0
        rating_medium = 0
        rating_high = 0
        if rating < 2:
            rating_low = 1
        elif rating > 6:
            rating_high = 1
        else:
            rating_medium = 1

        engagement = tweet['tweet_favourite_count'] + tweet['tweet_retweet_count']

        features.append((rating_low, rating_medium, rating_high))
        labels.append(engagement)
    features = np.array(features)
    labels = np.array(labels)
    labels = (labels > 0).astype(np.int)
    X = StandardScaler().fit_transform(features)
    y = np.ravel(labels)
    model = LogisticRegression()
    model = model.fit(X, y)
    return model


def apply_model(test, model):
    """

    :param test:
    :param LogisticRegression model: Model
    :return:
    """
    features = list()
    for tweet in test:
        rating = tweet['imdb_rating']

        rating_low = 0
        rating_medium = 0
        rating_high = 0
        if rating < 2:
            rating_low = 1
        elif rating > 6:
            rating_high = 1
        else:
            rating_medium = 1

        features.append((rating_low, rating_medium, rating_high))
    features = np.array(features)
    X = StandardScaler().fit_transform(features)
    predictions = model.predict(X)
    return predictions