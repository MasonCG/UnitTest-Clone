class OuterTests:
    def TestOuter(self):
        assert "outer".upper() == "OUTER"

    class InnerTests:
        def TestInner(self):
            assert "inner".capitalize() == "Inner"
