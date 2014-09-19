import dataset
import model
import numpy as np
import solution
import statistics


def run(tweets_train, tweets_test):
    reload(statistics)

    print('Computing features...')
    train_features, train_labels, test_features = statistics.compute_features(tweets_train, tweets_test)
    np.savetxt('/Users/jwasilewski/RecSys2014/train_features.csv', train_features, delimiter=",")
    np.savetxt('/Users/jwasilewski/RecSys2014/train_labels.csv', train_labels, delimiter=",")
    np.savetxt('/Users/jwasilewski/RecSys2014/test_features.csv', test_features, delimiter=",")

    print('Learning model...')
    lr_model = model.learn_model(train_features, train_labels)
    probabilities = model.apply_model(test_features, lr_model)

    print('Preparing solution...')
    solution.prepare_solutions(tweets_test, probabilities[:, 0])


if __name__ == "__main__2":
    print('Loading datasets...')
    tweets_train, tweets_test = dataset.read_datasets()
    run(tweets_train, tweets_test)


if __name__ == "__main__":
    print('Loading datasets...')
    tweets_train, tweets_test = dataset.read_evaluation_datasets()

    print('Computing features...')
    train_features, train_labels, test_features = statistics.compute_features(tweets_train, tweets_test)
    np.savetxt('/Users/jwasilewski/RecSys2014/eval_train_features.csv', train_features, delimiter=",")
    np.savetxt('/Users/jwasilewski/RecSys2014/eval_train_labels.csv', train_labels, delimiter=",")
    np.savetxt('/Users/jwasilewski/RecSys2014/eval_test_features.csv', test_features, delimiter=",")

    print('Learning model...')
    lr_model = model.learn_model(train_features, train_labels)
    probabilities = model.apply_model(test_features, lr_model)

    print('Preparing solution...')
    solution.prepare_solutions_for_evaluation(tweets_test, probabilities[:, 0])