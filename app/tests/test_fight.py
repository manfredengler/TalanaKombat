import unittest
from fight import get_steps
from errors.fight import EmptySteps

class TestFight(unittest.TestCase):

    def test_get_steps(self):

        test_cases = [
            {"data":{'movimientos': ['DSD', 'S'], 'golpes': ['P', '']}, "expected":[('DSD', 'P'), ('S', '')]},
            {"data":{'movimientos': ['DSD', 'WSAW', 'ASA', '', 'ASA', 'SA'], 'golpes': ['P', 'K', 'K', 'K', 'P', 'k']}, "expected":[('DSD', 'P'), ('WSAW', 'K'), ('ASA', 'K'), ('', 'K'), ('ASA', 'P'), ('SA', 'k')]},
        ]

        for test_case in test_cases:
            with self.subTest(data=test_case["data"]):
                result = get_steps(test_case["data"])
                self.assertEqual(result, test_case["expected"])

    def test_get_steps_failure__empty_dict(self):
        data = {}
        expected_error = EmptySteps("Se esperaban ambos diccionarios: movimientos y golpes")
        with self.assertRaises(EmptySteps) as cm:
            get_steps(data)

        exception = cm.exception
        self.assertEqual(str(exception), str(expected_error))

    def test_get_steps_failure__wrong_movements(self):
        data = {'movimientos': (), 'golpes': ['P', '']}
        expected_error = TypeError("El valor de 'movimientos' debe ser una lista")
        with self.assertRaises(TypeError) as cm:
            get_steps(data)

        exception = cm.exception
        self.assertEqual(str(exception), str(expected_error))

    def test_get_steps_failure__wrong_strikes(self):
        data = {'movimientos': ['DSD', 'S'], 'golpes': ""}
        expected_error = TypeError("El valor de 'golpes' debe ser una lista")
        with self.assertRaises(TypeError) as cm:
            get_steps(data)

        exception = cm.exception
        self.assertEqual(str(exception), str(expected_error))