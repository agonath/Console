from consoleCommand import Command

# Test-Command
class Hello_World1(Command):

    def execute(self, _parameters):
        print("Hello World 1!")
        return super().execute(_parameters)

    def helpShort(self, _parameters):
        print("Prints Hello World 1.")

    def help(self, _parameters):
        print("Prints Hello World 1.")