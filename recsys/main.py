import dataset
import model
import numpy as np
import solution
import statistics


def run(tweets_train, tweets_test, evaluation=False, retweets=True, k=3):
    reload(statistics)

    print('Computing features...')
    stats = statistics.compute_statistics(tweets_train, tweets_test, k=k)
    train_features, train_labels = statistics.prepare_train_features(tweets_train, stats, retweets)
    test_features = statistics.prepare_test_features(tweets_test, stats, retweets)

    if evaluation:
        np.savetxt('eval_train_features.csv', train_features, delimiter=",")
        np.savetxt('eval_train_labels.csv', train_labels, delimiter=",")
        np.savetxt('eval_test_features.csv', test_features, delimiter=",")
    else:
        np.savetxt('train_features.csv', train_features, delimiter=",")
        np.savetxt('train_labels.csv', train_labels, delimiter=",")
        np.savetxt('test_features.csv', test_features, delimiter=",")

    print('Learning model...')
    lr_model = model.learn_model(train_features, train_labels)
    probabilities = model.apply_model(test_features, lr_model)

    print('Preparing solution...')
    if evaluation:
        solution.prepare_solutions_for_evaluation(tweets_test, probabilities[:, 0])
    else:
        solution.prepare_solutions(tweets_test, probabilities[:, 0])


if __name__ == "__main__":
    evaluation = False

    print('Loading datasets...')
    if evaluation:
        tweets_train, tweets_test = dataset.read_evaluation_datasets()
    else:
        tweets_train, tweets_test = dataset.read_datasets()
    run(tweets_train, tweets_test)
