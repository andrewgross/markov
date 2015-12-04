README
======

The program presents a REPL, from which you can generate text in a
number of different ways, a list of commands can be produced by typing
`help`, and help for specific topics can be found by typing `help
topic`.

Installation
---------------

```
pip install markov
```

Usage
-----

Text sources should be multiple plaintext files in a directory.


````
train 3 --noparagraphs /path/to/KingJamesProgramming/*
tokens 350
````



Warning: Termination
--------------------

The `paragraphs` and `sentences` generators may not terminate. Because
they generate blocks of text at a time, and a block only ends when a
specific token (such as a paragraph break) occurs, if the generator
gets stuck in a loop, the token may never come up.

One way to resolve this would be to have a loop detector, but I
haven't got around to doing this yet.
