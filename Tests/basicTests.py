class MathTests:
    def TestAddition(self):
        assert 1 + 1 == 2

    def TestSubtraction(self):
        assert 5 - 3 == 2

    def TestDivision(self):
        result = 10 / 2
        assert result == 5

    def TestFailing(self):
        # This should fail
        assert False

class StringTests:
    def TestConcating(self):
        assert 's' + 's' =='ss'

    def TestRemoving(self):
        assert 'hello'[-1] == 'o'

    def TestSlicing(self):
        assert 'juvial'[:-1] == 'juvia'

    def TestSliceFail(self):
        # This should fail
        assert False
