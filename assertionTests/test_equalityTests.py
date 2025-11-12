from UnitTests import Assert

class EqualityTests:
    def TestEqual(self):
        Assert.Equal(5, 5)
        Assert.Equal("hello", "hello")

    def TestNotEqual(self):
        Assert.NotEqual(5, 4)
        Assert.NotEqual("hi", "bye")

    def TestAlmostEqual(self):
        Assert.AlmostEqual(1.000001, 1.000002, places=5)

    def TestNotAlmostEqual(self):
        Assert.NotAlmostEqual(1.001, 1.002, places=5)
