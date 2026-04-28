# UnitTest-Rendition
A Python Clone of UniteTests to practice creating a customizable, scalable, and generic module for general use. The goal is to be able to add any number of tests the user wishes allowing them to ensure their program continues to run smoothly and for debugging to be streamlined.

How it works:
1. walks through local files in relative path to TestManager.py
2. Finds any modules with test -> classes named test -> methods name test.
3. Supports setup and teardown methods.
4. Supports @failOut, @skip, and @expectedFailure decorators
5. Supports Common assertions tests. (Only failsOut with respective decorator)
6. Prints Test in readable format.
7. Creates Junit-xml file in "test-results" directory.

How to use:

1. File Management
- Ensure TestManager.py, Decorators.py, Utils.py, and Assertions.py are all in the same relative path.

2. Importing
- Import Decoractors, Assertions, and functions through UnitTests.py.
- import function testModules() and run.

3. Creating Tests
- tests are class based.
- Modules, classes and methods holding tests should be suffixed with "Test" or prefixed with "test_"
- to use Assertions import Assert as a class.
- 

