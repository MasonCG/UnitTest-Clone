from myunit import assertEqual, assertInRange, assertTrue, assertFalse

class AssertionHelperTests:
    def TestEqual(self):
        assertEqual(10, 10)

    def TestInRange(self):
        assertInRange(5, 1, 10)

    def TestTrueFalse(self):
        assertTrue(3 < 5)
        assertFalse(5 < 3)
