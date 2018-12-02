from consoleCommand import Command

# Test-Command
class Hello_World2(Command):

    def execute(self, _parameters):
        print("Hello World 2!")
        return super().execute(_parameters)

    def helpShort(self, _parameters):
        print("Prints Hello World 2.")

    def help(self, _parameters):
        print("Prints Hello World 2.")