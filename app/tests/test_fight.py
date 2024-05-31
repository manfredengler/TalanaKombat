import unittest
from unittest.mock import patch, Mock, call, MagicMock
from fight import get_steps, zip_steps, Player, is_player_1_starter, ends_with_word
from errors.fight import EmptySteps
from constants import (
    PLAYER_1,
    PLAYER_2,
    HABILITIES,
    STARTING_DRAW_LIMIT,
    MOVEMENT_INTERPRETER,
    DEFAULT_LIFE,
)


class TestFight(unittest.TestCase):

    def test_get_steps(self):

        test_cases = [
            {
                "data": {"movimientos": ["DSD", "S"], "golpes": ["P", ""]},
                "expected": [("DSD", "P"), ("S", "")],
            },
            {
                "data": {
                    "movimientos": ["DSD", "WSAW", "ASA", "", "ASA", "SA"],
                    "golpes": ["P", "K", "K", "K", "P", "k"],
                },
                "expected": [
                    ("DSD", "P"),
                    ("WSAW", "K"),
                    ("ASA", "K"),
                    ("", "K"),
                    ("ASA", "P"),
                    ("SA", "k"),
                ],
            },
        ]

        for test_case in test_cases:
            with self.subTest(data=test_case["data"]):
                result = get_steps(test_case["data"])
                self.assertEqual(result, test_case["expected"])

    def test_get_steps_failure__empty_dict(self):
        data = {}
        expected_error = EmptySteps(
            "Se esperaban ambos diccionarios: movimientos y golpes"
        )
        with self.assertRaises(EmptySteps) as cm:
            get_steps(data)

        exception = cm.exception
        self.assertEqual(str(exception), str(expected_error))

    def test_get_steps_failure__wrong_movements(self):
        data = {"movimientos": (), "golpes": ["P", ""]}
        expected_error = TypeError("El valor de 'movimientos' debe ser una lista")
        with self.assertRaises(TypeError) as cm:
            get_steps(data)

        exception = cm.exception
        self.assertEqual(str(exception), str(expected_error))

    def test_get_steps_failure__wrong_strikes(self):
        data = {"movimientos": ["DSD", "S"], "golpes": ""}
        expected_error = TypeError("El valor de 'golpes' debe ser una lista")
        with self.assertRaises(TypeError) as cm:
            get_steps(data)

        exception = cm.exception
        self.assertEqual(str(exception), str(expected_error))


class TestZipSteps(unittest.TestCase):
    @patch("fight.get_steps")
    def test_zip_steps(self, mock_get_steps):
        # Hago un mock de get_steps para saltar su lógica
        player1_data = Mock()
        player2_data = Mock()

        # Fuerzo salida esperada del mock
        mock_get_steps.side_effect = [
            [("DSD", "P"), ("S", "")],  # Valor de retorno para "player1"
            [
                ("DSD", "P"),
                ("WSAW", "K"),
                ("ASA", "K"),
            ],  # Valor de retorno para "player2"
        ]

        input_dict = {"player1": player1_data, "player2": player2_data}
        expected_output = [
            (("DSD", "P"), ("DSD", "P")),
            (("S", ""), ("WSAW", "K")),
            (["", ""], ("ASA", "K")),
        ]

        # Ejecutamos funcion a probar
        result = zip_steps(input_dict)

        # Verifico con resultado esperado
        self.assertEqual(result, expected_output)

        # Verifico que se haya llamado a get_steps con los argumentos correctos
        mock_get_steps.assert_has_calls(
            [call(steps=player1_data), call(steps=player2_data)]
        )

    @patch("fight.get_steps")
    def test_zip_steps_failure__get_step_raises_an_error(self, mock_get_steps):
        player1_data = Mock()
        player2_data = Mock()

        # Fuerzo que get_steps de un error
        mock_get_steps.side_effect = ValueError("Error al obtener los pasos")

        input_dict = {"player1": player1_data, "player2": player2_data}

        # Verifico que el error ocurra al llamar a zip_steps, solo falla no debe manejar el caso
        with self.assertRaises(ValueError):
            zip_steps(input_dict)


class TestIsPlayer1Starter(unittest.TestCase):
    def test_is_player_1_starter__player_1_wins(self):
        steps = [(["A", "B"], ["CD", "E"]), (["F", "G"], ["H", "I"])]
        self.assertTrue(is_player_1_starter(steps))

    def test_is_player_1_starter__player_2_wins(self):
        steps = [(["ABCD", "C"], ["D", "E"]), (["F", "G"], ["I", "J"])]
        self.assertFalse(is_player_1_starter(steps))

    def test_is_player_1_starter__tie(self):
        steps = [
            (["A", "B"], ["D", "E"]),
            (["C", "D"], ["C", "D"]),
            (["C", "D"], ["C", "D"]),
        ]
        self.assertTrue(is_player_1_starter(steps))

    def test_is_player_1_starter__limit_reached__player_1_wins(self):
        steps = [(["A", "B"], ["A", "B"])] * 10
        self.assertTrue(is_player_1_starter(steps))

    def test_is_player_1_starter_empty_steps(self):
        steps = []
        self.assertTrue(is_player_1_starter(steps))

    def test_is_player_1_starter_invalid_input(self):
        with self.assertRaises(IndexError):
            is_player_1_starter("invalid input")


class TestEndsWithWord(unittest.TestCase):
    def test_ends_with_word_true(self):
        self.assertTrue(ends_with_word("Hello World", "World"))
        self.assertTrue(ends_with_word("ASDASK", "ASK"))
        self.assertTrue(ends_with_word("ASP", "SP"))
        self.assertTrue(ends_with_word("P", "P"))

    def test_ends_with_word_false(self):
        self.assertFalse(ends_with_word("Hello World", "Universe"))
        self.assertFalse(ends_with_word("ASDASK", "AS"))
        self.assertFalse(ends_with_word("ASAWASP", "WAP"))

    def test_ends_with_word_edge_cases(self):
        self.assertFalse(ends_with_word("", ""))
        self.assertTrue(ends_with_word("Hello World", ""))
        self.assertFalse(ends_with_word("", "AP"))


class TestPlayerInit(unittest.TestCase):
    def test_init_with_valid_data(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)

        self.assertEqual(player.number, 1)
        self.assertEqual(player.fullname, "Tonyn Stallone")
        self.assertEqual(player.name, "Tonyn")
        self.assertEqual(player.life, DEFAULT_LIFE)
        self.assertEqual(player.combos, HABILITIES["Tonyn Stallone"])
        self.assertEqual(
            player.movement_interpreter, MOVEMENT_INTERPRETER["Tonyn Stallone"]
        )

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


class TestPlayerReadCombo(unittest.TestCase):
    def test_read_combo_valid_combo(self):
        player = Player({"number": 1, "name": "Tonyn Stallone"})
        combo = "SDK"
        damage, phrase = player.read_combo(combo)
        self.assertEqual(damage, 2)
        self.assertEqual(phrase, "conecta un Remuyuken")

    def test_read_combo_invalid_combo(self):
        player = Player({"number": 1, "name": "Tonyn Stallone"})
        combo = "invalid_combo"
        with self.assertRaises(AttributeError):
            player.read_combo(combo)

    def test_read_combo_combo_with_no_phrase(self):
        player = Player({"number": 1, "name": "Tonyn Stallone"})
        combo = ""
        with self.assertRaises(AttributeError):
            player.read_combo(combo)
