import os
import importlib
import inspect
import threading
import sys
import os

def clear_terminal():
    """Clears the terminal screen based on the operating system."""
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux (POSIX systems)
    else:
        _ = os.system('clear')


class UnitTests(object):
    """
        Holds all of the classes that have Test attatched. It only looks in the files that also have Test attached to the end.
    """
    _instance = None
    _initialized = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                # If no instance exists, create one using the superclass's __new__
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):

        if self._initialized:
            return

        self._initialized = True

        self._passedString =  "✅"      
        self._failedString = "❌"
        self._testDir = "."
        self._modules = {}
        self._testData = {}

    def initialize(self):
        
        for _, dirs, files in os.walk(self._testDir):
            dirs[:] = [d for d in dirs if "Tests" in d]
            files[:] = [f for f in files if "Tests" in f and f != "UnitTests.py"]
            for f in files:
                module = importlib.import_module(f[:-3])
                self._modules[module] = {}

        for module in self._modules.keys():
            module_dict = {}
            klasses = [k for k, obj in inspect.getmembers(module) if inspect.isclass(obj)]
            for k in klasses:
                klass = getattr(sys.modules[module.__name__], k)
                methods = [m for name, m in inspect.getmembers(klass, predicate=inspect.isfunction) if 'Test' in name]
                module_dict[klass] = methods

            self._modules[module] = module_dict

    def __str__(self):
        s = "\n"
        for key in self._modules:
            s += f'{str(key)} -> [\n'
            for klass, methods in self._modules[key].items():
                s += f'\t{str(klass)} -> {"".join(str(methods))}\n'
            s += ']\n'
        return s

    def testModule(self, module):
        exceptions = {}
        for klass in self._modules[module]:
            exceptions[klass] = self.testClass(module, klass)
        
        return exceptions
        

    def testClass(self, module, klass):
        exceptions = {}
        for method in self._modules[module][klass]:    
            exceptions[method] = self.testMethod(klass, method)

        return exceptions
                        

    def testMethod(self, Klass, method):
        try:
            method_signature = inspect.signature(method)
            method_paramaters = list(method_signature.parameters.keys())
            if len(method_paramaters) > 1 or method_paramaters[0] != 'self':
                raise TypeError("Method must only have 1 positional argument 'self'")

            if not method_paramaters and not method():
                raise TypeError("Method must not return a value")

            elif not method(Klass):
                raise TypeError("Method must not return a value.")
        except Exception as e:
            return e
        
        return None

    def __getModuleNames(self):
        """ returns a list of all the names of each module"""
        return [m.__name__ for m in self._modules.keys()]


    def testAll(self):
        self._testData = {}
        for module in self._modules.keys():
            self._testData[module] = self.testModule(module)

    def printTestData(self):
        s = ''
        for module in self._testData:
            s += f'{module.__name__} -> [\n'
            for klass in self._testData[module].keys():
                s += f'\t{klass.__name__} -> [\n'
                for method, e in self._testData[module][klass].items():
                    s += f'\t\t{method.__name__} -> [{e}],\n'
            s += '\t],\n'
        s += ']\n'
        
        print(s)

        


if __name__ == "__main__":
    unitTest = UnitTests()
    clear_terminal()
    unitTest.initialize()
    unitTest.testAll()
    unitTest.printTestData()