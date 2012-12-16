#!/usr/bin/env python

import sys, itertools
from operator import itemgetter

SCORES = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
          "x": 8, "z": 10}

# Note: First I had load_dict return a list of words that in the dictionary
# Obviously that was horrifically slow as valid_words was doing an O(n) linear
# search for each word. Switching it to using a set (which i assume internally is
# implemented as a hash table) vastly improved things (yay O(1) lookups :)
def load_dict(dictfile):
    f = open(dictfile, 'r')
    d = set()
    for line in f.readlines():
        d.add(line.strip().lower())
    return d

def permutations(chars):
    """Returns the permutations of the given set of characters, one by one"""
    for i in reversed(xrange(1, len(chars) + 1)):
        perms = itertools.permutations(chars, i)
        for perm in perms:
            yield "".join(perm)

def score_word(word):
    "Returns a score for the word"
    return sum([SCORES[c.lower()] for c in word])

def valid_words(chars, wordlist):
    """Returns a list of tuples (word, score) of valid scrabble words from a set of scrabble characters.
    The tuples are sorted in descending order, highest score first"""
    # Generate a dictionary of {word: score} pairs to eliminate duplicate words
    # Then sort the dictionary by value, converting the dict to a list of tuples and sorting by the second item
    return sorted({perm: score_word(perm) for perm in permutations(chars) if perm in wordlist}.iteritems(), key=itemgetter(1), reverse=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please call scrabbler with one argument, a list of characters to use"
        exit(0)

    chars = sys.argv[1].lower()
    if len(chars) != 7:
        print "Please only pass 7 characters, as a scrabble rack only has 7 tiles"
        exit(0)

    wordlist = load_dict("sowpods.txt")
    words = valid_words(chars, wordlist)
    print "Got number of words: %s" % len(words)
    for word, score in words:
        print "%s %s" % (score, word)