"""Regression tests for the safe calculator."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from jadivcli.commands.misc import calc
from jadivcli.safemath import CalcError, evaluate


class SafeMathRealResultsTest(unittest.TestCase):
    def test_negative_base_fractional_power_is_rejected(self):
        expressions = ("(-8)**(1/3)", "(-2)**0.5", "(-8)**(-0.5)")
        for expression in expressions:
            with self.subTest(expression=expression):
                with self.assertRaises(CalcError) as caught:
                    evaluate(expression)
                self.assertEqual(str(caught.exception), "result is not a real number")

    def test_real_powers_still_evaluate(self):
        self.assertEqual(evaluate("(-2)**3"), -8)
        self.assertEqual(evaluate("(-2)**2"), 4)
        self.assertEqual(evaluate("(-8)**1.0"), -8.0)
        self.assertEqual(evaluate("2**(-1)"), 0.5)
        self.assertAlmostEqual(evaluate("8**(1/3)"), 2.0)
        self.assertEqual(evaluate("9**0.5"), 3.0)

    def test_domain_errors_still_raise(self):
        with self.assertRaises(CalcError):
            evaluate("sqrt(-1)")

    def test_calc_command_reports_a_non_real_power(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            calc(None, ["(-8)**(1/3)"])
        self.assertEqual(
            buffer.getvalue(),
            "Invalid expression: result is not a real number\n",
        )


if __name__ == "__main__":
    unittest.main()
