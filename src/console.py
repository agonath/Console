import sys
import importlib
import os
#import signal # for later usage
import string
#import urwid # -> Graphic Console
from consoleCommand import Command

CONSOLE_VERSION = (0, 0, 2)
DEBUG = False


# Console class
class Console(object):
    
    __slots__ = ["prompt_messages", "history", "basicCommandList", "commandList", "version", "lastResult", "lineCounter", "running", "stdOut", "stdIn", "stdError"]
    
    def __init__(self, _args, _stdout=sys.stdout, _stdin=sys.stdin, _stderror=sys.stderr):
        self.history = {}
        self.lineCounter = 0
        self.commandList = {}  # List of registred commands (class Command)
        self.basicCommandList = {} # List of basic built in commands
        self.lastResult = str()
        self.version = str(CONSOLE_VERSION[0]) + "." + str(CONSOLE_VERSION[1]) + "." + str(CONSOLE_VERSION[2])
        self.running = True
        self.prompt_messages = {"READY":"READY.\n", "ERROR_CMD":"Command <{0}> doesn't seems to exists.\n", "ERROR":"ERROR-> {0}\n"} # replace with json file
        
        # set std streams, defaults to system values
        self.stdOut = _stdout
        self.stdIn = _stdin
        self.stdError = _stderror

        

    def __del__(self):
        pass


    # --- Console core functions ----

    #
    # Register a command
    #
    def registerCommand(self, _comObject):
        try:
            if(isinstance(_comObject, Command)):
                    self.commandList[_comObject.name] = _comObject
                    return True
            return False
        except:
            return False

    #
    # Print error messages.
    #
    def errorMsg(self, _msg):
        self.stdError.write(self.prompt_messages["ERROR"].format(_msg))

    #
    # Print text to current console stdout stream.
    #
    def printMsg(self, _msg):
        self.stdOut.write(str(_msg))

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
            print(_introMessage)
        # Console version
        print(self.version)

        # Register basic built in commands
        self.basicCommandList["exit"] = self.command_exit
        self.basicCommandList["version"] = self.command_version
        self.basicCommandList["help"] = self.command_help

                                      
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
        self.consoleStart();
         
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
            self.basicCommandList[_command.lower()](_parameters)
            return
        except LookupError:
            # Handle the registred commands
            try:
                self.commandList[_command.lower()].before(_parameters)
                self.commandList[_command.lower()].execute(_parameters)
                self.commandList[_command.lower()].after(_parameters)
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
            if(_parameter in self.basicCommandList.keys()):
                self.printMsg("help xxx -> Get help on command 'xxx'.\n"
                      "version -> Display version of console.\n"
                      "exit -> Quits console.\n")
                return True
            # registered command
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
                  "exit -> Quits console.")

            for item in self.commandList.keys():
                print(str(item) + str(" ->"), end=" ")
                self.commandList[item].helpShort(_parameter)
            return True

    # TODO - load commands like plugins
    def loadCommandModule(self, *, _path="Commands\\", _name):
        if(len(_name) > 0):
            try:
                if(_path not in sys.path):
                    sys.path.append(_path)
                    print(sys.path)

                module = importlib.import_module(_name)
                self.printMsg("Imported Module: " + str(module))
                command = getattr(module, 'class')
                self.registerCommand(command)
                return command
            except Exception as e:
                self.printMsg("Error-> " + str(e))