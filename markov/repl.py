
import cmd
import shlex
import docopt
import os
import glob
import markovstate
import fileinput
import functools

import help_text
from helpers import print_help


def decorator_with_arguments(wrapper):
    return lambda *args, **kwargs: lambda func: wrapper(func, *args, **kwargs)


@decorator_with_arguments
def arg_wrapper(f, cmd, argstr="", types={}):
    @functools.wraps(f)
    def wrapper(self, line):
        try:
            args = docopt.docopt("usage: {} {}".format(cmd, argstr),
                                 argv=shlex.split(line),
                                 help=False)

            for k, v in types.items():
                try:
                    if k in args:
                        args[k] = v[1] if args[k] == [] else v[0](args[k])
                except:
                    args[k] = v[1]

            return f(self, args)
        except docopt.DocoptExit:
            print(cmd + " " + argstr)
    return wrapper


class Repl(cmd.Cmd, object):
    """
    REPL for Markov interaction. This is way overkill, yay!
    """

    def __init__(self):
        """
        Initialise a new REPL.
        """
        self.cmdqueue = []
        super(Repl, self).__init__()
        self.markov = markovstate.MarkovState()
        self.prompt = "markov> "

    def help_generators(self):
        print_help(help_text.GENERATORS)

    @arg_wrapper("tokens",
                 "<len> [--seed=<seed>] [--prob=<prob>] [--offset=<offset>] [--] [<prefix>...]",
                 {"<len>": (int,),
                  "--seed": (int, None),
                  "--prob": (float, 0),
                  "--offset": (int, 0),
                  "<prefix>": (tuple, ())})
    def do_tokens(self, args):

        try:
            print(self.markov.generate(args["<len>"], args["--seed"],
                                       args["--prob"], args["--offset"],
                                       prefix=args["<prefix>"]))
        except markovstate.MarkovStateError as e:
            print(e.value)

    def help_tokens(self):
        print_help(help_text.TOKENS)

    @arg_wrapper("paragraphs",
                 "<len> [--seed=<seed>] [--prob=<prob>] [--offset=<offset>] [--] [<prefix>...]",
                 {"<len>": (int,),
                  "--seed": (int, None),
                  "--prob": (float, 0),
                  "--offset": (int, 0),
                  "<prefix>": (tuple, ('\n\n',))})
    def do_paragraphs(self, args):
        try:
            print(self.markov.generate(args["<len>"], args["--seed"],
                                       args["--prob"], args["--offset"],
                                       endchunkf=lambda t: t == '\n\n',
                                       kill=1, prefix=args["<prefix>"]))
        except markovstate.MarkovStateError as e:
            print(e.value)

    def help_paragraphs(self):
        print_help(help_text.PARAGRAPHS)

    @arg_wrapper("sentences",
                 "<len> [--seed=<seed>] [--prob=<prob>] [--offset=<offset>] [--] [<prefix>...]",
                 {"<len>": (int,),
                  "--seed": (int, None),
                  "--prob": (float, 0),
                  "--offset": (int, 0),
                  "<prefix>": (tuple, ())})
    def do_sentences(self, args):
        sentence_token = lambda t: t[-1] in ".!?"
        try:
            print(self.markov.generate(args["<len>"], args["--seed"],
                                       args["--prob"], args["--offset"],
                                       startf=sentence_token,
                                       endchunkf=sentence_token,
                                       prefix=args["<prefix>"]))
        except markovstate.MarkovStateError as e:
            print(e.value)

    def help_sentences(self):
        print_help(help_text.SENTENCES)

    @arg_wrapper("continue", "[<len>]", {"<len>": (int, 1)})
    def do_continue(self, args):
        try:
            print(self.markov.more(args["<len>"]))
        except markovstate.MarkovStateError as e:
            print(e.value)

    def help_continue(self):
        print_help(help_text.CONTINUE)

    # Loading and saving data
    @arg_wrapper("train", "<n> [--noparagraphs] <path> ...", {"<n>": (int,)})
    def do_train(self, args):
        paths = [path
                 for ps in args["<path>"]
                 for path in glob.glob(os.path.expanduser(ps))]

        def charinput(paths):
            fi = fileinput.input(paths)
            for line in fi:
                for char in line:
                    yield char
            fi.close()

        self.markov.train(args["<n>"],
                          charinput(paths),
                          noparagraphs=args["--noparagraphs"])

    def help_train(self):
        print_help(help_text.TRAIN)

    @arg_wrapper("load", "<file>")
    def do_load(self, args):
        self.markov.load(args["<file>"])

    def help_load(self):
        print_help(help_text.LOAD)

    @arg_wrapper("dump", "<file>")
    def do_dump(self, args):
        try:
            self.markov.dump(args["<file>"])
        except markovstate.MarkovStateError as e:
            print(e.value)

    def help_dump(self):
        print_help(help_text.DUMP)

    def do_exit(self, line):
        return True

    def help_exit(self):
        print_help(help_text.EXIT)

    do_EOF = do_exit
