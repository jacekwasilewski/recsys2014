from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np


def learn_model(train_features, train_labels):
    X = StandardScaler().fit_transform(train_features)
    y = np.ravel(train_labels)

    model = LogisticRegression()
    return model.fit(X, y)


def apply_model(test_features, model):
    """
    :param test_features:
    :param LogisticRegression model: Model
    :return:
    """
    X = StandardScaler().fit_transform(test_features)
    return model.predict_proba(X)