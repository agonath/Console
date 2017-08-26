import sys
import os
from console import Console
from loader import systemLoader


# Test-Command
"""
class Hello_World(Command):

    def execute(self, _parameters):
        print("Hello World!")
        return super().execute(_parameters)

    def helpShort(self, _parameters):
        print("Prints Hello World.")

    def help(self, _parameters):
        print("Prints Hello World.")
"""
#
# Start console
#
def main(args):
    con = Console(args)
   # hello = Hello_World(_name="hello", _console=con)
    
    load = systemLoader() 
    # try to create the class object
    newClass = load.loadClassFromModule(_className="Hello_World", _moduleName="Commands")
    hello = newClass(_name="hello", _console=con)
    # register the command...
    con.registerCommand(hello)
    
    
    con.consoleLoop();



if __name__ == '__main__':
    main(sys.argv[1:])
