import pytest
from core.pytest_practice import A, Calculator
from contextlib import nullcontext as does_not_raise

class TestCalculator:
    @pytest.mark.parametrize("x, y, res, expectation",
        [
        (1, 2, 0.5, does_not_raise()),
        (10, 2, 5, does_not_raise()),
        (5, "-1", -5, pytest.raises(TypeError)),
        # (10, 0, pytest.raises(ValueError)),
        ])
    def test_divide(self, x, y, res, expectation):
        with expectation:
            assert Calculator().divide(x, y) == res


    @pytest.mark.parametrize("x, y, res,",
            [
                (1, 2, 3),
                (10, 5, 15),
                (5, -1, 4),
            ])
    def test_add(self, x, y, res):
        assert Calculator().add(x, y) == res

class TestA:
    def test_1(self):
        assert A.x == 1

    def test_2(self):
        assert 2 == 2