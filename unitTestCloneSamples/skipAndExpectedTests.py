def skip(reason):
    def wrapper(func):
        func.__skip__ = reason
        return func
    return wrapper

def expectedFailure(func):
    func.__expected_failure__ = True
    return func


class ConditionalTests:
    @skip("Feature not ready yet")
    def TestUnimplemented(self):
        assert False  # Should be skipped

    @expectedFailure
    def TestKnownBug(self):
        assert 2 * 2 == 5  # Known failing test

    def TestRegular(self):
        assert 3 * 3 == 9
