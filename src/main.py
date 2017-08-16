import sys
import os
from console import Console
from consoleCommand import Command

# Test-Command
class Hello_World(Command):

    def execute(self, _parameters):
        print("Hello World!")
        return super().execute(_parameters)

    def helpShort(self, _parameters):
        print("Prints Hello World.")

    def help(self, _parameters):
        print("Prints Hello World.")

#
# Start console
#
def main(args):
    con = Console(args)
    hello = Hello_World(_name="hello", _console=con)
    con.consoleLoop();



if __name__ == '__main__':
    main(sys.argv[1:])
