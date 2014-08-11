from datetime import datetime
from math import log
import random
from scipy.cluster.vq import whiten
import item_clustering
import statistics
import solution
import numpy


def run_model(train, test, model_parameters):
    codebook = model_parameters['codebook']
    ip_codebook = model_parameters['ip_codebook']
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']
    cluster_user_eng = model_parameters['cluster_user_eng']
    # items_stats = model_parameters['items_stats']
    ip_clusters = model_parameters['ip_clusters']
    users_stats = model_parameters['users_stats']
    # train_tweets_per_day = model_parameters['tweets_per_day']

    ffts_test, ffts_test_labels = item_clustering.compute_fft_full(test)
    whitened_test = whiten(ffts_test)
    clusters_test = item_clustering.assign_clusters(whitened_test, ffts_test_labels, codebook)

    items_test_stats = dict()
    user_test_stats = dict()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        if rating < 1:
            rating = 1

        if item_id in items_test_stats:
            items_test_stats[item_id]['count'] += 1.0
            items_test_stats[item_id]['ratings_count'][rating] += 1.0
        else:
            items_test_stats[item_id] = dict()
            items_test_stats[item_id]['count'] = 1.0
            items_test_stats[item_id]['ratings_count'] = dict()
            for r in range(10):
                items_test_stats[item_id]['ratings_count'][r + 1] = 0.0
            items_test_stats[item_id]['ratings_count'][rating] = 1.0

        if user_id in user_test_stats:
            user_test_stats[user_id]['count'] += 1.0
        else:
            user_test_stats[user_id] = dict()
            user_test_stats[user_id]['count'] = 1.0

    # print('Clustering item popularity...')
    # items_test_count = list()
    # items_test_count_labels = list()
    # for tweet in test:
    #     item_id = tweet['imdb_item_id']
    #     items_test_count.append(items_test_stats[item_id]['count'])
    #     items_test_count_labels.append(item_id)

    # ------------

    i = 0
    print('Applying model...')
    solutions = list()
    solutions_debug = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])
        if rating < 1:
            rating = 1

        user_followers_count = int(tweet['user_followers_count'])
        user_statuses_count = int(tweet['user_statuses_count'])

        hashtags_count = tweet['hashtags_count']
        symbols_count = tweet['symbols_count']
        urls_count = tweet['urls_count']
        user_mentions_count = tweet['user_mentions_count']

        scraping_date = datetime.fromtimestamp(int(tweet['tweet_scraping_time']))
        tweet_date = datetime.strptime(tweet['tweet_created_at'], '%Y-%m-%d')
        user_date = datetime.strptime(tweet['user_created_at'], '%Y-%m-%d')
        user_age = (scraping_date - user_date).days
        tweet_age = (scraping_date - tweet_date).days
        relative_tweet_age = (tweet_date - user_date).days

        # fft_test = item_clustering.compute_fft_for_test(train_tweets_per_day, test, tweet)
        # whitened_tweet = numpy.array([fft_test])
        # cluster = item_clustering.assign_clusters_for_test(whitened_tweet, codebook)
        cluster = clusters_test[item_id]
        ip_cluster = None
        if item_id in ip_clusters:
            ip_cluster = ip_clusters[item_id]

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
        # 0.8411723432384
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
        # if item_id in ip_clusters:
        #     if ip_clusters[item_id] == 0:
        #         item_popularity = -10
        #     elif ip_clusters[item_id] == 1:
        #         item_popularity = -5
        #     elif ip_clusters[item_id] == 2:
        #         item_popularity = -20
        #     elif ip_clusters[item_id] == 3:
        #         item_popularity = 60
        #     elif ip_clusters[item_id] == 4:
        #         item_popularity = 90
        # else:
        #     item_popularity = 25
        #
        # if user_id in cluster_user_eng and cluster_user_eng[user_id][cluster]['eng_count'] > 0:
        #     cluster_coefficient = 1.0 + 0.025 * log(cluster_user_eng[user_id][cluster]['eng_sum'] / cluster_user_eng[user_id][cluster]['eng_count'])
        # else:
        #     cluster_coefficient = 1.0
        #
        # engagement = (base + rating_base + item_popularity) * engagement_coefficient * cluster_coefficient
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
        # 0.8425107067233986
        engagement = 0.0

        item_cluster0 = 0
        item_cluster1 = 0
        item_cluster2 = 0

        if cluster == 0:
            item_cluster0 = 1
        elif cluster == 1:
            item_cluster1 = 1
        elif cluster == 2:
            item_cluster2 = 1

        cluster_base = 1.0 + 0.99 * log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])

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

        item_popularity_cluster_none = 0
        item_popularity_cluster0 = 0
        item_popularity_cluster1 = 0
        item_popularity_cluster2 = 0
        item_popularity_cluster3 = 0
        item_popularity_cluster4 = 0

        if ip_cluster == 0:
            item_popularity_cluster0 = 1
        elif ip_cluster == 1:
            item_popularity_cluster1 = 1
        elif ip_cluster == 2:
            item_popularity_cluster2 = 1
        elif ip_cluster == 3:
            item_popularity_cluster3 = 1
        elif ip_cluster == 4:
            item_popularity_cluster4 = 1
        else:
            item_popularity_cluster_none = 1

        item_score = item_rating * cluster_base * engagement_coefficient * cluster_coefficient
        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 7 * item_cluster0 + 5 * item_cluster1 + 4 * item_cluster2
        engagement += 0 * item_popularity_cluster0 + 10 * item_popularity_cluster1 - 20 * item_popularity_cluster2 + 150 * item_popularity_cluster3 + 150 * item_popularity_cluster4 + 7 * item_popularity_cluster_none
        engagement += item_score
        engagement += 600 * user_mentions0
        engagement += 50 * user_mentions1
        engagement += 600 * tweet_is_retweet

        engagement = round(engagement)

        if not tweet_is_retweet:
            if tweet_age > 22:
                engagement = 0.0
            if user_followers_count < 10:
                engagement = 0.0
            if user_statuses_count < 40:
                engagement = 0.0
            if engagement <= 40:
                engagement = 0.0

        # ------------------
        solutions.append((user_id, tweet['tweet_id'], engagement))
        solutions_debug.append((user_id, tweet['tweet_id'], engagement, ''))

        if i % 100 == 0:
            print("Proccessed items %s..." % i)
        i += 1

    print('Sorting solution...')
    solutions = solution.sort_the_solution(solutions)
    solutions_debug = solution.sort_the_solution(solutions_debug)

    print('Saving solution...')
    solution.write_the_solution_file(solutions, '/Users/jwasilewski/RecSys2014/solution.dat')
    solution.write_the_solution_file_debug(solutions_debug, '/Users/jwasilewski/RecSys2014/solution_debug.dat')


