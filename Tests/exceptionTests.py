class ExceptionTests:
    def TestRaiseException(self):
        try:
            raise ValueError("This is an intentional error")
        except ValueError as e:
            assert str(e) == "This is an intentional error"

    def TestUnhandledException(self):
        # Should cause your runner to mark as failed
        raise RuntimeError("Runtime Test Error")
