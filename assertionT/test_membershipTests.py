from UnitTests import Assert

class MembershipTests:
    def TestIn(self):
        assert Assert.In(3, [1, 2, 3])
        assert Assert.In('a', 'cat')

    def TestNotIn(self):
        assert Assert.NotIn(4, [1, 2, 3])
        assert Assert.NotIn('z', 'cat')