def create_features(dataset, model_parameters, train=True):
    codebook = model_parameters['codebook']
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']
    cluster_user_eng = model_parameters['cluster_user_eng']
    ip_clusters = model_parameters['ip_clusters']

    ffts_test, ffts_test_labels = item_clustering.compute_fft_full(dataset)
    whitened_test = whiten(ffts_test)
    clusters_test = item_clustering.assign_clusters(whitened_test, ffts_test_labels, codebook)

    ids = list()
    features = list()
    labels = list()
    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])
        user_mentions_count = tweet['user_mentions_count']
        cluster = clusters_test[item_id]
        ip_cluster = None
        if item_id in ip_clusters:
            ip_cluster = ip_clusters[item_id]


        item_cluster0 = 0
        item_cluster1 = 0
        item_cluster2 = 0

        if cluster == 0:
            item_cluster0 = 1
        elif cluster == 1:
            item_cluster1 = 1
        elif cluster == 2:
            item_cluster2 = 1

        cluster_base = 1.0 + 0.99 * log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])
        cae1 = cluster_avg_engs[cluster]['eng_sum']
        cae2 = cluster_avg_engs[cluster]['eng_count']

        rating_h = 0
        rating_m = 0
        rating_l = 0
        if rating > 6:
            item_rating = 50 * rating
            rating_h = 1
        elif rating < 2:
            item_rating = 490 * rating
            rating_l = 1
        else:
            item_rating = 5 * rating
            rating_m = 1

        if item_id in tweets_with_engagement_count:
            engagement_coefficient = 1.1 + 0.26 * log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])
            twe1 = tweets_with_engagement_sum[item_id]
            twe2 = tweets_with_engagement_count[item_id]
        else:
            engagement_coefficient = 1.0
            twe1 = 0
            twe2 = 0

        if user_id in cluster_user_eng and cluster_user_eng[user_id][cluster]['eng_count'] > 0:
            cluster_coefficient = 1.031 + 0.26 * log(cluster_user_eng[user_id][cluster]['eng_sum'] / cluster_user_eng[user_id][cluster]['eng_count'])
            cue1 = cluster_user_eng[user_id][cluster]['eng_sum']
            cue2 = cluster_user_eng[user_id][cluster]['eng_count']
        else:
            cluster_coefficient = 1.0
            cue1 = 0
            cue2 = 0

        item_popularity_cluster_none = 0
        item_popularity_cluster0 = 0
        item_popularity_cluster1 = 0
        item_popularity_cluster2 = 0
        item_popularity_cluster3 = 0
        item_popularity_cluster4 = 0

        if ip_cluster == 0:
            item_popularity_cluster0 = 1
        elif ip_cluster == 1:
            item_popularity_cluster1 = 1
        elif ip_cluster == 2:
            item_popularity_cluster2 = 1
        elif ip_cluster == 3:
            item_popularity_cluster3 = 1
        elif ip_cluster == 4:
            item_popularity_cluster4 = 1
        else:
            item_popularity_cluster_none = 1

        # engagement = 7 * item_cluster0 + 5 * item_cluster1 + 4 * item_cluster2
        # engagement += 0 * item_popularity_cluster0 + 10 * item_popularity_cluster1 - 20 * item_popularity_cluster2 + 150 * item_popularity_cluster3 + 150 * item_popularity_cluster4 + 7 * item_popularity_cluster_none
        # engagement += item_rating * cluster_base * engagement_coefficient * cluster_coefficient
        # engagement += 600 * (user_mentions_count > 0)
        # engagement += 50 * (user_mentions_count > 1)
        # engagement += 600 * (True == tweet['tweet_is_retweet'])

        # ids.append((user_id, tweet['tweet_id']))
        if int(tweet['tweet_favourite_count']) + int(tweet['tweet_retweet_count']) > 0:
            engagement = True
        else:
            engagement = False
        # labels.append(engagement)
        features.append((user_id, tweet['tweet_id'], item_cluster0, item_cluster1, item_cluster2, item_popularity_cluster0, item_popularity_cluster1, item_popularity_cluster2, item_popularity_cluster3, item_popularity_cluster4, item_popularity_cluster_none, item_rating * cluster_base * engagement_coefficient * cluster_coefficient, int(user_mentions_count > 0), int(user_mentions_count > 1), int(True == tweet['tweet_is_retweet']), rating_l, rating_m, rating_h, cae1,cae2, twe1,twe2,cue1,cue2,engagement))
    return features


def run_model2(dataset, model_parameters):
    codebook = model_parameters['codebook']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    cluster_user_eng = model_parameters['cluster_user_eng']

    ffts_test, ffts_test_labels = item_clustering.compute_fft(dataset)
    whitened_test = whiten(ffts_test)
    clusters_test = item_clustering.assign_clusters(whitened_test, ffts_test_labels, codebook)

    print('Applying model...')
    solutions = list()
    for tweet in dataset:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])
        if rating < 1:
            rating = 1

        cluster = clusters_test[item_id]

        cluster_avg_engagement = log(cluster_avg_engs[cluster]['eng_sum'] / cluster_avg_engs[cluster]['eng_count'])

        if rating > 6:
            item_rating = 50 * rating
        elif rating < 2:
            item_rating = 490 * rating
        else:
            item_rating = 5 * rating
        item_rating = rating

        is_retweet = 0
        if tweet['tweet_is_retweet']:
            is_retweet = 1

        if item_id in tweets_with_engagement_count:
            engagement_coefficient = log(tweets_with_engagement_sum[item_id] / tweets_with_engagement_count[item_id])
        else:
            engagement_coefficient = 0.0

        if user_id in cluster_user_eng and cluster_user_eng[user_id][cluster]['eng_count'] > 0:
            cluster_coefficient = log(cluster_user_eng[user_id][cluster]['eng_sum'] / cluster_user_eng[user_id][cluster]['eng_count'])
        else:
            cluster_coefficient = 0.0

        engagement = 3.0109 * cluster + 48.8665 * cluster_avg_engagement + 13.8633 * is_retweet + 4.2272 * engagement_coefficient + 1.1179 * cluster_coefficient + -21.1935
        solutions.append((user_id, tweet['tweet_id'], engagement))

    print('Sorting solution...')
    solutions = solution.sort_the_solution(solutions)

    print('Saving solution...')
    solution.write_the_solution_file(solutions, '/Users/jwasilewski/RecSys2014/solution.dat')


def write_features(features, filename):
    lines = list()
    lines.append('user_id,tweet_id,item_cluster0,item_cluster1,item_cluster2,item_popularity_cluster0,item_popularity_cluster1,item_popularity_cluster2,item_popularity_cluster3,item_popularity_cluster4,item_popularity_cluster_none,user_mentions0,user_mentions1,tweet_is_retweet,rating_l,rating_m,rating_h,cae1,cae2,twe1,twe2,cue1,cue2,engagement\n')

    for (user_id,tweet_id,item_cluster0,item_cluster1,item_cluster2,item_popularity_cluster0,item_popularity_cluster1,item_popularity_cluster2,item_popularity_cluster3,item_popularity_cluster4,item_popularity_cluster_none,item_score,user_mentions0,user_mentions1,tweet_is_retweet,rating_l,rating_m,rating_h,cae1,cae2,twe1,twe2,cue1,cue2,engagement) in features:
        line = str(user_id) + ',' + str(tweet_id)+','+str(item_cluster0)+','+str(item_cluster1)+','+str(item_cluster2)+','+str(item_popularity_cluster0)+','+str(item_popularity_cluster1)+','+str(item_popularity_cluster2)+','+str(item_popularity_cluster3)+','+str(item_popularity_cluster4)+','+str(item_popularity_cluster_none)+','+str(user_mentions0)+','+str(user_mentions1)+','+str(tweet_is_retweet)+','+str(rating_l)+','+str(rating_m)+','+str(rating_h)+','+str(cae1)+','+str(cae2)+','+str(twe1)+','+str(twe2)+','+str(cue1)+','+str(cue2)+','+str(engagement)+'\n'
        lines.append(line)

    with file(filename, 'w') as outfile:
        outfile.writelines(lines)


