from assertions import Assert

class RangeAndNumericTests:
    def TestGreater(self):
        assert Assert.Greater(10, 5)

    def TestGreaterEqual(self):
        assert Assert.GreaterEqual(5, 5)
        assert Assert.GreaterEqual(10, 5)

    def TestLess(self):
        assert Assert.Less(1, 5)

    def TestLessEqual(self):
        assert Assert.LessEqual(5, 5)
        assert Assert.LessEqual(3, 10)

    def TestInRange(self):
        assert Assert.InRange(5, 1, 10)
        assert Assert.InRange(0, -1, 1)
