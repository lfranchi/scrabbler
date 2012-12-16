# Scrabble cheater

Small program to generate scrabble words and points from a scrabble rack

Write a Python script that takes a Scrabble rack as a command-line
argument and prints all valid Scrabble words that can be constructed
from that rack using the official SOWPODS Scrabble word list, along
with their Scrabble scores, sorted by score.

===

## Optimizations

Solving rows with two blank tiles is really slow. Time shows (after 2 to warm up my caches):

    ./scrabbler.py _AEFIE_  9.61s user 0.10s system 80% cpu 12.078 total
    ./scrabbler.py _AEFIE_  9.47s user 0.07s system 67% cpu 14.110 total
    ./scrabbler.py _AEFIE_  9.94s user 0.07s system 61% cpu 16.163 total
    ./scrabbler.py _AEFIE_  9.48s user 0.06s system 97% cpu 9.747 total

So it needs to be faster :) Running it through cProfile and visualizating it with RunSnakeRun (the closest thing i've found to KCacheGrind, my favorite profile visualization tool) showed this:

![profile output](http://files.lfranchi.com/scrabbler_profiler_1.png)

Which shows that first, expand_blanks is the really slow function, and second, that there are a *ton* of calls to array.extend. I figured I could eliminate one recursive case by making the second-to-last recursion check for it in advance:

    for word in w:
        if not '_' in word:
            expanded.append(word)
        else:
            expanded.extend(expand_blanks(word))

And see if that helps:

    ./scrabbler.py _AEFIE_  7.08s user 0.08s system 79% cpu 8.958 total
    ./scrabbler.py _AEFIE_  7.04s user 0.07s system 76% cpu 9.278 total
    ./scrabbler.py _AEFIE_  7.16s user 0.12s system 49% cpu 14.818 total
    ./scrabbler.py _AEFIE_  7.09s user 0.08s system 71% cpu 10.050 total

Which is already quite a nice improvement :)