def run_logreg(train, test, model_parameters):
    codebook = model_parameters['codebook']
    items_stats = model_parameters['items_stats']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    users_stats = model_parameters['users_stats']

    ffts_test, ffts_test_labels = item_clustering.compute_fft(test)
    whitened_test = whiten(ffts_test)
    clusters_test = item_clustering.assign_clusters(whitened_test, ffts_test_labels, codebook)

    solutions = list()
    tweets_per_cluster = dict()
    tweets_per_cluster[0] = 0
    tweets_per_cluster[1] = 0
    tweets_per_cluster[2] = 0
    tweets_per_cluster_all = dict()
    tweets_per_cluster_all[0] = 0
    tweets_per_cluster_all[1] = 0
    tweets_per_cluster_all[2] = 0
    for tweet in test:
        user_id = tweet['user_id']
        item_id = tweet['imdb_item_id']
        tweet_id = tweet['tweet_id']
        rating = tweet['imdb_rating']

        cluster = clusters_test[item_id]

        engagement = 0
        if tweet['tweet_is_retweet']:
            engagement = 1
        else:
            tweets = ['421094807046324225', '421104392784609280', '421104885942468608', '421131508095909888', '421302800782725121', '421306507712815104', '421319747100495872', '421344840131936256', '421348102394892288', '421141436252160000', '421173057643094016', '421185937436327936', '421227814432800768', '421047840891469824', '421051629673414656', '421055812019429376', '421700598288089088', '421734435181326337', '421749094504472576', '421757805650247680', '421758890884468736', '421762466910314497', '421763894067990528', '421381788964229121', '421390088153874433', '421391608245157888', '421393665907367936', '421396705096269824', '421401554701520896', '421418587169898496', '421428086429990912', '421432010692112385', '421434439894581249', '421442425367052288', '421457626837561345', '421465341076971520', '421469875199299584', '421472414519025664', '421486769021145088', '421502137416171520', '421505173442531328', '421511081203601408', '421517063870750720', '421536828886642688', '421556924552065024', '421556986074120192', '421563630211981312', '421609526815510528', '421633128370028544', '421637460041691136', '421645583191777280', '421658121237708800', '421670962753703936', '421688587781148673', '421689055861305344', '421787449556467712', '421791862203371521', '421793646376411136', '421795182263021568', '421797495891820545', '421805088542580736', '421806175706165249', '421807132283912192', '421807364950736896', '421841655143354368', '421844708760231936', '421849881687638016', '421853472665772033', '421854612455714816', '421864043469885440', '421864857764237312', '421866371665121281', '421867737674047488', '421868777609760768', '421877064132591616', '421887627361406976', '421904355265372160', '421904548924776448', '421932037927235586', '421937921751781376', '421943679998500864', '421947320998322176', '421958496096366592', '421968724107616256', '421973218334113792', '421990518176768000', '422004213040693248', '422010466089848832', '422031194445070336', '421807791939268608', '421811797885476864', '421812826077151232', '421818430782967809', '421837555198218240', '421772223465422848', '421775904717942784', '421780587087949824', '421783095818588160', '421785399074516992', '422200371671732224', '422200828334972928', '422212410359820288', '422214250090610688', '422214406945378304', '422219351354114049', '422224987437924352', '422226582418497536', '422228000399048704', '422228080568967168', '422228337163919360', '422252554513575936', '422257117945659392', '422258433014779905', '422266357300744192', '422281249399382016', '422289611084161024', '422289718798454784', '422291309005520897', '422294947547856896', '422054234545459201', '422069692778295296', '422070002716803072', '422070718554456064', '422091494741512192', '422096754289692672', '422097441999953921', '422108691614420992', '422108780051312640', '422115909747376128', '422122444464209920', '422123932498804736', '422125311455924224', '422126709606199297', '422137242921213952', '422140181140234240', '422143204537139200', '422143643051646976', '422143772315893761', '422146455479267329', '422148330702258176', '422159923217461248', '422160012027658240', '422160457924087808', '422161398714884096', '422163244942626817', '422170482519973888', '422186825982439424', '422367385824559104', '422381551528464384', '422381706654797824', '422381932576800769', '422382783064211456', '422420968494346240', '422421237668007936', '422421804154892288', '422426195771551744', '422429943360790529', '422443748854091777', '422445715265449984', '422446825673867264', '422447223524589568', '422448089677713408', '422452124421984256', '422455488052461568', '422458718899695616', '422460993420406785', '422466169501937664', '422474446826663936', '422477281420783616', '422479061748031488', '422480215462666240', '422483413040631808', '422483518082789377', '422487418634522625', '422492208823271426', '422502665260900352', '422385702140411904', '422395954759618560', '422400783007887360', '422418681306443776', '422323863813652481', '422332267202363392', '422332386638970880', '422332447486144512', '422332488409952256', '422332531430936576', '422332575202684928', '422332614696259584', '422332708829032448', '422332765145927680', '422332813434970112', '422332852790104064', '422334268829089792', '422852646547243008', '422854270505844737', '422865900111691776', '422876541589422080', '422877174732177408', '422878098670252032', '422879721719099392', '422888878656475136', '422893197078327296', '422894880701296640', '422897731053813760', '422908022529466368', '422916982745604096', '422918294291898368', '422506882805534720', '422517313146208257', '422529965843021824', '422540972288126977', '422571029119373312', '422574842714411008', '422606176409231360', '422612313204477952', '422645389284892672', '422673051566612481', '422674835836522496', '422675289135939584', '422697544427503617', '422704017182326785', '422709271957356544', '422711895208906752', '422719714859958273', '422749759657758720', '422755590398832640', '422758457776037888', '422820223902035969', '422824677602369536', '422838699169419265', '422844645228679168', '422845366103732224', '423029609781682177', '423029827528966144', '423033096972541952', '423034082332008449', '423034299932495872', '423036307775164416', '423037477793058816', '423040770653036544', '423054355554504704', '423057148097351680', '423083486669332480', '423165093744877569', '423165233960865792', '423181661732601856', '423185847761252352', '423195134428446720', '423198584348360704', '423219645630664704', '423225667107692544', '423226712974176256', '423229996417941505', '423242782975987712', '423246980790636544', '423248915140710400', '423289544298205184', '423293991795163137', '423306645184454656', '423339056416583680', '423099752138674176', '423124176401338368', '422929880766894080', '422941443091865600', '422944320157921280', '422967729490886656', '422968698023215104', '422980733645250560', '423699108583313409', '423701523583881216', '423702580259069952', '423717921970724864', '423720106691002368', '423346763118817280', '423353638312894464', '423388622742511616', '423390522255101952', '423410503461777408', '423410580762808321', '423413723647078400', '423420729128792064', '423432047504674816', '423445261700968448', '423483910551797760', '423488500819034112', '423506192837529600', '423522013328969728', '423531994920652800', '423543017124143105', '423544738092830720', '423545162128580608', '423551572279193600', '423564721321943040', '423569799244156929', '423571314499416064', '423578205178830848', '423595144789917697', '423596469099454464', '423599879748087808', '423611331628257280', '423611806159208448', '423621259772313600', '423637503938408448', '423659581206958080', '423673627436138496', '423675727847100416', '423934081320386560', '423946877504352256', '423989515951538176', '424015271536250880', '424028046254178304', '424055529250783232', '424058406551318528', '424067528282112000', '424084914905296897', '424131677695537152', '424166639610109952', '424167825272762368', '424169494324719616', '424169637132369920', '424192348948422656', '424200023677878273', '424201000699035648', '424210769086263296', '424212209926160385', '424217724970344448', '424242730437312512', '424244352509280256', '424244469144109056', '423956523082334208', '423984270294908929', '423858889533423616', '423888397951070208', '423890517756084224', '423899421857026048', '423911256442302464', '424511212496252928', '424515228030619648', '424532540092059648', '424551320679632896', '424555206354161664', '424556640550289408', '424562334099857409', '424589110624653312', '424257319484919808', '424259658870579200', '424261623529078784', '424269221502394368', '424273474480136192', '424274511148879872', '424280015489208321', '424281260874539008', '424288891039129600', '424298176569679872', '424310845443932160', '424318166467354624', '424319795677642752', '424329683308912640', '424332505853214720', '424344297698496512', '424354888458711040', '424358735814098945', '424359235313754112', '424360141912567808', '424360139593121792', '424362037704417280', '424366690554880001', '424413289217392640', '424420010778316803', '424439228345622528', '424448388155707392', '424461720828911616', '424469032222593024', '424480717465075712', '424492993656414208', '424497102895738880', '424505318102814720', '424628816716128256', '424630992880795648', '424633497232609280', '424641435368194048', '424643971546353664', '424645327573221376', '424646493359054848', '424670954351247360', '424675915332067328', '424685143534895105', '424688570818121729', '424688775810523136', '424693348725956608', '424693610874142720', '424696214052147200', '424696651328925696', '424699936245305344', '424702821569941504', '424703048137863168', '424704421571067904', '424713836902756352', '424714718281220096', '424738135340089344', '424740597803397120', '424770935041036288', '424772192744648704', '424657694633787392', '424659122219646976', '424659756763316225', '424660750612041728', '424665739346591744', '424667258783543296', '424667335442845696', '424594927176011776', '424610472374308864', '424622429999071232', '424624279796215808', '425010042690342912', '425012328946761728', '425015558309150720', '425021286939918336', '425024654747922432', '425032099201286144', '425034873615949824', '425035662690357248', '425040430091493376', '425042493944918017', '424785918705147904', '424786653463339009', '424788690796154881', '424799468605542400', '424814317603520513', '424814745976184832', '424817478468767744', '424821846068822016', '424843229826387968', '424848466678775808', '424848956271521792', '424877627112161280', '424888135966031872', '424898336727261184', '424904129215881216', '424911996409372674', '424917148398809088', '424919432482127873', '424919966681669632', '424927131022667776', '424934741612433408', '424935309097570304', '424936432801558528', '424943912118407168', '424946222991159296', '424949694012198912', '424963392311681024', '424968136723812352', '424969221085618176', '424982852732989441', '424989894247972864', '424996865265123328', '424997026678337536', '425068340831608832', '425088404145971200', '425107239674736641', '425108224233459712', '425184939186094080', '425194641743675392', '425231342901948416', '425257140438454272', '425299949593821184', '425306154965958656', '425306165791043585', '425319459449208832', '425327712878600192', '425336861201289216', '425346421576192000', '425348125365002240', '425350215152189440', '425369277051330560', '425374196433055744', '425374518128168960', '425382677588746242', '425383907597774848', '425394262914904064', '425396493273800704', '425396825978585088', '425399569128910848', '425403025377992704', '425116640544444417', '425122203295051776', '425132257150369792', '425141035690229760', '425043590591426562', '425050289365061632', '425053537358610432', '425054682793672704', '425055149640679425', '425062775220469760', '425064248994037761', '425067397104807936', '425769346213105664', '425776185302589440', '425784414787104768', '425787527447187456', '425801789565571072', '425817611319132160', '425821667341131777', '425835402457399296', '425848247135907840', '425857554556538880', '425858184423550976', '425406778709647360', '425411547221880832', '425416978652999680', '425419894201782272', '425421760381870080', '425436202586865664', '425469467775094785', '425494097332158465', '425500295418765312', '425527502652854272', '425569903064907776', '425570669049675776', '425574776607084544', '425612276042059776', '425612365611405312', '425649084096348160', '425668994612207616', '425687911590526977', '425692351047413761', '425695910618988544', '425696030274109440', '425696139212754945', '425698003073396736', '425701080304197632', '425714415322013697', '425720813523058688', '425744962240913408', '425764144336605184', '425985445559021568', '425991148612902912', '426002348117614592', '426033593203580928', '426123821557743616', '426124072016445440', '426134113700282368', '426134428428275712', '426149363837313024', '426155816904060928', '426156219376869376', '426173467323797504', '426174772444024832', '426184704824721408', '426185953133096962', '426197872611438592', '426227909125472256', '426268674148679681', '426269395799646209', '426290571574267904', '426324333212864512', '426327089667899392', '426359376241508352', '426378792660402176', '426382406158151680', '426396698903318529', '426064215280189440', '426073134337626112', '426092911659593728', '425881129926033408', '425896919500476416', '425922558756548608', '425928627734478848', '425951049686728704', '426787960017940480', '426804385348599808', '426811010565943296', '426818536166932480', '426821608443875328', '426833689675587584', '426836519295676416', '426839174613049345', '426839620522115072', '426416032950272000', '426432084781961216', '426447821643206656', '426451171025616896', '426463017384304640', '426467032922476544', '426471119852294144', '426473587370119168', '426479753764548608', '426481241018613762', '426484122832621568', '426484600635142144', '426484661217681409', '426503648949338113', '426528834637545472', '426544213036380160', '426561015695020032', '426563387158302721', '426566889733492736', '426594211329486848', '426598849587601408', '426601936633090048', '426640147455942656', '426665295252422657', '426670088541208576', '426671630585438208', '426716121648353280', '426729618012262400', '426729769070518272', '426741696869965824', '426741937480425472', '427703830386470912', '427722325232873472', '428741089223520256', '428770194501423104', '429724052656500736', '429725307047018498', '429743699644665856', '427197188541014016', '427197191791579136', '427197575662690304', '427203210374557696', '427203262908215296', '427204281997860865', '427731768612233216', '427735814546935808', '427749169856806912', '427762539578290177', '427788559659962369', '428834900540923904', '428860103388049409', '428887156019699712', '429748524226727937', '429750909606715392', '429751267121168386', '429752419778830336', '429752724134313984', '429754724506943488', '429755138325352448', '429756741732294656', '429759799572832256', '427207082228862976', '427211216973750272', '427211729559621632', '427214412701659136', '427215457876447233', '427218131736879105', '427219742873882626', '427219756404727808', '427220881518362624', '427220891400171520', '427851198486822912', '427866554836205568', '427871227496370176', '428936979665784832', '428950829945856000', '428964207963684864', '428985980960657408', '429766035387203584', '429768207604252673', '429768527541985280', '429770292701831168', '429775494952013824', '427225914960015360', '427227395351785472', '427229484732153856', '427230835373535232', '427235093451898880', '427249396028551168', '427901879969153024', '427907478064332800', '427913947594096640', '427915514921631744', '428990207523028992', '429024575699968002', '429876113750638592', '427250188726833153', '427254122728161280', '427258674474917888', '427262605699604480', '427266535095160832', '427276708312780800', '427284762672119809', '427931864230555649', '427937516382322688', '427945242151903232', '427945685481431040', '429040558690938881', '429045374939324416', '429052305494016000', '429052799478161409', '429053633217699840', '429953392207998976', '427311656478052352', '427315316108959744', '427324772679041024', '427326437779984384', '427338365868843008', '427954624952160256', '428010399091277824', '428015844405559296', '429066351874170880', '429093435744595968', '429101351239712768', '429115754676363264', '429124514048659456', '429813758119411712', '429827516459921408', '429830060494057472', '429831007152664577', '427382893883555840', '427384753344757760', '427385258615398400', '428041885806899200', '428051437415710720', '428052165622370304', '428074541920059392', '428080055621672960', '428126783578603520', '428126856496549888', '428128015370174464', '428132431141818369', '429184843008999424', '429224506994208768', '429233724472176640', '429235994026844161', '429905081996435456', '429921696171425793', '429926013121073152', '429929743866421248', '429947638629548032', '429948506422652928', '429950639708573696', '427405570849927168', '427429717747040256', '427434338230468608', '427442336973729792', '428157637830922240', '428159460972822528', '428185101672148992', '428196878300487680', '428203763351158784', '428207310096564224', '428216032042713088', '429263257749438464', '429284786218471424', '429291697152204800', '429310008619044866', '429995442810937344', '429997755936026624', '428244482320904192', '428273776116387843', '428276700301238272', '428281184351961089', '429316851337007104', '429320993371602944', '426846603295862785', '426846823647821824', '426846991151161344', '426847887033901056', '426854619516764160', '426868287017091072', '427484948204101632', '427507556438016000', '428283283193860096', '428283804252651520', '428283935404347392', '428286107735064576', '428290764201005056', '428314059373817857', '429380764514648065', '429383500777947136', '429384405250236416', '429387277958393856', '426885047208398848', '426895516459614208', '426899061875437568', '426912374650839040', '426913920360919040', '427519267320659968', '427519410006667264', '427523916073291776', '428327187255922688', '428349266231562240', '429396390691614721', '429416452941443072', '429416604452278272', '429429648204640256', '426944606723665920', '426958025099063296', '426963986232258560', '427534939400441856', '427536852438896640', '429483962231455744', '429484583374311424', '429500239460843521', '429502010660884480', '427013773006610433', '427020400661258240', '427040204180836352', '427045679664340992', '427554050666934272', '427555538688552960', '427556089161596928', '427556627542474752', '427561354963468288', '427565069522587649', '427565345311055873', '428490405186113536', '428493022557663232', '428501819191730176', '428531089762947072', '428531268393787392', '428542585914007552', '428552647617302528', '429507875874959360', '429512849397133312', '429519081939542017', '429527052861980672', '427059746697670656', '427064916739371008', '427068054124916736', '427077616857014272', '427088465012854784', '427091084624138242', '427091271916994560', '427099745899659265', '427107235940937728', '427573861367185408', '427577678850715648', '427580881931624449', '428565708016865282', '428573010711171072', '428588090933149696', '428589591374086144', '428616677535010816', '428616674292817920', '429578932162404352', '429611761256660992', '429620788325412865', '427117597562523648', '427119151061426176', '427119193969156096', '427147212192509952', '427584394740899840', '427584572918738944', '427587888159531008', '427593141303390208', '427600555083825152', '428631552046956545', '428634410972614656', '428640024729767936', '428641420803854336', '428650262858039297', '428650955509628928', '428652790907691008', '429638481078661120', '429651855098920960', '429658391745941504', '427153620107538432', '427177978091823104', '427186870632853504', '427188542444695552', '427624349852381185', '427632518897360897', '427639017841389568', '428658484130086913', '428660809750048769', '428662377706704896', '428668559364198400', '428685405605871616', '428685484223913985', '428685717121015808', '428701301367910401', '429679171305238528', '429679391472640001', '429695250882654208', '431556502332407809', '431565325856157696', '431570146919194625', '431574532349251584', '431574761471479808', '431575161452904448', '431583263111778304', '431592651289137152', '431592932106600448', '431595850314567680', '432354036554399744', '432355989753315328', '432357413652422656', '432362075382239232', '421548916408987649', '421784473324511232', '422070100305657856', '430447997462532097', '430452574903603200', '430461200842104832', '430462393903489025', '430462991239507968', '430466964642070528', '431605510258044928', '431700288417054720', '432379698966835200', '432386759947583488', '432392664693374976', '422842940579258368', '430486975746174976', '430487887726272512', '430497765429608448', '431753012303134720', '431765289160937472', '431768509010685953', '431774330742403072', '431780839723393024', '431783796472827904', '431784469973188608', '431784722201870338', '431789284824059904', '431792903246340096', '431809871999037440', '432445077731164160', '432470874231668736', '432476349870379008', '432486663965519872', '423970063423528960', '424298159981215744', '424309279592824832', '424401437196828672', '424648600929710080', '430537301794369536', '430570961050812416', '430571107863629824', '430576021658562560', '430585822786887681', '431825206488084480', '431831234566975488', '431847227343241216', '431849836967895041', '431852779976798208', '431873374512766976', '432516178029072384', '432518536963969025', '432520841813704704', '432521429167259648', '432545501645242369', '432550365045596161', '432552115635257345', '432559022525673472', '424663407535853568', '424910805067653121', '425226368142819328', '425061015353851904', '425596899723591680', '430661129996488704', '430668144404086784', '430668371445960704', '430674335653564417', '430680067682082816', '431882469001134080', '431882777840340993', '431884999827398656', '431890975511019520', '431899994199977984', '432590211491856384', '432591869231775744', '426025660143112192', '429016741750915073', '427270071166070784', '427379386472751104', '429216004728582144', '429949363885207552', '428210566964842496', '429363740073791488', '427495827100401664', '430742789882925056', '430747495925567488', '430776716659658752', '430788107236282369', '430796922635706368', '430797229608423424', '430800638952632320', '431913614522331138', '431920189870190593', '431921063275266049', '431923684065161216', '431925394884014081', '431934374050033665', '432595649184681984', '432597121611857920', '432599068951719936', '432602227023175681', '432609209872830464', '432616077764620288', '432619958045278208', '431904485016084480', '431932477092139008', '432616794067861505', '430828569322090496', '430887964227686400', '432657311925272576', '433000429329580032', '430802634338205696', '430810651267588096', '430813315779289088', '430822846479097856', '430829693475241984', '431941178003820544', '431953383738847232', '431958186502160384', '431961574480568320', '431965934711209984', '431973703341981696', '432623979594256384', '426134674235478016', '426495716249575424', '426541852775677952', '426712033992900608', '427862375535239168', '427247421027266560', '430851506049675264', '430863664108015616', '431983626025050112', '431984736462856192', '431997215071293440', '432019166615195648', '432027261785501696', '432650369194549250', '432655876294721536', '432663667847757824', '429565004346822656', '427091944905273344', '429672985796935681', '427173300159393792', '430915858639372288', '430923173690109952', '430938710146707457', '430976904217100288', '432036218873077760', '432088759685750784', '432095530622005249', '432692628493066240', '432693710103408641', '432716346556948480', '430066453396484096', '430069272560148480', '431020041577193472', '431048016426840066', '431048074019229696', '431048124657045504', '431058639441653760', '431061020837019648', '431066716647751680', '431068906623479809', '431077513565990912', '432101219226484736', '432131352025370624', '432764261879021568', '430074907058536448', '430081254328119297', '430084992639959040', '430085069118513152', '430089408617123840', '430089848293052416', '431099409305059328', '431103040096313344', '431103291662290945', '431103886938894338', '431115149865668608', '431117465712869376', '431124509723467776', '431125756245458944', '431125933127643136', '431142899355762689', '432177655475998721', '432178180330635264', '432864307261341696', '432875760026931200', '432892619858116608', '432900480873009152', '432920244966154240', '432925969620676608', '432926270608134145', '432926821710311424', '430100731971260416', '430103668516728832', '430106396059635712', '430108878572097537', '430110880890486784', '430112001340481536', '430114089244041216', '431150927467544576', '431162505533345792', '431183478940778496', '431183586424004608', '432192098482130945', '432201179897298944', '432205375442808832', '432209829419954176', '432219426226962432', '432227743133368320', '432939326004269056', '432957754085752832', '432961974280802305', '432968167384965120', '432968968761249792', '430117120161361920', '430118924152487936', '430127372831322112', '430160861240786944', '431228100576550912', '432230402590515200', '432243183003508736', '432249195660320768', '432256923069857792', '432261458555326465', '432990289423527936', '432990450757402624', '432991598746812417', '432991857338228736', '433000321317879808', '433004352706715649', '433004456498962432', '431295534025162752', '432265929905283072', '432265945315549184', '432269187604434945', '432269935092326402', '432277733918261249', '432279896220770305', '432281800639905792', '432282359552286720', '433016508735029248', '433031247661907968', '433038485529067521', '433065110102212608', '433065182361681920', '430229671083405312', '430254770356756480', '430261141751996416', '430261788056514560', '430283455898087424', '430287732997230593', '430291610857779200', '430313242477740032', '430323903823478784', '431377865415069696', '431444139335372801', '432283778447589376', '432288583828115457', '433098795757600768', '433133122155454464', '433133135333564416', '430362512249217024', '430367133260722176', '430382006976122880', '430386355928317952', '430390126733434880', '431471054121615361', '431471211949068288', '431500712762408960', '431502896778448896', '431503106900504576', '431512845654982656', '431519906375663616', '431521312314785792', '431521456590450691', '432298633334386688', '432302273142996993', '432307020964700161', '432325507305439232', '433219968973684736', '433223951313948672', '433245288846086144', '433258878696837121', '430411708465942528', '430412109542080512', '430412911769833473', '430442426697003008', '431523400025399296', '431544469507555328', '431550430221701120', '431555698220998656', '432329448625799168', '421397270383583232', '421856137659842560', '421924030782791680', '422015023175966720', '422142839985041408', '422332662851051520', '422512738209136640', '422655518323515392', '423946733652307968', '424211919210577920', '423895378803834880', '424916520289198080', '424991204766679040', '425334093287395328', '425399570408173568', '425827235426103296', '425420367117942785', '426045986482692096', '426220976435888128', '426275859969114112', '426784479219564544', '427692637877829632', '428727944476098560', '428937325762990080', '429023742048489474', '427361637280935936', '428273361874350080', '429331875765972992', '426847731790127106', '426882992976719872', '426946586514444288', '426972558538203136', '426995940449603585', '429662997158846464', '427167539161214976', '431849082358095872', '431874108037808128', '430699179984556032', '432582331598397441', '432004788813697024', '432058772128026624', '431068963699564544', '432737270991302656', '432927287735234560', '430124653504258048', '430368374229843968', '430403418117926912', '433228251201540096']
            tweets_per_cluster_all[cluster] += 1
            # if str(tweet_id) in tweets and item_id in items_stats and item_id in tweets_with_engagement_count and cluster == 2:
            #     print(tweets_with_engagement_count[item_id] / items_stats[item_id]['count'])
            if str(tweet_id) in tweets:
                tweets_per_cluster[cluster] += 1
                # engagement = 1
            if item_id in items_stats and items_stats[item_id]['count'] > 0 and item_id in tweets_with_engagement_count and cluster == 1 and tweets_with_engagement_count[item_id] / items_stats[item_id]['count'] > 0.05:
                engagement = 1
            if item_id in items_stats and items_stats[item_id]['count'] > 0 and item_id in tweets_with_engagement_count and cluster == 0 and tweets_with_engagement_count[item_id] / items_stats[item_id]['count'] > 0.1:
                engagement = 1
            if item_id in items_stats and items_stats[item_id]['count'] > 0 and item_id in tweets_with_engagement_count and cluster == 2 and tweets_with_engagement_count[item_id] / items_stats[item_id]['count'] > 0.2:
                engagement = 1
                # print str(tweets_with_engagement_count[item_id]) + ' ' + str(items_stats[item_id]['count']) + ' ' + str(tweets_with_engagement_count[item_id] / items_stats[item_id]['count'])
            # if user_id in users_stats and users_stats[user_id]['count'] > 0 and cluster == 0:
            #     print str(users_stats[user_id]['eng_count']) + ' ' + str(users_stats[user_id]['count'])
            #     if float(users_stats[user_id]['eng_count']) / float(users_stats[user_id]['count']) >= 0.9:
            #         engagement = 1
        solutions.append((user_id, tweet_id, engagement))
    print(tweets_per_cluster)
    print(tweets_per_cluster_all)
    # train_ids, train_features, train_labels = create_features(train, model_parameters)
    # X = train_features
    # Y = train_labels
    # logreg = linear_model.LogisticRegression(C=1e5)
    # logreg.fit(X, Y)
    # test_ids, test_features, _ = create_features(test, model_parameters, train=False)
    # Xtest = test_features
    # Z = logreg.predict(Xtest)
    # solutions = list()
    # i = 0
    # for entity in test_features:
    #     solutions.append((test_ids[i][0], test_ids[i][1], Z[i]))
    #     i += 1
    solutions = solution.sort_the_solution(solutions)
    solution.write_the_solution_file(solutions, '/Users/jwasilewski/RecSys2014/solution_logreg.dat')


