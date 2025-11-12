

# Custome Python Modules
import Assertions
import Decorators
from TestManager import TestManager


# setting global Assert Class
Assert = Assertions.Assert
skip = Decorators.skip
expectedFailure = Decorators.expectedFailure



        
        
if __name__ == "__main__":
    TM = TestManager()
    TM.printTests()