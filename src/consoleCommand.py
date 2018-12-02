import sys
import os

# Simple base class for a command
#
# - Added the module name. Needed for the "unregister" command. (Agonath)
#
class Command(object):
    
    def __init__(self, *, _name, _console, _moduleName):
        self.name = _name           # Name of command as string
        self.console = _console     # Console object, references the console itself
        self.moduleName = _moduleName        # corresponding module name as string

    def __del__(self):
        pass

    def before(self, _parameters):
        pass

    def execute(self, _parameters):
        pass

    def after(self, _parameters):
        pass

    def help(self, _parameters):
        pass

    def helpShort(self, _parameters):
        pass
