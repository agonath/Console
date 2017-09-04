import sys
import os
#import signal # for later usage
import string
#import urwid # -> Graphic Console
from consoleCommand import Command
from loader import XLoader

CONSOLE_VERSION = (0, 0, 3)
DEBUG = False


# Console class
class Console(object):
    
    __slots__ = ["args", "prompt_messages", "history", "builtinCommandList", "commandList", "version", "lastResult", "lineCounter", "running", "saveOut", "saveIn", "saveError", "maxThreadCount", "width", "height"]
    
    def __init__(self, _args, _stdout=sys.stdout, _stdin=sys.stdin, _stderror=sys.stderr):
        self.args = _args
        self.history = {}
        self.lineCounter = 0
        self.commandList = {}  # List of registred commands (class Command)
        self.builtinCommandList = {} # List of basic built in commands
        self.lastResult = str()
        self.version = str(CONSOLE_VERSION[0]) + "." + str(CONSOLE_VERSION[1]) + "." + str(CONSOLE_VERSION[2])
        self.running = True
        self.prompt_messages = {"READY":"READY.\n", "ERROR_CMD":"Command <{0}> doesn't seems to exists.\n", "ERROR":"ERROR-> {0}\n"} # replace with json file
        self.maxThreadCount = os.cpu_count()
        try:
            self.width, self.height = os.get_terminal_size()
        except Exception as e:
            print(e)
        
        # save the system streams
        self.saveOut = sys.stdout
        self.saveIn = sys.stdin
        self.saveError = sys.stderr
        # set std streams, defaults to system values
        sys.stdout = _stdout
        sys.stdin = _stdin
        sys.stderr = _stderror

        

    def __del__(self):
        # restore system streams
        sys.stdout = self.saveOut
        sys.stdin = self.saveIn
        sys.stderr = self.saveError
        


    # --- Console core functions ----

    #
    # Register a command
    #
    # _commandName -> Name of command to be registered
    # _class -> Class name of instance of "Command" class
    # _module -> Python file name
    # _path -> Path to module
    #
    # Example: < console.registerCommand(_commandName="Hello2", _path="..\\bin\Plugins\\Commands", _module="Hello_World2.pyc", _class="Hello_World2") >
    #
    def registerCommand(self, *, _commandName, _class, _module, _path):
        
        load = XLoader() 
        # try to create the class object
        myClass = load.load_ModuleAndGetClass(_className=_class, _moduleName=_module, _path=_path)
        myCommand = myClass(_name=_commandName, _console=self)
        
        try:
            if(isinstance(myCommand, Command)):
                    self.commandList[_commandName] = myCommand
                    #print("Command {0} loaded...".format(_commandName))
                    return True

            self.errorMsg(myCommand)
            return False
        
        except Exception as e:
            self.errorMsg(e)
            return False

    #
    # Print error messages.
    #
    def errorMsg(self, _msg):
        sys.stderr.write(self.prompt_messages["ERROR"].format(_msg))

    #
    # Print text to current console stdout stream. (faster than print...)
    #
    def printMsg(self, _msg):
        sys.stdout.write(str(_msg))

    #
    # Print HTML formatted text to console.
    # Just some HTML-Tags are supported. (<br>, <b>, <p>...)
    #
    # TODO
    def printHtmlMsg(self, _htmlMsg):
        result = ""
        pass

    #
    # Start the console
    #
    def consoleStart(self, *, _listofCommands=[], _introMessage=""):
        # Intro text....
        if(_introMessage != ""):
            self.printMsg(_introMessage + str("\n"))
        else:
            # Console version
            self.printMsg(str("Version ") + self.version + str(" - "))
            self.printMsg(str(sys.getallocatedblocks()) + str(" Memory blocks used - "))
            self.printMsg(str("Number of CPU cores ") + str(os.cpu_count()) + str("\n"))
            self.printMsg(str("Current user is ") + str(os.getlogin()) + str("\n\n"))
            

        # Register basic built in commands
        self.builtinCommandList["exit"] = self.command_exit
        self.builtinCommandList["version"] = self.command_version
        self.builtinCommandList["help"] = self.command_help

                                      
    #
    # The console loop
    #
    # TODO: Replace by an more functional version with curses like display output.
    #
    def consoleLoop(self):
        # used vars 
        line = str()
        cmd = str()
        sep = str()
        parameters = str()
        
        # Console start
        self.consoleStart()

        while(self.running==True):
            
            # read input until '\n'
            line = input(self.prompt_messages["READY"])

            # update history and counter
            self.history[self.lineCounter] = line
            self.lineCounter += 1
                
            # split line into command and parameter
            cmd, sep, parameters = line.partition(' ')

            #Debug info if enabled
            if(DEBUG):
                for x in self.history:
                    self.printMsg("History-Entry No.: " + str(x) + " - " + str(self.history[x]))


            # try to find the command and excute it
            if(0 < len(cmd)):
                self.parseExecute(cmd, parameters)
            
    
    #
    # Find and excute an command
    #
    def parseExecute(self, _command, _parameters):

        if(DEBUG):
            self.printMsg("Command: ", _command)
            self.printMsg("Parameters: ", _parameters)

        # Handle the built in functions if needed
        try:
            self.builtinCommandList[_command.lower()](_parameters)
            return
        except LookupError:
            # Handle the registred commands
            try:
                self.commandList[_command].before(_parameters)
                self.commandList[_command].execute(_parameters)
                self.commandList[_command].after(_parameters)
            except LookupError:
                self.errorMsg(self.prompt_messages["ERROR_CMD"].format(_command))


  
         

    ### Built in console commands -----------------

    # Exit
    def command_exit(self, _parameter):
        self.running = False
        return True

    # Print version
    def command_version(self, _parameter):
        print(self.version)
        return True

    # Help on commands
    def command_help(self, _parameter=""):
        # Help with parameter called
        if(len(_parameter) > 0):
            # basic command
            if(_parameter in self.builtinCommandList.keys()):
                self.printMsg("help xxx -> Get help on command 'xxx'.\n"
                      "version -> Display version of console.\n"
                      "exit -> Quits console.\n")
                return True
            # registered commands
            elif(_parameter in self.commandList.keys()):
                self.commandList[_parameter.lower()].help(_parameter)
                return True
            else:
                # unknown command
                self.errorMsg(self.prompt_messages["ERROR_CMD"].format(_parameter))
                return False 
        else:
            # Help without parameters called.
            # --> Just print out all commands and basic commands.
            self.printMsg("help xxx -> Get help on command 'xxx'.\n"
                  "version -> Display version of console.\n"
                  "exit -> Quits console.\n")

            for item in self.commandList.keys():
                print(str(item) + str(" ->"), end=" ")
                self.commandList[item].helpShort(_parameter)
            return True