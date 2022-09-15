import pytest
from app.calculator import Calculator


class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiplay_calculate_correctly(self):
        assert self.calc.multiply(self, 2, 7) == 14

    def test_divison_correct(self):
        assert self.calc.division(self, 27, 3) == 9

    def test_subtraction_correct(self):
        assert self.calc.subtraction(self, 30, 3) == 27

    def test_adding_correct(self):
        assert self.calc.adding(self, 20, 7) == 150