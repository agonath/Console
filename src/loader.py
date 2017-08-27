import importlib
import sys
import os

# Directory separator
SEP=os.sep

class SystemLoader(object):

    #
    # Helper: Remove file format endings if needed.
    #
    def normalizeModuleName(self, _moduleName):
        if(0 < len(_moduleName)):
            if(True == _moduleName.endswith(".py")):
                return _moduleName[:-3]
            elif(True ==_moduleName.endswith(".pyc") or True == _moduleName.endswith(".pyo")):
                return _moduleName[:-4]
            else:
                return _moduleName
                
            

    #
    # Load a class from module in given path.
    #
    # Module parameter must be a "*.py", "*.pyc" or "*.pyo" file.
    # Path parameter points to the local directory by default.
    # Class name must be a class within the module.
    #
    # Example:  " loadModuleByPath(_path="..\\Programs\\Plugins", _moduleName="test", _className="myClass") "
    #           OR " loadModuleByPath(_moduleName="test.pyc", _className="myClass") "
    #
    def load_ModuleAndGetClass(self, *, _className, _moduleName, _path=str(".\\" + SEP)):
        try:
            moduleABC=self.load_ModuleByPath(_path=_path, _moduleName = _moduleName)
            classABC = self.load_ClassFromModule(_className = _className, _module=moduleABC)
            return classABC
        except Exception as e:
            print(e)
        

    #
    # Load module by path.
    # Module must be a "*.py", "*.pyc" or "*.pyo" file.
    # 
    # Example: loadModuleByPath(_path="..\\Programs\\Plugins", _moduleName="test")
    #
    def load_ModuleByPath(self, *, _path=str(".\\" + SEP), _moduleName):
        if(len(_moduleName) > 0):
            mod = self.normalizeModuleName(_moduleName)
            
            if(len(_path) > 0):
                # add path to list of known system paths
                if(_path not in sys.path):
                    sys.path.append(_path)
            # try to load module
            try:
                return importlib.import_module(mod)
            except Exception as e:
                print(e)


    #
    # Load a class from a given module.
    # Module must be an instance of <class, module>.
    #
    def load_ClassFromModule(self, *, _className, _module):
        if(len(_className) > 0 and None != _module):
            try:
                # try to find the class
                newClass = getattr(_module, _className)
                return newClass
            except Exception as e:
                print(e)