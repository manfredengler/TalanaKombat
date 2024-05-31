import unittest
from unittest.mock import patch, Mock, call
from fight import get_steps, zip_steps, Player
from errors.fight import EmptySteps
from constants import PLAYER_1, PLAYER_2, HABILITIES, STARTING_DRAW_LIMIT, MOVEMENT_INTERPRETER, DEFAULT_LIFE


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


class TestZipSteps(unittest.TestCase):
    @patch('fight.get_steps')
    def test_zip_steps(self, mock_get_steps):
        # Hago un mock de get_steps para saltar su lógica
        player1_data = Mock()
        player2_data = Mock()

       # Fuerzo salida esperada del mock
        mock_get_steps.side_effect = [
            [('DSD', 'P'), ('S', '')],  # Valor de retorno para "player1"
            [('DSD', 'P'), ('WSAW', 'K'), ('ASA', 'K')]  # Valor de retorno para "player2"
        ]

        input_dict = {"player1": player1_data, "player2": player2_data}
        expected_output = [(('DSD', 'P'), ('DSD', 'P')), (('S', ''), ('WSAW', 'K')), (['', ''], ('ASA', 'K'))]

        # Ejecutamos funcion a probar
        result = zip_steps(input_dict)

        # Verifico con resultado esperado
        self.assertEqual(result, expected_output)

        # Verifico que se haya llamado a get_steps con los argumentos correctos
        mock_get_steps.assert_has_calls([
            call(steps=player1_data),
            call(steps=player2_data)
        ])

    @patch('fight.get_steps')
    def test_zip_steps_failure__get_step_raises_an_error(self, mock_get_steps):
        player1_data = Mock()
        player2_data = Mock()

        # Fuerzo que get_steps de un error
        mock_get_steps.side_effect = ValueError("Error al obtener los pasos")

        input_dict = {"player1": player1_data, "player2": player2_data}

        # Verifico que el error ocurra al llamar a zip_steps, solo falla no debe manejar el caso
        with self.assertRaises(ValueError):
            zip_steps(input_dict)



class TestPlayerInit(unittest.TestCase):
    def test_init_with_valid_data(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)

        self.assertEqual(player.number, 1)
        self.assertEqual(player.fullname, "Tonyn Stallone")
        self.assertEqual(player.name, "Tonyn")
        self.assertEqual(player.life, DEFAULT_LIFE)
        self.assertEqual(player.combos, HABILITIES["Tonyn Stallone"])
        self.assertEqual(player.movement_interpreter, MOVEMENT_INTERPRETER["Tonyn Stallone"])

    def test_init_with_missing_number(self):
        data = {"name": "Jane Doe"}
        with self.assertRaises(KeyError):
            Player(data)

    def test_init_with_missing_name(self):
        data = {"number": 2}
        with self.assertRaises(AttributeError):
            Player(data)

    def test_init_with_invalid_data_type(self):
        data = "invalid data type"
        with self.assertRaises(AttributeError):
            Player(data)
