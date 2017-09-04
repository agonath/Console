import sys
import os

# Simple base class for a command
class Command(object):
    
    def __init__(self, *, _name, _console):
        self.name = _name           #Name of command
        self.console = _console     #Console object

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
