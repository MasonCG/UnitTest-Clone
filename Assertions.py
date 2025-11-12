import inspect

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
    
    def Equal(a, b) -> Exception | bool:
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
        """ Raises error if rounded(a-b, places) != 0 """

        roundA = round(a, places)
        roundB = round(b, places)
        if round(a, places) != round(b, places):
            Assert.__raiseError(f"Expected [{roundA}], got [{roundB}] round to [{places}] places")

        return True
        

    def NotAlmostEqual(a, b, places=7) -> Exception | bool:
        """ Raises error if rounded(a-b, places) == 0 """

        if not round(a-b, places):
            Assert.__raiseError()

        return True
        
    def IsTrue(expr:bool) -> Exception | bool:
        """ Raises error if expr == True """
        if not expr:
            Assert.__raiseError()

        return True
        
    def IsFalse(expr:bool) -> Exception | bool:
        """ Raised error if expr == False """
        if expr:
            Assert.__raiseError()

        return True
        

    def Is(item1, item2) -> Exception | bool:
        """ Raises error if item1 != item2 """
        if not item1 == item2:
            Assert.__raiseError(f"Expected [{item1}, got [{item2}]]")

        return True
        
    def IsNot(item1, item2) -> Exception | bool:
        """ Raises error if item1 == item2 """

        if (item1 == item2):
            Assert.__raiseError()

        return True
            
    
    def IsNone(obj) -> Exception | bool:
        """ Rases error if obj != None """

        if not obj == None:
            Assert.__raiseError(f'Expected [None], got [{obj}]')

        return True
    
    def IsNotNone(obj) -> Exception | bool:
        """ Rases error if obj == None """

        if obj == None:
            Assert.__raiseError(f"Expected [{obj}], got [None]")

        return True

    def In(member, container) -> Exception | bool:
        """ Raises error if member in container """
        if not member in container:
            Assert.__raiseError()
        
        return True

    def NotIn(member, container) -> Exception | bool:
        """ Raises error if member not in container """

        if member in container:
            Assert.__raiseError()

        return True

    def IsInstance(obj, cls) -> Exception | bool:
        """ Raises error if isinstance(obj, cls) == False """

        if not isinstance(obj, cls):
            Assert.__raiseError(f'Expected [{cls}], got [{type(obj)}]')

        return True
    
    def IsNotInstance(obj, cls) -> Exception | bool:
        """ Raises error if isinstance(obj, cls) == True """

        if isinstance(obj, cls):
            Assert.__raiseError()

        return True
            
    
    def Raises(execType, func, *args, **kwargs) -> Exception | None:
        """ Raises error if expected Exception is not Exception received 
            Raises error if no Exception is thrown """

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

    def Greater(a, b) -> Exception | bool:
        """ Raises error if a <= b """
        if not a > b:
            Assert.__raiseError(f"[{a}] <= [{b}]")

        return True
    
    def GreaterEqual(a, b) -> Exception | bool:
        """ Raises error if a < b """
        if not a >= b:
            Assert.__raiseError(f"[{a}] < [{b}]")

        return True
    
    def Less(a, b) -> Exception | bool:
        """ Raises error if a >= b """
        if not a < b:
            Assert.__raiseError(f"[{a}] >= [{b}]")
    
        return True

    def LessEqual(a, b) -> Exception | bool:
        """ Raises error if a > b """

        if not a <= b:
            Assert.__raiseError(f"[{a}] > [{b}]")

        return True

    def InRange(x, low, high) -> Exception | bool:
        """ Raises error if x is not in range(low, high) """
        if not low <= x <= high:
            Assert.__raiseError(f'[{x}] not in range [{low, high}]')
        
        return True

""" 
    Exception and Warning
    assertWarns(warning_type, func, *args, **kwargs)	True if warning raised.
    Custom Utility Booleans (optional but common in clones)
    assertFileExists(path)	True if file exists.
    assertDictContainsSubset(subset, dictionary)	True if dict contains keys and values.
    assertCountEqual(a, b)	True if two sequences have same elements with same counts.
    assertSameElements(a, b)	True if sets of elements match.
    assertJsonEqual(json1, json2)	True if parsed JSON objects match.
    assertWithinDelta(a, b, delta)	True if abs(a-b) <= delta.
    """