class CounterTests:
    count = 0

    @classmethod
    def setUpClass(cls):
        cls.count = 0
        print("[setupClass] Counter reset")

    def setUp(self):
        self.value = 10

    def tearDown(self):
        print(f"[tearDown] Finished test with value={self.value}")

    @classmethod
    def tearDownClass(cls):
        print("[tearDownClass] All done")

    def TestIncrement(self):
        self.value += 1
        assert self.value == 11

    def TestDecrement(self):
        self.value -= 1
        assert self.value == 9
