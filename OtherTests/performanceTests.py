import time

class PerformanceTests:
    def TestFast(self):
        assert sum(range(10)) == 45

    def TestSlow(self):
        time.sleep(0.5)
        assert sum(range(100)) == 4950
