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

    def __init__(self, testDir:str="."):

        if self._initialized:
            return

        self._initialized = True

        self._passedString =  "✅"      
        self._failedString = "❌"
        self._OK = "OK!"
        self._buffer = '\n'

        self._modules = {}
        if not os.path.isdir(testDir):
            raise OSError(f"ERROR: '{testDir}' is not a valid directory")
        
        
        for root, dirs, files in os.walk(testDir):
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

        if not (isinstance(module, str) or type(module).__name__ == "module"):
            raise TypeError(f"ERROR: moduleName must be a string or module class you gave {module} which is a(n) {type(module)}")
        if not (module in self._modules.keys() or module in self.getModuleNames()):
            raise ModuleNotFoundError(f"ERROR: Module '{module}' was not found")
        
        passed = None
        passedString = self._passedString
        if isinstance(module, str):
            module = importlib.import_module(module)

        s = f' {module.__name__}.py\n'
        s += f'\t{len(self._modules[module].keys())} classes, '
        method_count = 0
        klass_string = ""
        for klass in self._modules[module].keys():
            pf, pass_list = self.testClass(module, klass)
            method_count += len(pass_list)
            if pf == self._OK:
                method_string = f'\t{self._passedString} Class: {klass.__name__}(){self._buffer}{"".join(pass_list)}'
            else:
                passed = self._failedString
                method_string = f'\t{self._failedString} Class: {klass.__name__}(){self._buffer}{"".join(pass_list)}'


            klass_string += method_string
            
        s += f'{method_count} methods{self._buffer}\n{klass_string}'

        if passedString == self._passedString:
            passed = self._OK
            
        return (passed, self._buffer + passedString + s + self._buffer)
                

    def testClass(self, module, Klass):
        methods = self._modules[module][Klass]
        pass_list = []
        pf = self._OK

        for m in methods:
            methodString = self.testMethod(Klass, m)
            if self._failedString in methodString:
                pf = None
            pass_list.append(methodString)

        return pf, pass_list

    def getModuleNames(self):
        """ returns a list of all the names of each module"""
        return [m.__name__ for m in self._modules.keys()]

    def testMethod(self, Klass, method):

        s = f"{Klass.__name__}.{method.__name__}()...\n\t\t\t"
        tab = '\t\t'
        try:
            mSignature = inspect.signature(method)
            paramaters = list(mSignature.parameters.keys())
            if not paramaters:
                if method():
                    s = tab + self._passedString + s + self._OK
                else:
                    raise Exception("No Error: Test failed.")
            if len(paramaters) > 1 or paramaters[0] != 'self':
                raise TypeError(f"-> UnitTestError: {method.__name__}() may only have 1 positional argument 'self'.")
            else:

                if method(Klass):
                    s = tab + self._passedString + s + self._OK
                else:
                    raise Exception("Method Finish, but Test failed.")
                
        except Exception as e:
            s = tab + self._failedString + s + f'ERROR: {str(e)}'

        return f'{s}\n'

    def testAll(self):
        passedString = self._passedString
        s = f" Testing {len(self._modules.keys())} Modules...\n"
        for module in self._modules:
            pf, moduleString = self.testModule(module)
            s += moduleString

            if pf != self._OK:
                passedString = self._failedString
        
        s = passedString + s

        print(s[:-2])


if __name__ == "__main__":
    unitTest = UnitTests()
    clear_terminal()
    unitTest.testAll()