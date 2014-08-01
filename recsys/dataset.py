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
                retweet_of = json_obj['retweeted_status']['id']
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
                'user_created_at': user_created_at_date
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
            tweet_created_at_date = parser.parse(tweet_created_at).strftime('%Y-%m-%d %H:%M:%S')
            user_created_at_date = parser.parse(user_created_at).strftime('%Y-%m-%d %H:%M:%S')
            is_retweet = 'retweeted_status' in json_obj
            retweet_of = None
            if is_retweet:
                retweet_of = json_obj['retweeted_status']['id']
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
                'user_created_at': user_created_at_date
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
    tweets_test = read_train_dataset('/Users/jwasilewski/Datasets/RecSys2014/test.dat')
    return tweets_train, tweets_test


def read_datasets_sample():
    tweets_train = read_train_dataset('/Users/jwasilewski/Datasets/RecSys2014/training.dat', 1000)
    tweets_test = read_train_dataset('/Users/jwasilewski/Datasets/RecSys2014/test.dat', 1000)
    return tweets_train, tweets_test