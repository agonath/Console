from consoleCommand import Command

# Test-Command
class Hello_World(Command):

    def execute(self, _parameters):
        print("Hello World!")
        return super().execute(_parameters)

    def helpShort(self, _parameters):
        print("Prints Hello World.")

    def help(self, _parameters):
        print("Prints Hello World.")