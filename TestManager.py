# requierd python Modules
import importlib
import inspect
import threading
import sys
import os
import time
from junit_xml import TestCase, TestSuite
from colorama import Fore, Style

# Custom python Module to help
from Utils import clear_terminal

# report constants
PASSED: bool = None
SKIPPED: str = "Skipped"
EXPECTED_FAILURE: str = "Expected Failure"


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
    
    def __failOut(self):
        # current function call
        current_frame = inspect.currentframe()
        #  previous function call (testClass)
        class_frame = current_frame.f_back
        # function call before previous (testModule)
        module_frame = class_frame.f_back
        # getting results dict from testClass()
        class_results = class_frame.f_locals['results']
        # getting klass obj from testModule()
        module_klass_obj = module_frame.f_locals['klass']
        # getting results dict from testModule()
        module_results = module_frame.f_locals['results']
        # updating unfinished class results to results dict from testModule()
        module_results[module_klass_obj] = class_results
        # getting module obj from testModule()
        module = module_frame.f_locals['module']
        # updating testData to reflect all the tests
        self._testData[module] = module_results

        self.printTests(failing_out=True)
        sys.exit(1)


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
                results[method] = self.__createTestTuple(msg=SKIPPED)
                continue
            if hasattr(method, "__expected_failure__"):
                results[method] = self.__createTestTuple(msg="Expected Failure")
                continue

            if hasattr(klass, "setUp"):
                klass.setUp(klass)

            result = self.testMethod(klass, method)
            results[method] = result

            #required to be emmitted after method failure
            if hasattr(method, "__fail_out__") and result[0]:
                self.__failOut()
            
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
        
        return self.__createTestTuple(msg=PASSED,  startTime=start_time)

    def testAll(self):
        self._testData = {}
        for module in self._modules.keys():
            self._testData[module] = self.testModule(module)

    def __getNumModules(self) -> int:
        self.__testDataAvailable()
        return len(list(self._testData))
    
    def __getNumClasses(self) -> int:
        self.__testDataAvailable()

        numClasses: int = 0
        for klass_dict in self._testData.values():
            numClasses += len(list(klass_dict.keys()))

        return numClasses
    
    def __getNumMethods(self) -> int:
        self.__testDataAvailable()
        numMethods: int = 0
        for klass_dict in self._testData.values():
            numMethods += len(list(klass_dict.values()))

        return numMethods

    def __testDataAvailable(self):
        if not len(list(self._testData)):
            raise LookupError("Test Data is not available. Please make sure to run testAlL before calling this function")

    def CreateJUnitXmlReport(self, filename:str = "report.xml"):
        self.__testDataAvailable()

        test_suites = []
        for module in self._testData:
            test_cases = []
            for klass in self._testData[module]:
                for method, result in self._testData[module][klass].items():
                    tc = TestCase(name=f'{method.__name__}.py', classname=klass.__name__, elapsed_sec=result[1])
                    
                    if result[0] == PASSED:
                        tc.add_skipped_info(message=result[0])
                    elif "Assert." in result[0] or result[0] == EXPECTED_FAILURE:
                        tc.add_failure_info(message=result[0])
                    else:
                        tc.add_error_info(message=result[0])
                    
                    test_cases.append(tc)
            
            test_suites.append(TestSuite(f'{module.__name__}.py', test_cases))

        with open(filename, 'w') as f:
            TestSuite.to_file(f, test_suites, prettyprint=True)

        






    def printTests(self, failing_out: bool =False) -> None:

        self.__testDataAvailable()

        clear_terminal()
        print(Style.RESET_ALL)
        total_time:float = 0
        for module in self._testData:
            s = f'{Fore.GREEN}Running Tests in {module.__name__}.py\n{Fore.BLUE}{'-'*50}\n'
            total_module_time: float = 0
            for klass in self._testData[module].keys():
                
                total_class_time:float = 0    
                passed:int = 0
                failed:int = 0
                skipped:int = 0

                for method, result in self._testData[module][klass].items():

                    e, testing_time = result
                    output = self._passedString
                    if e == PASSED:
                        passed += 1 
                    elif e == SKIPPED:
                        skipped += 1
                        output = self._skippedString
                    else:
                        failed += 1
                        output = self._failedString

                    if e != PASSED:
                        output += f' {e}'

                    total_class_time += testing_time                    

                    s += f'{Fore.BLUE}{klass.__name__}.{method.__name__:<25}{output} ({testing_time:.3f}s)\n'
                total_module_time += total_class_time
                s+= f'{'-'*50}\n'
                s+=f"{Fore.RED}Passed: {passed} | Failed: {failed} | Skipped: {skipped} | Duration: {total_class_time:.2f}\n\n"
            total_time += total_module_time
            
            print(s)


        final_s = f'{Fore.BLUE}{'-'*50}\n'
        final_s += f'{"Modules Tests: ":<25}{self.__getNumModules()}\n' 
        final_s += f'{"Classes Tested: ":<25}{self.__getNumClasses()}\n'
        final_s += f'{"Methods Tested: ":<25}{self.__getNumMethods()}\n'
        final_s += f'{"Test Duration: ":<25}{total_time:.3f}s\n'
        final_s += f'{'-'*50}\n'

        print(final_s)

        if failing_out:
            print(f"{Style.BRIGHT}{Fore.RED}{'-'*50}\nTests have stopped! Last test failed out!\n{'-'*50}\n")

        else:
            print(f"{Fore.GREEN}{'-'*50}\nCongratulations all Tests have been run!\n{'-'*50}\n")

        print(Style.RESET_ALL)

        
    
