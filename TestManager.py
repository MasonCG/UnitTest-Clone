# requierd python Modules
import importlib
import inspect
import threading
import sys
import os
import time
from colorama import Fore, Style

# Custom python Module to help
from Utils import clear_terminal

class TestManager(object):
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
        self._skippedString = "🟡"
        self._testDir = "."
        self._modules = {}
        self._testData = {}
        self.initialize()

    def __createTestTuple(self, msg: str | None, startTime: int = 0) -> tuple:
        if startTime:
            startTime = time.time() - startTime
        return (msg, startTime)
    


    def initialize(self):
        
        for root, dirs, files in os.walk(self._testDir):
            dirs[:] = [d for d in dirs if "Tests" in d]
            files[:] = [f for f in files if "Tests" in f and f != "UnitTests.py"]
            sys.path.append(root)
            for f in files:
                module = importlib.import_module(f[:-3])
                self._modules[module] = {}
            sys.path.remove(root)

        for module in self._modules.keys():
            module_dict = {}
            klasses = [k for k, obj in inspect.getmembers(module) if inspect.isclass(obj)]
            klasses[:] = [k for k in klasses if "Tests" in k]
            for k in klasses:
                klass = getattr(sys.modules[module.__name__], k)
                methods = [m for name, m in inspect.getmembers(klass, predicate=inspect.isfunction) if 'Test' in name]
                module_dict[klass] = methods

            self._modules[module] = module_dict

    def __str__(self):
        s = "\n"
        for module in self._modules:
            s += f'{module.__name__}: [\n'
            for klass in self._modules[module]:
                s += f'\t{klass.__name__}: ['
                for method in self._modules[module][klass]:
                    s += f' {method.__name__},'
                s = s[:-1] + '],\n'
            s += s[:-2] + '\n]\n\n'
        return s

    def testModule(self, module):
        results = {}
        for klass in self._modules[module]:
            results[klass] = self.testClass(module, klass)
        
        return results
        

    def testClass(self, module, klass):
        results = {}
        if hasattr(klass, "setUpClass"):
            klass.setUpClass()

        for method in self._modules[module][klass]:
            if hasattr(method, "__skip__"):
                results[method] = self.__createTestTuple(msg="Skipped")
                continue
            if hasattr(method, "__expected_failure__"):
                results[method] = self.__createTestTuple(msg="Expected Failure")
                continue

            if hasattr(klass, "setUp"):
                klass.setUp(klass)

            
            results[method] = self.testMethod(klass, method)
            
            if hasattr(klass, "tearDown"):
                klass.tearDown(klass)

        if hasattr(klass, "tearDownClass"):
            klass.tearDownClass()
        

        return results
                        

    def testMethod(self, Klass: object, method: object) -> Exception | tuple:
        start_time = time.time()
        method_signature = inspect.signature(method)
        method_paramaters = list(method_signature.parameters.keys())

        try:
            if len(method_paramaters) > 1 or method_paramaters[0] != 'self':
                raise TypeError("Method must only have 1 positional argument 'self'")

            if not method_paramaters and not method():
                raise TypeError("Method must not return a value")

            elif method(Klass):
                raise TypeError("Method must not return a value.")
        except AssertionError:
            return self.__createTestTuple(msg="Assertion Error",startTime=start_time)
        except Exception as e:            
            return self.__createTestTuple(msg=e, startTime=start_time)
        
        return self.__createTestTuple(msg=None,  startTime=start_time)

    def testAll(self):
        self._testData = {}
        for module in self._modules.keys():
            self._testData[module] = self.testModule(module)

    def printTests(self):

        if not len(list(self._testData)):
            self.testAll()


        clear_terminal()
        print(Style.RESET_ALL)
        for module in self._testData:
            s = f'{Fore.GREEN}Running Tests in {module.__name__}.py\n{Fore.BLUE}{'-'*50}\n'
            for klass in self._testData[module].keys():
                total_class_time:float = 0    
                passed:int = 0
                failed:int = 0
                skipped:int = 0

                for method, result in self._testData[module][klass].items():
                    e, testing_time = result
                    output = self._passedString
                    if not e:
                        passed += 1 
                    elif e == "Skipped":
                        skipped += 1
                        output = self._skippedString
                    else:
                        failed += 1
                        output = self._failedString

                    total_class_time += testing_time

                    if e != None:
                        output += f' {e}'
                    

                    s += f'{Fore.BLUE}{klass.__name__}.{method.__name__:<25}{output} ({testing_time:.3f}s)\n'
                s+= f'{'-'*50}\n'
                s+=f"{Fore.RED}Passed: {passed} | Failed: {failed} | Skipped: {skipped} | Duration: {total_class_time:.2f}\n\n"
            print(s + Style.RESET_ALL)