TRAIN = """
Train a generator on a corpus.

train <n> [--noparagraphs] <path> ...

Discard the current generator, and train a new generator on the given paths.
Wildcards are allowed.

<n> is the length of prefix (producing <n+1>-grams). If the 'noparagraphs'
option is given, paragraph breaks are treated as spaces and discarded, rather
than a separate token.
"""

LOAD = """
Load a generator from disk.

load <file>

Discard the current generator, and load the trained generator in the given
file.
"""

DUMP = """
Save a generator to disk.

dump <file>

Save the trained generator to the given file.
"""

HELP = """
exit
Exit markov
"""

GENERATORS = """
Generate a sequence of output:

generator <len> [--seed=<seed>] [--prob=<prob>] [--offset=<offset>] [--] [<prefix>...]

<len> is the length of the sequence

<seed> is the optional random seed. If no seed is given, the current system time is used

<prob> is the probability of random token choice. The default value for <prob>
is 0. If an offset is give, drop that many tokens from the start of the
output. The optional prefix is used to see the generator with tokens. A
prefix of length longer than the generator's n will be truncated.
"""

TOKENS = """
Generate tokens of output. See 'help generators'.
"""

PARAGRAPHS = """
Generate paragraphs of output. See 'help generators'.
"""

EXIT = """
Exit the REPL
"""

CONTINUE = """
Continue generating output.

continue [<len>]
"""

SENTENCES = """
Generate sentences of output. See 'help generators'.
"""