from assertions import Assert

class TruthinessTests:
    def TestIsTrue(self):
        assert Assert.IsTrue(True)
        assert Assert.IsTrue(1 == 1)

    def TestIsFalse(self):
        assert Assert.IsFalse(False)
        assert Assert.IsFalse(1 == 2)

    def TestIs(self):
        assert Assert.Is(5, 5)
        assert Assert.Is("x", "x")

    def TestIsNot(self):
        assert Assert.IsNot(5, 6)
        assert Assert.IsNot("a", "b")