def run_model_clustered_default(test, model_parameters, cluster):
    cluster_avg_engs = model_parameters['cluster_avg_engs']
    tweets_with_engagement_count = model_parameters['tweets_with_engagement_count']
    tweets_with_engagement_sum = model_parameters['tweets_with_engagement_sum']
    cluster_user_eng = model_parameters['cluster_user_eng']
    ip_clusters = model_parameters['ip_clusters']

    items_test_stats = dict()
    user_test_stats = dict()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = tweet['imdb_rating']
        if rating < 1:
            rating = 1

        if item_id in items_test_stats:
            items_test_stats[item_id]['count'] += 1.0
            items_test_stats[item_id]['ratings_count'][rating] += 1.0
        else:
            items_test_stats[item_id] = dict()
            items_test_stats[item_id]['count'] = 1.0
            items_test_stats[item_id]['ratings_count'] = dict()
            for r in range(10):
                items_test_stats[item_id]['ratings_count'][r + 1] = 0.0
            items_test_stats[item_id]['ratings_count'][rating] = 1.0

        if user_id in user_test_stats:
            user_test_stats[user_id]['count'] += 1.0
        else:
            user_test_stats[user_id] = dict()
            user_test_stats[user_id]['count'] = 1.0

    print('Clustering item popularity...')
    items_test_count = list()
    items_test_count_labels = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        items_test_count.append(items_test_stats[item_id]['count'])
        items_test_count_labels.append(item_id)

    # ------------

    i = 0
    print('Applying model...')
    solutions = list()
    solutions_debug = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])
        if rating < 1:
            rating = 1

        user_followers_count = int(tweet['user_followers_count'])
        user_statuses_count = int(tweet['user_statuses_count'])

        user_mentions_count = tweet['user_mentions_count']

        scraping_date = datetime.fromtimestamp(int(tweet['tweet_scraping_time']))
        tweet_date = datetime.strptime(tweet['tweet_created_at'], '%Y-%m-%d')
        tweet_age = (scraping_date - tweet_date).days

        ip_cluster = None
        if item_id in ip_clusters:
            ip_cluster = ip_clusters[item_id]


        cluster_base = 1.0 + 0.99 * log(cluster_avg_engs['eng_sum'] / cluster_avg_engs['eng_count'])

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

        if user_id in cluster_user_eng and cluster_user_eng[user_id]['eng_count'] > 0:
            cluster_coefficient = 1.031 + 0.26 * log(cluster_user_eng[user_id]['eng_sum'] / cluster_user_eng[user_id]['eng_count'])
        else:
            cluster_coefficient = 1.0

        item_popularity_cluster_none = 0
        item_popularity_cluster0 = 0
        item_popularity_cluster1 = 0
        item_popularity_cluster2 = 0
        item_popularity_cluster3 = 0
        item_popularity_cluster4 = 0

        if ip_cluster == 0:
            item_popularity_cluster0 = 1
        elif ip_cluster == 1:
            item_popularity_cluster1 = 1
        elif ip_cluster == 2:
            item_popularity_cluster2 = 1
        elif ip_cluster == 3:
            item_popularity_cluster3 = 1
        elif ip_cluster == 4:
            item_popularity_cluster4 = 1
        else:
            item_popularity_cluster_none = 1

        item_score = item_rating * cluster_base * engagement_coefficient * cluster_coefficient
        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 7
        engagement += 0 * item_popularity_cluster0 + 10 * item_popularity_cluster1 - 20 * item_popularity_cluster2 + 150 * item_popularity_cluster3 + 150 * item_popularity_cluster4 + 7 * item_popularity_cluster_none
        engagement += item_score
        engagement += 600 * user_mentions0
        engagement += 50 * user_mentions1
        engagement += 600 * tweet_is_retweet

        engagement = round(engagement)

        if not tweet_is_retweet:
            if tweet_age > 22:
                engagement = 0.0
            if user_followers_count < 10:
                engagement = 0.0
            if user_statuses_count < 40:
                engagement = 0.0
            if engagement <= 40:
                engagement = 0.0

        # ------------------
        solutions.append((user_id, tweet['tweet_id'], engagement))
        solutions_debug.append((user_id, tweet['tweet_id'], engagement, ''))

        if i % 100 == 0:
            print("Proccessed items %s..." % i)
        i += 1

    print('Sorting solution...')
    solutions = solution.sort_the_solution(solutions)

    print('Saving solution...')
    solution.write_the_solution_file_clustered(solutions, '/Users/jwasilewski/RecSys2014/solution_%s.dat' % str(cluster), cluster)


