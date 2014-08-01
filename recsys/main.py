import dataset
import statistics
from recsys import model


if __name__ == "__main__":
    print('Loading datasets...')
    tweets_train, tweets_test = dataset.read_datasets_sample()

    model_parameters = statistics.compute_statistics(tweets_train)

    model.run_model(tweets_test, model_parameters)