import time
import os
class PerformanceTests:
    def TestFast(self):
        assert sum(range(10)) == 45

    def TestSlow(self):
        time.sleep(0.5)
        assert sum(range(100)) == 4950

    def TestInfiniteLoop(self):
        print(os.getcwd())
        while True:
            pass