def run_model_0(test, model_parameters):
    cluster_user_eng = model_parameters['cluster_user_eng']
    items_had_engagement = model_parameters['items_had_engagement']
    cluster_avg_engs2 = model_parameters['cluster_avg_engs2']
    cluster_user_eng2 = model_parameters['cluster_user_eng2']

    solutions = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])
        user_mentions_count = tweet['user_mentions_count']

        cluster_base = 1.1 + 1.0 * log(cluster_avg_engs2['eng_sum'] / cluster_avg_engs2['eng_count'])

        if rating > 6:
            item_rating = 50 * rating
        elif rating < 2:
            item_rating = 490 * rating
        else:
            item_rating = 55 * rating

        if item_id in items_had_engagement:
            engagement_coefficient = 1.5# + 0.5 * log(items_mean_engagement[item_id])
        else:
            engagement_coefficient = 1.0

        if user_id in cluster_user_eng and cluster_user_eng[user_id]['eng_count'] > 0:
            cluster_coefficient = 1.5# + 1.0 * log(cluster_user_eng[user_id]['eng_sum'] / cluster_user_eng[user_id]['eng_count'])
        else:
            cluster_coefficient = 1.0

        item_score = item_rating * cluster_base * engagement_coefficient * cluster_coefficient
        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 0
        engagement += item_score
        engagement += 600 * user_mentions0
        engagement += 50 * user_mentions1
        engagement += 600 * tweet_is_retweet

        solutions.append((user_id, tweet['tweet_id'], engagement))
    return solutions


