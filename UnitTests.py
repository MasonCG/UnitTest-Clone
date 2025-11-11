import os
import importlib
import inspect
import threading
import sys
import os
import time
from colorama import Fore, init

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
    def Equal(a: any, b: any) -> Exception | bool:
        """ Raises error if a != b """
        if not a == b:
            Assert.__raiseError(f"Expected [{a}], got [{b}]")

        return True

    def NotEqual(a: any, b: any) -> Exception | bool:
        """ Raises error if a == b """
        if a==b:
            Assert.__raiseError()

        return True

    def AlmostEqual(a, b, places=7) -> Exception | bool:
        roundA = round(a, places)
        roundB = round(b, places)
        if round(a, places) != round(b, places):
            Assert.__raiseError(f"Expected [{roundA}], got [{roundB}] round to [{places}] places")

        return True
        

    def NotAlmostEqual(a, b, places=7) -> Exception | bool:
        if not round(a-b, places):
            Assert.__raiseError()

        return True
        
    
    # Truthiness
    def IsTrue(expr) -> Exception | bool:
        if not expr:
            Assert.__raiseError()

        return True
        
    def IsFalse(expr) -> Exception | bool:
        if expr:
            Assert.__raiseError()

        return True
        

    def Is(expr1, expr2) -> Exception | bool:
        if not expr1 == expr2:
            Assert.__raiseError(f"Expected [{expr1}, got [{expr2}]]")

        return True
        
    def IsNot(expr1, expr2) -> Exception | bool:
        if (expr1 == expr2):
            Assert.__raiseError()

        return True
            
    
    # None and Boolean Checks
    def IsNone(obj) -> Exception | bool:
        if not obj == None:
            Assert.__raiseError(f'Expected [None], got [{obj}]')

        return True
    
    def IsNotNone(obj) -> Exception | bool:
        if obj == None:
            Assert.__raiseError(f"Expected [{obj}], got [None]")

        return True

    # Membership and Type
    def In(member, container) -> Exception | bool:
        if not member in container:
            Assert.__raiseError()
        
        return True

    def NotIn(member, container) -> Exception | bool:
        if member in container:
            Assert.__raiseError()

        return True

    def IsInstance(obj, cls) -> Exception | bool:
        if not isinstance(obj, cls):
            Assert.__raiseError(f'Expected [{cls}], got [{type(obj)}]')

        return True
    
    def IsNotInstance(obj, cls) -> Exception | bool:
        if isinstance(obj, cls):
            Assert.__raiseError()

        return True
            
    
    # Exception and Wanring
    def Raises(execType, func, *args, **kwargs) -> Exception | None:
        execName = execType.__name__

        try:
            func(*args, **kwargs)
        except Exception as e:
            eName = type(e).__name__
            if not execName == eName:
                Assert.__raiseError(f"Expected [{execName}], got [{eName}]")
            else:
                return True
        
        Assert.__raiseError(f"No Error Raised")
        
    # def Warns(warning_type, func, *args, **kwargs)

    # Range and Numeric
    def Greater(a, b) -> Exception | bool:
        if not a > b:
            Assert.__raiseError(f"[{a}] <= [{b}]")

        return True
    
    def GreaterEqual(a, b) -> Exception | bool:
        if not a >= b:
            Assert.__raiseError(f"[{a}] < [{b}]")

        return True
    
    def Less(a, b) -> Exception | bool:
        if not a < b:
            Assert.__raiseError(f"[{a}] >= [{b}]")
    
        return True

    def LessEqual(a, b) -> Exception | bool:
        if not a <= b:
            Assert.__raiseError(f"[{a}] > [{b}]")

        return True

    def InRange(x, low, high) -> Exception | bool:
        if not low <= x <= high:
            Assert.__raiseError(f'[{x}] not in range [{low, high}]')
        
        return True


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
        for i in range(5):
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
        self.initialize()

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