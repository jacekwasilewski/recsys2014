import subprocess
import dataset


def read_solution(the_solution_file):
    solutions = list()
    header = True
    with file(the_solution_file, 'r') as infile:
        for line in infile:
            if header:
                header = False
                continue
            line_array = line.strip().split(',')
            user_id = line_array[0]
            tweet_id = line_array[1]
            engagement = float(line_array[2])
            solutions.append(list((user_id, tweet_id, engagement)))
    return solutions


def write_the_solution_file(solutions, the_solution_file, evaluate=False):
    lines = list()
    lines.append('userid,tweetid,engagement' + '\n')

    for (user, tweet, engagement) in solutions:
        line = str(user) + ',' + str(tweet) + ',' + str(engagement) + '\n'
        lines.append(line)

    with file(the_solution_file, 'w') as outfile:
        outfile.writelines(lines)
    if evaluate:
        p = subprocess.Popen('java -jar rscevaluator-0.14-jar-with-dependencies.jar test_solution.dat %s' % the_solution_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        p.wait()
        print lines[8]


def write_the_solution_file_debug(solutions, the_solution_file):
    lines = list()
    lines.append('userid,tweetid,engagement' + '\n')

    for (user, tweet, engagement, debug) in solutions:
        line = str(user) + '\t' + str(tweet) + '\t' + "{:6.1f}".format(engagement) + '\t\t' + str(debug) + '\n'
        lines.append(line)

    with file(the_solution_file, 'w') as outfile:
        outfile.writelines(lines)


def write_debug(debug, the_solution_file):
    lines = list()
    lines.append('cluster,item_id,tweet_id,user_id,lcme,rating_1,rating_2,rating_3,rating_4,rating_5,rating_6,rating_7,rating_8,rating_9,rating_10,lime,lume,tweet_is_retweet,user_mentions0,user_mentions1,item_had_engagement,user_had_engagement,rating,iep,uep,cep,ucep,user_mentions,engagement' + '\n')

    for (cluster,item_id, tweet_id, user_id, lcme, rating_1, rating_2, rating_3, rating_4, rating_5, rating_6, rating_7, rating_8, rating_9, rating_10, lime, lume, tweet_is_retweet, user_mentions0, user_mentions1, item_had_engagement, user_had_engagement, rating, iep, uep, cep, ucep, user_mentions, engagement) in debug:
        line = str(cluster)+','+str(item_id) + ',' + str(tweet_id)+','+ str(user_id)+','+ str(lcme)+','\
               +str(rating_1)+','+str(rating_2)+','+str(rating_3)+','+ str(rating_4)+','+ str(rating_5)+','+str(rating_6)+','+ str(rating_7)+','+str(rating_8)+','+str(rating_9)+','+str(rating_10)+','\
               +str(lime)+','+str(lume)+','+str(tweet_is_retweet)+','+str(user_mentions0)+','+str(user_mentions1)+','+str(item_had_engagement)+','+str(user_had_engagement)+','+str(rating)+','+str(iep)+','+str(uep)+','+str(cep)+','+str(ucep)+','+str(user_mentions)+','+str(engagement)+'\n'
        lines.append(line)

    with file(the_solution_file, 'w') as outfile:
        outfile.writelines(lines)


def sort_the_solution(solutions):
    return sorted(solutions, key=lambda data: (-int(data[0]), -float(data[2]), -int(data[1])))


def threshold_the_solution(solutions, topn, user_had_engagement):
    user_i = None
    prev_user = None
    new_solutions = list()
    for (user_id, tweet_id, engagement) in solutions:
        if user_id != prev_user:
            prev_user = user_id
            user_i = 0
        user_i += 1
        if user_i > topn and user_id in user_had_engagement and not user_had_engagement[user_id]:
            engagement = 0.0
        new_solutions.append((user_id, tweet_id, engagement))
    return new_solutions


def split_solution(dataset_file, the_solution_file, output_file):
    test = dataset.read_test_dataset(dataset_file)
    tweets = list()
    for tweet in test:
        tweet_id = str(tweet['tweet_id'])
        tweets.append(tweet_id)

    header = True
    lines = list()
    with file(the_solution_file, 'r') as infile:
        for line in infile:
            if header:
                header = False
                lines.append(line)
                continue
            line_array = line.strip().split(',')
            tweet_id = str(line_array[1])
            if tweet_id in tweets:
                lines.append(line)

    with file(output_file, 'w') as outfile:
        outfile.writelines(lines)


def write_the_solution_file_clustered(solutions, the_solution_file, cluster):
    lines = list()
    lines.append('userid,tweetid,engagement' + '\n')

    for (user, tweet, engagement) in solutions:
        line = str(user) + ',' + str(tweet) + ',' + str(engagement) + '\n'
        lines.append(line)

    with file(the_solution_file, 'w') as outfile:
        outfile.writelines(lines)

    p = subprocess.Popen('java -jar rscevaluator-0.14-jar-with-dependencies.jar test_solution_%s.dat %s' % (str(cluster), the_solution_file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    p.wait()
    print lines[8]


def prepare_solutions(tweets_test, predictions):
    solutions = list()
    for i, tweet in enumerate(tweets_test):
        solutions.append((tweet['user_id'], tweet['tweet_id'], predictions[i]))
    solutions = sort_the_solution(solutions)
    write_the_solution_file(solutions, 'solutions.dat', True)


def prepare_solutions_for_evaluation(tweets_test, predictions):
    solutions = list()
    for i, tweet in enumerate(tweets_test):
        solutions.append((tweet['user_id'], tweet['tweet_id'], predictions[i]))
    solutions = sort_the_solution(solutions)
    write_the_solution_file(solutions, 'evaluation_solution.dat', False)