def run_model_1(test, model_parameters):
    cluster_user_eng = model_parameters['cluster_user_eng']
    ip_clusters = model_parameters['ip_clusters']
    items_had_engagement = model_parameters['items_had_engagement']
    cluster_avg_engs2 = model_parameters['cluster_avg_engs2']
    cluster_user_eng2 = model_parameters['cluster_user_eng2']

    solutions = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])

        user_followers_count = int(tweet['user_followers_count'])
        user_mentions_count = tweet['user_mentions_count']

        scraping_date = datetime.fromtimestamp(int(tweet['tweet_scraping_time']))
        tweet_date = datetime.strptime(tweet['tweet_created_at'], '%Y-%m-%d')
        tweet_age = (scraping_date - tweet_date).days

        ip_cluster = None
        if item_id in ip_clusters:
            ip_cluster = ip_clusters[item_id]

        cluster_base = 1.3 + 1.15 * log(cluster_avg_engs2['eng_sum'] / cluster_avg_engs2['eng_count'])

        if rating > 6:
            item_rating = 50 * rating
        elif rating < 2:
            item_rating = 495 * rating
        else:
            item_rating = 50 * rating

        if item_id in items_had_engagement:
            item_engagement_coefficient = 1.6# + 1.05 * log(items_mean_engagement[item_id])
        else:
            item_engagement_coefficient = 1.0

        if user_id in cluster_user_eng and cluster_user_eng[user_id]['eng_count'] > 0:
            cluster_coefficient = 1.6# + 0.7 * log(cluster_user_eng[user_id]['eng_sum'] / cluster_user_eng[user_id]['eng_count'])
        else:
            cluster_coefficient = 1.0

        item_popularity_cluster_none = 0
        item_popularity_cluster0 = 0
        item_popularity_cluster1 = 0
        item_popularity_cluster2 = 0
        item_popularity_cluster3 = 0
        item_popularity_cluster4 = 0

        if ip_cluster == 0:
            item_popularity_cluster0 = 1
        elif ip_cluster == 1:
            item_popularity_cluster1 = 1
        elif ip_cluster == 2:
            item_popularity_cluster2 = 1
        elif ip_cluster == 3:
            item_popularity_cluster3 = 1
        elif ip_cluster == 4:
            item_popularity_cluster4 = 1
        else:
            item_popularity_cluster_none = 1

        item_score = item_rating * cluster_base * item_engagement_coefficient * cluster_coefficient
        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 0
        engagement += item_score
        # engagement += 0 * item_popularity_cluster0 \
        #               + 10 * item_popularity_cluster1 \
        #               - 10 * item_popularity_cluster2 \
        #               + 20 * item_popularity_cluster3 \
        #               + 15 * item_popularity_cluster4 \
        #               + 10 * item_popularity_cluster_none
        engagement += 600 * user_mentions0
        engagement += 50 * user_mentions1
        engagement += 600 * tweet_is_retweet

        if not tweet_is_retweet:
            if tweet_age > 22:
                engagement = 0.0
            if user_followers_count < 10:
                engagement = 0.0

        solutions.append((user_id, tweet['tweet_id'], engagement))

    return solutions


