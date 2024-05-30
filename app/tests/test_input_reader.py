import unittest
from unittest.mock import mock_open, patch
import json
from input_reader import read_input

class TestReadInput(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_input(self, mock_file):
        expected_result = {"key": "value"}
        result = read_input(filename="ejemplo_1")
        
        # Comprueba que se llama a open con el archivo correcto
        mock_file.assert_called_with(file='./input/ejemplo_1.json', mode='r')

        # Comprueba que el resultado es el esperado
        self.assertEqual(result, expected_result)