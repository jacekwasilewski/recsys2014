import dataset
from recsys import model


if __name__ == "__main__":
    tweets_train, tweets_test = dataset.read_datasets()
    model.run_model(tweets_train, tweets_test)