def run_model_2(test, model_parameters):
    cluster_user_eng = model_parameters['cluster_user_eng']
    ip_clusters = model_parameters['ip_clusters']
    items_had_engagement = model_parameters['items_had_engagement']
    cluster_avg_engs2 = model_parameters['cluster_avg_engs2']
    cluster_user_eng2 = model_parameters['cluster_user_eng2']

    solutions = list()
    for tweet in test:
        item_id = tweet['imdb_item_id']
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])
        user_mentions_count = tweet['user_mentions_count']

        ip_cluster = None
        if item_id in ip_clusters:
            ip_cluster = ip_clusters[item_id]

        cluster_base = 1.6 + 1.3 * log(cluster_avg_engs2['eng_sum'] / cluster_avg_engs2['eng_count'])

        if rating > 6:
            item_rating = 45 * rating
        elif rating < 2:
            item_rating = 490 * rating
        else:
            item_rating = 55 * rating

        if item_id in items_had_engagement:
            engagement_coefficient = 2.0# + 1.2 * log(items_mean_engagement[item_id])
        else:
            engagement_coefficient = 1.0

        if user_id in cluster_user_eng and cluster_user_eng[user_id]['eng_count'] > 0:
            cluster_coefficient = 1.6# + 1.05 * log(cluster_user_eng[user_id]['eng_sum'] / cluster_user_eng[user_id]['eng_count'])
        else:
            cluster_coefficient = 1.0

        item_popularity_cluster_none = 0
        item_popularity_cluster0 = 0
        item_popularity_cluster1 = 0
        item_popularity_cluster2 = 0
        item_popularity_cluster3 = 0
        item_popularity_cluster4 = 0

        if ip_cluster == 0:
            item_popularity_cluster0 = 1
        elif ip_cluster == 1:
            item_popularity_cluster1 = 1
        elif ip_cluster == 2:
            item_popularity_cluster2 = 1
        elif ip_cluster == 3:
            item_popularity_cluster3 = 1
        elif ip_cluster == 4:
            item_popularity_cluster4 = 1
        else:
            item_popularity_cluster_none = 1

        item_score = item_rating * cluster_base * engagement_coefficient * cluster_coefficient
        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 0
        engagement += item_score
        # engagement += 0 * item_popularity_cluster0 \
        #               + 10 * item_popularity_cluster1 \
        #               - 10 * item_popularity_cluster2 \
        #               + 20 * item_popularity_cluster3 \
        #               + 15 * item_popularity_cluster4 \
        #               + 10 * item_popularity_cluster_none
        engagement += 600 * user_mentions0
        engagement += 50 * user_mentions1
        engagement += 600 * tweet_is_retweet

        solutions.append((user_id, tweet['tweet_id'], engagement))
    return solutions


