import json
import os
import random
import numpy as np


class Quiz():
    def __init__(self, vocabs, mode, num_option=4, seed=0, save_penalty=False):
        self.vocabs = vocabs
        self.mode = mode
        self.vocab_list = list(vocabs.keys())
        self.meta_list = [vocabs[key] for key in self.vocab_list]
        self.vocabs_len = len(self.vocabs)
        self.vocabs_index = [i for i in range(self.vocabs_len)]
        self.num_option = num_option
        self.seed = seed
        self.save_penalty = save_penalty
        self.correct = 0
        self.wrong = 0
        
    def generate_options_answer(self):
        # random.seed(0)
        self.options_index = np.random.randint(low=0, high=self.vocabs_len, size=self.num_option)
        self.options_vocab = [self.vocab_list[idx] for idx in self.options_index]
        self.options_meta = [self.meta_list[idx] for idx in self.options_index]

        self.options_vocab = []
        self.options_mean = []
        for idx in self.options_index:
            self.options_vocab.append(self.vocab_list[idx])
            self.options_mean.append(self.meta_list[idx]['mean'])

        self.answer_index = random.randint(0, self.num_option-1)
        self.answer_vocab = self.options_vocab[self.answer_index]
        self.answer_mean = self.options_mean[self.answer_index]
        self.answer_proficiency = self.vocabs[self.answer_vocab]['proficiency']

    def enter_answer(self):
        isvalid = False
        while isvalid == False:
            self.input_answer = input('input your answer: ')
            if self.input_answer in [str(i+1) for i in range(self.num_option)]:
                self.input_answer = int(self.input_answer)-1
                isvalid = True
            else:
                print('Please enter the index [%d-%d]'%(0, self.num_option-1))
                continue

    def check_answer(self):
        if self.mode == 'e2c':
            input_answer = self.options_vocab[self.input_answer]
            correct_answer = self.answer_vocab
        elif self.mode == 'c2e':
            input_answer = self.options_mean[self.input_answer]
            correct_answer = self.answer_mean
        else:
            raise ValueError('Please select the correct mode (e2c or c2e)')
        
        print('Your Input is "%s"'%input_answer)
        print('The Correct Answer is "%s"'%correct_answer)
        if input_answer == correct_answer:
            self.correct += 1
            print('Correct !!!')
        else:
            self.wrong += 1
            if self.save_penalty:
                self.vocabs[self.answer_vocab]['proficiency'] += 1
            print('Wrong Answer')

    def generate_question(self):
        self.generate_options_answer()
        if self.mode == 'e2c':
            question = self.answer_mean
            options = self.options_vocab
        elif self.mode == 'c2e':
            question = self.answer_vocab
            options = self.options_mean
        print('\nQuestion:', question)
        for i in range(self.num_option):
            print('(%s) %s'%(i+1, options[i]))
        self.enter_answer()
        self.check_answer()