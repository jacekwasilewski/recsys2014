import random
import dataset
from recsys.solution import read_solution, sort_the_solution, write_the_solution_file
import statistics
from recsys import model


if __name__ == "__main__":
    print('Loading datasets...')
    tweets_train, tweets_test = dataset.read_datasets_sample()

    model_parameters = statistics.compute_statistics(tweets_train)

    model.run_model(tweets_train, tweets_test, model_parameters)
    # model.run_logreg(tweets_train, tweets_test, model_parameters)
    # solutions = read_solution('/Users/jwasilewski/RecSys2014/test_solution.dat')
    # new_solutions = list()
    # for (user_id, tweet_id, engagement) in solutions:
    #     if engagement > 0:
    #         new_solutions.append((user_id, tweet_id, 1.0))
    #     else:
    #         new_solutions.append((user_id, tweet_id, 0.0))
    #     if engagement > 0 and random.random() > 0.5:
    #         new_solutions.append((user_id, tweet_id, random.random()))
    #     else:
    #         new_solutions.append((user_id, tweet_id, 0))
    # new_solutions = sort_the_solution(new_solutions)
    # write_the_solution_file(new_solutions, '/Users/jwasilewski/RecSys2014/solutions_rand.dat')