def run_model_new(test):
    solutions = list()
    for tweet in test:
        user_id = tweet['user_id']
        rating = float(tweet['imdb_rating'])
        user_mentions_count = tweet['user_mentions_count']

        if rating > 6:
            item_rating = 100 * rating
        elif rating < 2:
            item_rating = 400 * rating
        else:
            item_rating = 100 * rating

        tweet_is_retweet = int(True == tweet['tweet_is_retweet'])
        user_mentions0 = int(user_mentions_count > 0)
        user_mentions1 = int(user_mentions_count > 1)

        engagement = 0
        engagement += item_rating
        engagement += 600 * user_mentions0
        engagement += 50 * user_mentions1
        engagement += 600 * tweet_is_retweet

        solutions.append((user_id, tweet['tweet_id'], engagement))
    return solutions


def run_model_clustered(train, test, model_parameters_all):
    clusters = model_parameters_all['clusters']
    tweets_train_0 = list()
    tweets_train_1 = list()
    tweets_train_2 = list()
    tweets_0 = list()
    tweets_1 = list()
    tweets_2 = list()
    tweets_new = list()
    for tweet in train:
        item_id = tweet['imdb_item_id']
        if item_id in clusters:
            cluster = clusters[item_id]
            if cluster == 0:
                tweets_train_0.append(tweet)
            elif cluster == 1:
                tweets_train_1.append(tweet)
            elif cluster == 2:
                tweets_train_2.append(tweet)
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

    model_parameters_0 = statistics.compute_statistics_0(tweets_0, tweets_train_0)
    model_parameters_1 = statistics.compute_statistics_0(tweets_1, tweets_train_1)
    model_parameters_2 = statistics.compute_statistics_0(tweets_2, tweets_train_2)
    solutions_0 = run_model_0(tweets_0, model_parameters_0)
    solutions_1 = run_model_1(tweets_1, model_parameters_1)
    solutions_2 = run_model_2(tweets_2, model_parameters_2)
    solutions_new = run_model_new(tweets_new)

    sol = list()
    for (user_id, tweet_id, engagement) in solutions_0:
        sol.append((user_id, tweet_id, 1.0 * engagement))
    for (user_id, tweet_id, engagement) in solutions_1:
        sol.append((user_id, tweet_id, 1.0 * engagement))
    for (user_id, tweet_id, engagement) in solutions_2:
        sol.append((user_id, tweet_id, 1.0 * engagement))
    for (user_id, tweet_id, engagement) in solutions_new:
        sol.append((user_id, tweet_id, 1.0 * engagement))
    sol = solution.sort_the_solution(sol)
    solution.write_the_solution_file(sol, '/Users/jwasilewski/RecSys2014/solution.dat')


def run_model_clustered_debug(train, test, model_parameters_all):
    clusters = model_parameters_all['clusters']
    tweets_train_1 = list()
    tweets_1 = list()
    len()
    for tweet in train:
        item_id = tweet['imdb_item_id']
        if item_id in clusters:
            cluster = clusters[item_id]
            if cluster == 1:
                tweets_train_1.append(tweet)
    for tweet in test:
        item_id = tweet['imdb_item_id']
        if item_id in clusters:
            cluster = clusters[item_id]
            if cluster == 1:
                tweets_1.append(tweet)

    model_parameters_1 = statistics.compute_statistics_0(tweets_train_1)
    solutions_1 = run_model_1(tweets_1, model_parameters_1)

    solutions_1 = solution.sort_the_solution(solutions_1)
    solution.write_the_solution_file_clustered(solutions_1, '/Users/jwasilewski/RecSys2014/solution_1.dat', '1')