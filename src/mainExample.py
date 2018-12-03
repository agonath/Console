import sys
import os
from console import Console


#
# Start console and register some commands.
#
def main(args):
    con = Console(args)
      
    # try to register a command
    print(str(".." + os.sep + "src" + os.sep + "Commands"))
    con.registerCommand(_commandName="Hello1", _class="Hello_World1", _module="Hello_World1", _path=str(".." + os.sep + "src" + os.sep + "Commands"))
    
    # ...path points to another folder
    con.registerCommand(_commandName="Hello2", _path="..\\bin\Plugins\\Commands", _module="Hello_World2.pyc", _class="Hello_World2")
    
    con.consoleLoop();



if __name__ == '__main__':
    main(sys.argv[1:])
