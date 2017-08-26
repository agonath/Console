import importlib
import sys


class systemLoader(object):

    #
    # Load a class from a given module.
    # Module must be a subfolder in the same folder as this.
    #
    def loadClassFromModule(self, *, _className, _moduleName):
        if(len(_className) > 0 and len(_moduleName) > 0):
            try:
                # try to import <moduleName.classname>
                module = importlib.import_module(_moduleName + str(".") + _className)
                # try to find the class
                newClass = getattr(module, _className)
                return newClass
            except Exception as e:
                print(e)