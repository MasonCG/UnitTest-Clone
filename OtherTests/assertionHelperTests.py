from UnitTests import Assert, failOut

class AssertionHelperTests:
    def TestEqual(self):
        Assert.Equal(9, 10)

    def TestInRange(self):
        Assert.InRange(5, 1, 10)

    def TestTrueFalse(self):
        Assert.IsTrue(3 < 5)
        Assert.IsTrue(5 < 3)

    def TestRounded(self):
        Assert.AlmostEqual(2.001, 2.003, 2)
        Assert.NotAlmostEqual(2.003, 2.001, 3)

