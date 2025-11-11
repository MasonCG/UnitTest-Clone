from assertions import Assert

class NoneAndTypeTests:
    def TestIsNone(self):
        assert Assert.IsNone(None)

    def TestIsNotNone(self):
        assert Assert.IsNotNone(10)

    def TestIsInstance(self):
        assert Assert.IsInstance(5, int)
        assert Assert.IsInstance("hello", str)

    def TestIsNotInstance(self):
        assert Assert.IsNotInstance(5, str)
        assert Assert.IsNotInstance([], dict)
