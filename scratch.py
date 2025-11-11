import sys
import inspect
import importlib
import os


try:
    assert False, "This assertion will fail"
except AssertionError as e:
    print(f"Caught assertion error: {e}")
except Exception as e:
    print(f"Caught a general exception: {e}")