from assertions import Assert

def raises_zero_div():
    1 / 0

def raises_value_err():
    int('x')

class ExceptionTests:
    def TestRaises(self):
        assert Assert.Raises(ZeroDivisionError, raises_zero_div)
        assert Assert.Raises(ValueError, raises_value_err)
