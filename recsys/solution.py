import sys
import subprocess


def read_solution(the_solution_file):
    solutions = list()
    header = True
    min = sys.float_info.max
    max = sys.float_info.min
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
            if engagement > max:
                max = engagement
            if engagement < min:
                min = engagement
    return solutions, min, max


def write_the_solution_file(solutions, the_solution_file):
    lines = list()
    lines.append('userid,tweetid,engagement' + '\n')

    for (user, tweet, engagement) in solutions:
        line = str(user) + ',' + str(tweet) + ',' + str(engagement) + '\n'
        lines.append(line)

    with file(the_solution_file, 'w') as outfile:
        outfile.writelines(lines)

    p = subprocess.Popen('java -jar /Users/jwasilewski/RecSys2014/rscevaluator-0.14-jar-with-dependencies.jar /Users/jwasilewski/RecSys2014/test_solution.dat %s' % the_solution_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line)
    p.wait()

def write_the_solution_file_debug(solutions, the_solution_file):
    lines = list()
    lines.append('userid,tweetid,engagement' + '\n')

    for (user, tweet, engagement, a, b, c, d) in solutions:
        line = str(user) + ',' + str(tweet) + ',' + str(engagement) + ',' + str(a) + ',' + str(b) + ',' + str(c) + ',' + str(d) + '\n'
        lines.append(line)

    with file(the_solution_file, 'w') as outfile:
        outfile.writelines(lines)


def sort_the_solution(solutions):
    return sorted(solutions, key=lambda data: (-int(data[0]), -int(data[2]), -int(data[1])))