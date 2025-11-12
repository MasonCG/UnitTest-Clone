# Custome Python Modules
import Assertions
import Decorators
from TestManager import TestManager


# setting global Assert Class
Assert = Assertions.Assert

# setting global Decorators
skip = Decorators.skip
expectedFailure = Decorators.expectedFailure
failOut = Decorators.failOut

def testModules():
    TM = TestManager()
    TM.printTests()
        
        
if __name__ == "__main__":
    TM = TestManager()
    TM.printTests()