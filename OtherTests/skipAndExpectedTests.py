from UnitTests import skip, expectedFailure, failOut, Assert
class ConditionalTests:
    @skip("Feature not ready yet")
    def TestUnimplemented(self):
        assert False  # Should be skipped

    @expectedFailure
    def TestKnownBug(self):
        assert 2 * 2 == 5  # Known failing test

    def TestRegular(self):
        assert 3 * 3 == 9

    @failOut
    def TestFailOutPass(self):
        assert 3 * 3 == 9

    def TestFailOutFail(self):
        Assert.Equal(4, 5)

