from .repl import Repl


def main():
    while True:
        try:
            Repl().cmdloop()
        except KeyboardInterrupt:
            print("^C")  # noqa
            continue
        break
