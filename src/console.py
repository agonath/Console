import sys
import os
#import signal # for later usage
import string
from consoleCommand import Command

CONSOLE_VERSION = (0, 0, 1)
DEBUG = False


# Console class
class Console(object):
    
    __slots__ = ["prompt_messages", "history", "basicCommandList", "commandList", "version", "lastResult", "lineCounter", "running", "oldStdout", "oldStdin", "oldStderror"]
    
    def __init__(self, _args):
        self.history = {}
        self.lineCounter = 0
        self.commandList = {}  # List of registred commands (class Command)
        self.basicCommandList = {} # List of basic built in commands
        self.lastResult = str()
        self.version = str(CONSOLE_VERSION[0]) + "." + str(CONSOLE_VERSION[1]) + "." + str(CONSOLE_VERSION[2])
        self.running = True
        self.prompt_messages = {"READY":"READY.\n", "ERROR_CMD":"ERROR-> Command <{0}> doesn't seems to exists.\n"} # replace with json file
        # save the system standard in, out, error streams
        self.oldStdout = sys.stdout;
        self.oldStdin = sys.stdin;
        self.oldStderror = sys.stderr;

        

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
                    print("History-Entry No.: " + str(x) + " - " + str(self.history[x]))


            # try to find the command and excute it
            if(0 < len(cmd)):
                self.parseExecute(cmd, parameters)
            
    
    #
    # Find and excute an command
    #
    def parseExecute(self, _command, _parameters):

        if(DEBUG):
            print("Command: ", _command)
            print("Parameters: ", _parameters)

        # Handle the built in functions if needed
        try:
            self.basicCommandList[_command.lower()](_parameters)
            return
        except:
            # Handle the registred commands
            try:
                self.commandList[_command.lower()].before(_parameters)
                self.commandList[_command.lower()].execute(_parameters)
                self.commandList[_command.lower()].after(_parameters)
            except:
                print(self.prompt_messages["ERROR_CMD"].format(_command), file=sys.stderr)


  
         

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
    def command_help(self, _parameter):
        # Help with parameter called
        if(len(_parameter) > 0):
            try:
                if(_parameter in self.basicCommandList.keys()):
                    print("help xxx -> Get help on command 'xxx'.\n"
                          "version -> Display version of console.\n"
                          "exit -> Quits console.\n")
                    return True
                else:
                    self.commandList[_parameter.lower()].help(_parameter)
                    return True
            except:
                print(self.prompt_messages["ERROR_CMD"].format(_parameter), file=sys.stderr)
                return False 
        else:
            # Help without parameters called.
            # --> Just print out all commands and basic commands.
            print("Hier!!!")
            print("help xxx -> Get help on command 'xxx'.\n"
                  "version -> Display version of console.\n"
                  "exit -> Quits console.")

            for item in self.commandList:
                print(str("\"{0}\" -> .\n").format(item))# --> {1}.\n").format(item, str(self.commandList[item].help(""))))
            return True