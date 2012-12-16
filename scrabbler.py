#!/usr/bin/env python

# Note: requires python 2.7 for argparse and nicer dictionary generator syntax {k:v for (k, v) in [..]}

import sys, itertools, argparse, re
from operator import itemgetter

SCORES = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
          "x": 8, "z": 10, "_": 0}

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# Note: First I had load_dict return a list of words that in the dictionary
# Obviously that was horrifically slow as valid_words was doing an O(n) linear
# search for each word. Switching it to using a set (which i assume internally is
# implemented as a hash table) vastly improved things (yay O(1) lookups :)
def load_dict(dictfile):
    """Load the given dictionary file---strip and lowercase each line, and insert it into the resulting set"""
    try:
        f = open(dictfile, 'r')
        d = set()
        for line in f.readlines():
            d.add(line.strip().lower())
        return d
    except IOError as e:
        print "Failed to open word list: %s" % dictfile
        exit(1)

def permutations(chars):
    """Returns the permutations of the given set of characters, one by one"""
    for i in reversed(xrange(1, len(chars) + 1)):
        perms = itertools.permutations(chars, i)
        for perm in perms:
            yield "".join(perm)

def score_word(word):
    "Returns a score for the word"
    return sum([SCORES[c.lower()] for c in word])

def expand_blanks(word):
    """Recursively generate a list of expanded blanks---a list of all permutations possible
    when replacing an _ by any character in the alphabet"""
    if not '_' in word:
        return [word]
    expanded = []
    for i in xrange(len(word)):
        if word[i] == '_':
            w = [word[:i] + c + word[i+1:] for c in ALPHABET]
            for word in w:
                expanded.extend(expand_blanks(word))
    return expanded

def in_wordlist(word, wordlist):
    """Returns a truthy value if the word is in the wordlist. If the word has one or more wildcards,
    this will return a list of all words that match the word list. If there is no wildcard, returns an
    empty list."""
    if '_' in word:
        found = []
        expanded = expand_blanks(word)
        for expanded_word in expanded:
            if expanded_word in wordlist:
                found.append(expanded_word)
        return found
    else:
        if word in wordlist:
            return [word]
        else:
            return []

def sorted_scored_words(chars, wordlist):
    """Returns a list of tuples (word, score) of valid scrabble words from a set of scrabble characters.
    The tuples are sorted in descending order, highest score first"""
    # Generate a dictionary of {word: score} pairs to eliminate duplicate words
    # Then sort the dictionary by value, converting the dict to a list of tuples and sorting by the second item
    scores = {}
    for permutation in permutations(chars):
        words = in_wordlist(permutation, wordlist) # Handle the fact that blanks might generate a lot of potential matching words
        for word in words:
            scores[word] = score_word(word)
    return sorted(scores.iteritems(), key=itemgetter(1), reverse=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A scrabble solver program')
    parser.add_argument("characters", help="The scrabble characters to use")
    parser.add_argument('--dict', action="store", default="sowpods.txt", metavar="wordlist", type=str, help="A user-supplied word list file")
    p = parser.parse_args()
    chars = p.characters.lower()

    wordlist = load_dict(p.dict)

    words = sorted_scored_words(chars, wordlist)
    print "Got number of words: %s" % len(words)
    for word, score in words:
        print "%s %s" % (score, word)