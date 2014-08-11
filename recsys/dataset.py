from dateutil import parser
import json


def read_train_dataset(the_dataset_file, limit=False):
    tweets = list()
    header = True
    i = 1
    with file(the_dataset_file, 'r') as infile:
        for line in infile:
            if header:
                header = False
                continue
            if i == limit:
                break
            line_array = line.strip().split(',')
            user_id = line_array[0]
            item_id = line_array[1]
            rating = max(min(int(line_array[2]), 10), 0)
            scraping_time = line_array[3]
            tweet = ','.join(line_array[4:])
            json_obj = json.loads(tweet)
            tweet_created_at = json_obj['created_at']
            user_created_at = json_obj['user']['created_at']
            tweet_created_at_date = parser.parse(tweet_created_at).strftime('%Y-%m-%d')  # strftime('%Y-%m-%d %H:%M:%S')
            user_created_at_date = parser.parse(user_created_at).strftime('%Y-%m-%d')  # strftime('%Y-%m-%d %H:%M:%S')
            is_retweet = 'retweeted_status' in json_obj
            retweet_of = None
            if is_retweet:
                # continue
                retweet_of = json_obj['retweeted_status']['id']
            entities = json_obj['entities']
            hashtags_count = len(entities['hashtags'])
            symbols_count = len(entities['symbols'])
            urls_count = len(entities['urls'])
            user_mentions_count = len(entities['user_mentions'])
            tweets.append({
                'imdb_item_id': item_id,
                'imdb_rating': rating,
                'tweet_id': json_obj['id'],
                'tweet_favourite_count': json_obj['favorite_count'],
                'tweet_retweet_count': json_obj['retweet_count'],
                'tweet_engagement': json_obj['favorite_count'] + json_obj['retweet_count'],
                'tweet_created_at': tweet_created_at_date,
                'tweet_scraping_time': scraping_time,
                'tweet_is_retweet': is_retweet,
                'tweet_retweet_of': retweet_of,
                'user_id': user_id,
                'user_favourites_count': json_obj['user']['favourites_count'],
                'user_followers_count': json_obj['user']['followers_count'],
                'user_friends_count': json_obj['user']['friends_count'],
                'user_listed_count': json_obj['user']['listed_count'],
                'user_statuses_count': json_obj['user']['statuses_count'],
                'user_created_at': user_created_at_date,
                'hashtags_count': hashtags_count,
                'symbols_count': symbols_count,
                'urls_count': urls_count,
                'user_mentions_count': user_mentions_count
            })
            if i % 100 == 0:
                print("Read entries %s..." % i)
            i += 1
    return tweets


def read_test_dataset(the_dataset_file, limit=False):
    tweets = list()
    header = True
    i = 1
    with file(the_dataset_file, 'r') as infile:
        for line in infile:
            if header:
                header = False
                continue
            if i == limit:
                break
            line_array = line.strip().split(',')
            user_id = line_array[0]
            item_id = line_array[1]
            rating = max(min(int(line_array[2]), 10), 0)
            scraping_time = line_array[3]
            tweet = ','.join(line_array[4:])
            json_obj = json.loads(tweet)
            tweet_created_at = json_obj['created_at']
            user_created_at = json_obj['user']['created_at']
            tweet_created_at_date = parser.parse(tweet_created_at).strftime('%Y-%m-%d')
            user_created_at_date = parser.parse(user_created_at).strftime('%Y-%m-%d')
            is_retweet = 'retweeted_status' in json_obj
            retweet_of = None
            if is_retweet:
                retweet_of = json_obj['retweeted_status']['id']
            entities = json_obj['entities']
            hashtags_count = len(entities['hashtags'])
            symbols_count = len(entities['symbols'])
            urls_count = len(entities['urls'])
            user_mentions_count = len(entities['user_mentions'])
            tweets.append({
                'imdb_item_id': item_id,
                'imdb_rating': rating,
                'tweet_id': json_obj['id'],
                'tweet_created_at': tweet_created_at_date,
                'tweet_scraping_time': scraping_time,
                'tweet_is_retweet': is_retweet,
                'tweet_retweet_of': retweet_of,
                'user_id': user_id,
                'user_favourites_count': json_obj['user']['favourites_count'],
                'user_followers_count': json_obj['user']['followers_count'],
                'user_friends_count': json_obj['user']['friends_count'],
                'user_listed_count': json_obj['user']['listed_count'],
                'user_statuses_count': json_obj['user']['statuses_count'],
                'user_created_at': user_created_at_date,
                'hashtags_count': hashtags_count,
                'symbols_count': symbols_count,
                'urls_count': urls_count,
                'user_mentions_count': user_mentions_count
            })
            if i % 100 == 0:
                print("Read entries %s..." % i)
            i += 1
    return tweets


def read_todo_from_emtpy_file(the_dataset_file):
    todos = list()
    header = True
    i = 1
    with file(the_dataset_file, 'r') as infile:
        for line in infile:
            if header:
                header = False
                continue
            line_array = line.strip().split(',')
            tweet = ','.join(line_array[4:])
            json_obj = json.loads(tweet)
            user_id = line_array[0]
            tweet_id = json_obj['id']
            todos.append({
                'user_id': user_id,
                'tweet_id': tweet_id
            })
            if i % 100 == 0:
                print("Read entries %s..." % i)
            i += 1
    return todos


def read_datasets():
    tweets_train = read_train_dataset('/Users/jwasilewski/Datasets/RecSys2014/training.dat')
    tweets_test = read_test_dataset('/Users/jwasilewski/Datasets/RecSys2014/test.dat')
    return tweets_train, tweets_test


