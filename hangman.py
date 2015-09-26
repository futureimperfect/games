#!/usr/bin/env python

import urllib3

from random import randint

MAX_WRONG_GUESSES = 6


class Words(object):

    def __init__(self):
        self.url = 'http://www.mieliestronk.com/corncob_lowercase.txt'
        self.words = self.httpGet(self.url).splitlines()

    def httpGet(self, url):
        return urllib3.PoolManager(
        ).request(
            'GET',
            url
        ).read()

    def getRandomWord(self):
        return self.words[randint(0, len(self.words) - 1)]


def print_hangman(fail_count=0):
    hmap = {
        '1': 'O',
        '2': '/',
        '3': '|',
        '4': '\\',
        '5': '/',
        '6': '\\',
    }
    for k, v in hmap.items():
        if int(k) > fail_count:
            hmap[k] = ' '
    hangman = '''
     ------
     |    |
     %(1)s    |
    %(2)s%(3)s%(4)s   |
    %(5)s %(6)s   |
    ''' % hmap
    print(hangman)


def play(words):
    r_word = words.getRandomWord()
    random_word = list(r_word)
    print("I've picked a random word. Can you guess what it is?")
    wrong_guesses = 0
    right_guesses = []
    while len(random_word) > 0 and wrong_guesses < MAX_WRONG_GUESSES:
        guess = raw_input('Enter your guess: ')
        while len(guess) > 1 or not guess.isalpha():
            guess = raw_input('Must be a single letter! Enter your guess: ')
        if guess in random_word:
            while guess in random_word:
                right_guesses.append(random_word.pop(random_word.index(guess)))
        else:
            wrong_guesses += 1
        print_hangman(fail_count=wrong_guesses)
        print(' '.join([w if w in right_guesses else '__' for w in r_word]))
    if len(random_word) == 0:
        print('You won! The winning word was {0}.'.format(r_word))
    else:
        print('Failwhale! The word you missed was {0}.'.format(r_word))
    response = raw_input('\nWould you like to play again? y/n ')
    while response not in ('y', 'Y', 'yes', 'n', 'N', 'no'):
        response = raw_input(
            'Please enter a valid response. Would you like to play again? y/n ')
    return True if response in ('y', 'Y', 'yes') else False


def main():
    print('Welcome to Hangman!\n')
    print('Building word list...\n\n')
    words = Words()
    while play(words):
        pass
    print('\nGoodbye!')


if __name__ == '__main__':
    main()
