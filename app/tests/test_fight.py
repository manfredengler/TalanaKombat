from typing import Literal
import unittest
from unittest.mock import patch, Mock, call
from fight import (
    get_steps,
    zip_steps,
    Player,
    is_player_1_starter,
    ends_with_word,
    fight_loop,
)
from errors.fight import EmptySteps
from constants import (
    HABILITIES,
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


class TestFindCombo(unittest.TestCase):
    def test_find_composed_combo(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)
        strike = "K"
        movements = "ASDAWWDASDASD"
        expected_combo_text = "conecta un Remuyuken"
        expected_damage = 2

        new_movements, combo, damage = player.find_combo(movements, strike)

        self.assertEqual(new_movements, "ASDAWWDASDA")
        self.assertEqual(combo, expected_combo_text)
        self.assertEqual(damage, expected_damage)

    def test_simple_combo(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)
        strike = f"P"
        movements = "ASDAWWDASDASD"
        expected_combo_text = "le da un puñetazo al pobre Arnaldor"
        expected_damage = 1

        new_movements, combo, damage = player.find_combo(movements, strike)

        self.assertEqual(new_movements, movements)
        self.assertEqual(combo, expected_combo_text)
        self.assertEqual(damage, expected_damage)

    def test_no_combo(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)
        strike = ""
        movements = "ASDAWWDASDASD"
        expected_combo_text = ""
        expected_damage = 0

        new_movements, combo, damage = player.find_combo(movements, strike)

        self.assertEqual(new_movements, movements)
        self.assertEqual(combo, expected_combo_text)
        self.assertEqual(damage, expected_damage)


class TestRunStep(unittest.TestCase):
    def test_run_step_with_only_combo(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)
        strike = f"P"
        movements = ""
        step = (movements, strike)
        expected_phrase = "Tonyn le da un puñetazo al pobre Arnaldor"
        expected_damage = 1

        phrase, damage = player.run_step(step)

        self.assertEqual(phrase, expected_phrase)
        self.assertEqual(damage, expected_damage)

    def test_run_step_with_combo_and_movement(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)
        strike = f"P"
        movements = "ASDAWWDASDASD"
        step = (movements, strike)
        expected_phrase = "Tonyn se mueve y le da un puñetazo al pobre Arnaldor"
        expected_damage = 1

        phrase, damage = player.run_step(step)

        self.assertEqual(phrase, expected_phrase)
        self.assertEqual(damage, expected_damage)

    def test_run_step_with_movement_and_without_combo(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)
        movements = "SAS"
        strike = ""
        step: tuple[Literal["SAS"], Literal[""]] = (movements, strike)
        expected_phrase = "Tonyn se mueve"
        expected_damage = 0

        phrase, damage = player.run_step(step)

        self.assertEqual(phrase, expected_phrase)
        self.assertEqual(damage, expected_damage)

    def test_run_step_with_simple_movement(self):
        data = {"number": 1, "name": "Tonyn Stallone"}
        player = Player(data)
        movements = "D"
        strike = ""
        step = (movements, strike)
        expected_phrase = "Tonyn avanza"
        expected_damage = 0

        phrase, damage = player.run_step(step)

        self.assertEqual(phrase, expected_phrase)
        self.assertEqual(damage, expected_damage)


class TestDealDamage(unittest.TestCase):

    def test_deal_damage_less_than_life(self):
        player = Player(data={"name": "Arnaldor Shuatseneguer", "number": 1})
        self.assertFalse(player.deal_damage(2))
        self.assertEqual(player.life, 4)

    def test_deal_damage_equal_to_life(self):
        player = Player(data={"name": "Tonyn Stallone", "number": 1})
        self.assertTrue(player.deal_damage(6))
        self.assertEqual(player.life, 0)

    def test_deal_damage_more_than_life(self):
        player = Player(data={"name": "Arnaldor Shuatseneguer", "number": 1})
        self.assertTrue(player.deal_damage(10))
        self.assertEqual(player.life, -4)


class TestFightLoop(unittest.TestCase):
    def test_fight_loop_player1_wins(self):
        player_1 = Player(data={"name": "Tonyn Stallone", "number": 1})
        player_2 = Player(data={"name": "Arnaldor Shuatseneguer", "number": 2})
        steps = [
            (("SDD", "K"), ("DSD", "P")),
            (("DSD", "P"), ("WSAW", "K")),
            (("SA", "K"), ("ASA", "K")),
            (("DSD", "P"), ("", "K")),
            (["", ""], ("ASA", "P")),
            (["", ""], ("SA", "k")),
        ]
        fight_loop(steps, player_1=player_1, player_2=player_2)
        self.assertEqual(player_1.life, 1)
        self.assertEqual(player_2.life, -2)

    def test_fight_loop_player2_wins(self):
        player_1 = Player(data={"name": "Tonyn Stallone", "number": 1})
        player_2 = Player(data={"name": "Arnaldor Shuatseneguer", "number": 2})
        steps = [
            (("DSD", "P"), ("", "P")),
            (("S", ""), ("ASA", "")),
            (["", ""], ("DA", "P")),
            (["", ""], ("AAA", "K")),
            (["", ""], ("", "K")),
            (["", ""], ("SA", "K")),
        ]
        fight_loop(steps, player_1=player_1, player_2=player_2)
        self.assertEqual(player_1.life, -1)
        self.assertEqual(player_2.life, 3)

    def test_fight_loop_ends_with_less_instrucctions__player1_wins(self):
        player_1 = Player(data={"name": "Tonyn Stallone", "number": 1})
        player_2 = Player(data={"name": "Arnaldor Shuatseneguer", "number": 2})
        steps = [
            (("DSD", "P"), ("", "P")),
            (("S", ""), ("ASA", "")),
        ]
        fight_loop(steps, player_1=player_1, player_2=player_2)
        self.assertEqual(player_1.life, 5)
        self.assertEqual(player_2.life, 3)

    def test_fight_loop_ends_with_less_instrucctions__player2_wins(self):
        player_1 = Player(data={"name": "Tonyn Stallone", "number": 1})
        player_2 = Player(data={"name": "Arnaldor Shuatseneguer", "number": 2})
        steps = [
            (("SDD", "K"), ("DSDASA", "P")),
        ]
        fight_loop(steps, player_1=player_1, player_2=player_2)
        self.assertEqual(player_1.life, 4)
        self.assertEqual(player_2.life, 5)

    def test_fight_loop_ends_with_less_instrucctions__draw(self):
        player_1 = Player(data={"name": "Tonyn Stallone", "number": 1})
        player_2 = Player(data={"name": "Arnaldor Shuatseneguer", "number": 2})
        steps = [
            (("SDD", "K"), ("DSD", "P")),
            (("DSD", "P"), ("WSAW", "K")),
            (("SA", "K"), ("ASA", "K")),
        ]
        fight_loop(steps, player_1=player_1, player_2=player_2)
        self.assertEqual(player_1.life, 1)
        self.assertEqual(player_2.life, 1)
