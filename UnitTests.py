import os
import importlib
import inspect
import threading
import sys
import os
import time
from colorama import Fore, init
import random

init(autoreset=True)

class Assert():
    """ A collection of assertion tests"""

    def __raiseError(expr: str = "") -> Exception:
        """
            raises error for the assert functions
            expr(str): info to print to console
            raises(RunTimeError): "Assert.functionCallName Error"
        """
        funcCall = inspect.currentframe().f_back
        funcName = funcCall.f_code.co_name
        line = funcCall.f_back.f_lineno
        raise RuntimeError(f"(line {line}) Asssert.{funcName} Error: {expr}")
    

    # Eaulity and Inequalities
    def Equal(a: any, b: any) -> Exception:
        """ Raises error if a != b """
        if not a == b:
            Assert.__raiseError(f"Expected [{a}], got [{b}]")

    def NotEqual(a: any, b: any):
        """ Raises error if a == b """
        if a==b:
            Assert.__raiseError()

    def AlmostEqual(a, b, places=7):
        roundA = round(a, places)
        roundB = round(b, places)
        if round(a, places) != round(b, places):
            Assert.__raiseError(f"Expected [{roundA}], got [{roundB}] round to [{places}] places")

    def NotAlmostEqual(a, b, places=7):
        if not round(a-b, places):
            Assert.__raiseError()
    
    
    # Truthiness
    def IsTrue(expr):
        return expr
    def IsFalse(expr):
        return expr
    def Is(expr1, expr2):
        return expr1 == expr2
    def IsNot(expr1, expr2):
        return not (expr1 == expr2)
    
    # None and Boolean Checks
    def IsNone(obj):
        return obj == None
    def IsNotNone(obj):
        return not (obj == None)

    # Membership and Type
    def In(member, container):
        return member in container
    def NotIn(member, container):
        return not (member in container)
    def IsInstance(obj, cls):
        return isinstance(obj, cls)
    def IsNotInstance(obj, cls):
        return not isinstance(obj, cls)
    
    # Exception and Wanring
    def Raises(execType, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            if (execType == type(e)):
                return True
        return False

    # def Warns(warning_type, func, *args, **kwargs)

    # Range and Numeric
    def Greater(a, b):
        return a > b
    def GreaterEqual(a, b):
        return a >= b
    def Less(a, b):
        return a < b
    def LessEqual(a, b):
        return a <= b
    def InRange(x, low, high):
        return low <= x <= high
    

    """ 

    🔹 Exception and Warning
    assertWarns(warning_type, func, *args, **kwargs)	True if warning raised.
    🔹 Custom Utility Booleans (optional but common in clones)
    assertFileExists(path)	True if file exists.
    assertDictContainsSubset(subset, dictionary)	True if dict contains keys and values.
    assertCountEqual(a, b)	True if two sequences have same elements with same counts.
    assertSameElements(a, b)	True if sets of elements match.
    assertJsonEqual(json1, json2)	True if parsed JSON objects match.
    assertWithinDelta(a, b, delta)	True if abs(a-b) <= delta.
    """
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
        results = {}
        for klass in self._modules[module]:
            results[klass] = self.testClass(module, klass)
        
        return results
        

    def testClass(self, module, klass):
        results = {}
        if hasattr(klass, "setUpClass"):
            klass.setUpClass()

        for method in self._modules[module][klass]:
            if hasattr(klass, "setUp"):
                klass.setUp(klass)
            results[method] = self.testMethod(klass, method)
            
            if hasattr(klass, "tearDown"):
                klass.tearDown(klass)

        if hasattr(klass, "tearDownClass"):
            klass.tearDownClass()
        

        return results
                        

    def testMethod(self, Klass, method):
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
            return ("Assertion Error", time.time() - start_time)
        except Exception as e:            
            return (e, time.time() - start_time)
        
        return (None,  time.time() - start_time)

    def testAll(self):
        self._testData = {}
        for module in self._modules.keys():
            self._testData[module] = self.testModule(module)

    def logger(self):

        for module in self._testData:
            s = f'\n{Fore.GREEN}Running Tests in {module.__name__}.py\n{Fore.BLUE}{'-'*50}\n'
            for klass in self._testData[module].keys():
                total_class_time:float = 0    
                passed:int = 0
                failed:int = 0
                skipped:int = 0

                for method, result in self._testData[module][klass].items():
                    e, testing_time = result
                    if not e:
                        passed += 1 
                    else:
                        failed += 1
                    total_class_time += testing_time
                    ouput = self._passedString if not e else f'{self._failedString} {str(e)}'

                    s += f'{Fore.BLUE}{klass.__name__}.{method.__name__:<25}{ouput} ({testing_time:.3f}s)\n'
                s+= f'{'-'*50}\n'
                s+=f"{Fore.RED}Passed: {passed} | Failed: {failed} | Skipped: {skipped} | Duration: {total_class_time:.2f}\n\n"
            print(s)

        
        
if __name__ == "__main__":
    unitTest = UnitTests()
    unitTest.initialize()
    unitTest.testAll()
    unitTest.logger()