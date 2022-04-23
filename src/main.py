import json
import os
import random
from argparse import ArgumentParser

# from quiz_c2e import Quiz_c2e
# from quiz_e2c import Quiz_e2c
from quiz import Quiz

def check_score(correct, wrong):
    return (correct / (correct + wrong)) * 100

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--n", help="number of questions.", default=5, type=int)
    parser.add_argument("--mode", help="mode of quiz. c2e for chinese to english, e2c for english to chinese.", default='c2e', type=str)
    parser.add_argument("--filename", help="the filename of the vocabulary.", default='vocabs.json')
    parser.add_argument("--save_penalty", help="whether to save the wrong vocabs in this quiz.", action='store_true')
    parser.add_argument("--scope", help="the vocab scope is based on the date of storage", default=None)
    args = parser.parse_args()

    n = args.n
    mode = args.mode
    filename = args.filename
    save_penalty = args.save_penalty
    scope = args.scope

    meta_path = "../data/meta"
    with open(os.path.join(meta_path, filename)) as f:
        vocabs = json.load(f)

    if scope is not None:
        vocabs = {key:value for key, value in vocabs.items() if value['date'] == scope}
        if len(vocabs) == 0:
            raise ValueError('Your vocabulary in "%s" is empty'%scope)

    quiz = Quiz(vocabs, mode, save_penalty=save_penalty)
    for i in range(n):
        quiz.generate_question()
    score = check_score(quiz.correct, quiz.wrong)
    print('\nYour Score: %d'%score)

    if save_penalty:
        # save the dictionary json
        with open(filename, 'w') as outfile:
            json.dump(vocabs, outfile, indent=4)