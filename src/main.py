import sys
import os
from console import Console
from loader import SystemLoader


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
    
    load = SystemLoader() 
    # try to create the class object
    newClass = load.load_ModuleAndGetClass(_className="Hello_World", _moduleName="Hello_World", _path=str(".\\" + os.sep + "Commands"))
    hello = newClass(_name="hello", _console=con)
    # register the command...
    con.registerCommand(hello)

    newClass2 = load.load_ModuleAndGetClass(_path="..\\bin\Plugins\\Commands", _moduleName="Hello_World2.pyc", _className="Hello_World2")
    hello2 = newClass2(_name="hello2", _console=con)
    con.registerCommand(hello2)

    print(chr(0x2557))
    print(chr(0x2500))
    print(oct(0x2500))
    
    
    con.consoleLoop();



if __name__ == '__main__':
    main(sys.argv[1:])