def read_datasets_sample():
    tweets_train = read_train_dataset('/Users/jwasilewski/Datasets/RecSys2014/training.dat', 1000)
    tweets_test = read_test_dataset('/Users/jwasilewski/Datasets/RecSys2014/test.dat', 1000)
    return tweets_train, tweets_test


def get_users_items_lists(train, test):
    users = list()
    items = list()
    for tweet in train:
        user_id = tweet['user_id']
        item_id = tweet['imdb_item_id']
        if user_id not in users:
            users.append(user_id)
        if item_id not in items:
            items.append(item_id)
    for tweet in test:
        user_id = tweet['user_id']
        item_id = tweet['imdb_item_id']
        if user_id not in users:
            users.append(user_id)
        if item_id not in items:
            items.append(item_id)
    users.sort(key=int)
    items.sort(key=int)
    return users, items


def transform_dataset_to_lists(tweets, users, items):
    ratings = list()
    engagements = list()
    i = 0
    for tweet in tweets:
        user_id = tweet['user_id']
        item_id = tweet['imdb_item_id']
        rating = tweet['imdb_rating']
        if rating > 10:
            rating = 10
        if rating < 1:
            rating = 1
        engagement = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
        uidx = users.index(user_id)
        iidx = items.index(item_id)
        ratings.append((uidx, iidx, rating))
        engagements.append((uidx, iidx, engagement))
        if i % 100 == 0:
            print("Processing %s..." % i)
        i += 1
    ratings = sorted(ratings, key=lambda data: (int(data[0]), int(data[1])))
    engagements = sorted(engagements, key=lambda data: (int(data[0]), int(data[1])))
    return ratings, engagements


def save_list(list_set, output_file):
    lines = list()
    for (uidx, iidx, value) in list_set:
        line = str(uidx) + '\t' + str(iidx) + '\t' + str(value) + '\n'
        lines.append(line)

    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def save_list_for_cofirank(list_set, output_file):
    lines = list()
    prev_uidx = list_set[0][0]
    line = ''
    i = 1
    for (uidx, iidx, value) in list_set:
        while i < uidx:
            lines.append('\n')
            i += 1
        if prev_uidx != uidx:
            prev_uidx = uidx
            line += '\n'
            lines.append(line)
            i += 1
            line = ''
        line = line + str(iidx) + ':' + str(value) + ' '
    line += '\n'
    lines.append(line)

    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def save_list_for_rankals1(list_set, output_file):
    dataset = sorted(list_set, key=lambda data: (int(data[0]), int(data[1])))
    lines = list()
    prev_uidx = None
    icnt = 0
    i = 1
    for (uidx, iidx, value) in dataset:
        while i < uidx:
            lines.append(str(icnt) + '\n')
            i += 1
        if prev_uidx != uidx:
            prev_uidx = uidx
            lines.append(str(icnt) + '\n')
            i += 1
        icnt += 1
    # icnt += 1
    lines.append(str(icnt) + '\n')

    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def save_list_for_rankals2(list_set, output_file):
    dataset = sorted(list_set, key=lambda data: (int(data[1]), int(data[0])))
    lines = list()
    prev_iidx = None
    ucnt = 0
    i = 1
    for (uidx, iidx, value) in dataset:
        while i < iidx:
            lines.append(str(ucnt) + '\n')
            i += 1
        if prev_iidx != iidx:
            prev_iidx = iidx
            lines.append(str(ucnt) + '\n')
            i += 1
        ucnt += 1
    # ucnt += 1
    lines.append(str(ucnt) + '\n')

    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def save_hashtags_engagement(dataset, output_file):
    lines = list()
    for tweet in dataset:
        engagement = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
        lines.append(str(tweet['hashtags_count']) + ',' + str(tweet['urls_count']) + ',' + str(tweet['user_mentions_count']) + ',' + str(engagement) + '\n')

    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def save_ratings_engagement(dataset, output_file):
    lines = list()
    for tweet in dataset:
        if tweet['tweet_is_retweet']:
            continue
        engagement = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
        lines.append(str(tweet['imdb_rating']) + ',' + str(engagement) + '\n')

    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def save_tweet_engagement_per_item(dataset, model_parameters, output_file):
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']
    lines = list()
    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        engagement = int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count'])
        if item_id in tweets_with_engagement_count:
            aa = tweets_with_engagement_count[item_id]
        else:
            aa = 0
        if item_id in tweets_with_engagement_sum:
            bb = tweets_with_engagement_sum[item_id]
        else:
            bb = 0
        lines.append(str(item_id) + ',' + str(aa) + ',' + str(bb) + ',' + str(engagement) + '\n')
    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def split_train_dataset(the_dataset_file, model_parameters, cluster_id, output_file):
    clusters = model_parameters['clusters']
    header = True
    lines = list()
    with file(the_dataset_file, 'r') as infile:
        for line in infile:
            if header:
                header = False
                lines.append(line)
                continue
            line_array = line.strip().split(',')
            item_id = line_array[1]
            if item_id in clusters and clusters[item_id] == cluster_id:
                lines.append(line)
    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def split_test_dataset_unknown(the_dataset_file, model_parameters, output_file):
    clusters = model_parameters['clusters']
    header = True
    lines = list()
    with file(the_dataset_file, 'r') as infile:
        for line in infile:
            if header:
                header = False
                lines.append(line)
                continue
            line_array = line.strip().split(',')
            item_id = line_array[1]
            if item_id not in clusters:
                lines.append(line)
    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


