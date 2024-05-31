from itertools import zip_longest

from errors.fight import EmptySteps
from constants import PLAYER_1, PLAYER_2, HABILITIES, STARTING_DRAW_LIMIT, MOVEMENT_INTERPRETER, DEFAULT_LIFE

class Player:
    def __init__(self, data:dict):
        self.number = data.get("number")
        self.fullname = data.get("name")
        self.name = self.fullname.split(" ")[0]
        self.life = DEFAULT_LIFE
        self.combos = HABILITIES[self.fullname]
        self.movement_interpreter = MOVEMENT_INTERPRETER[self.fullname]


def get_steps(steps:dict):
    """Obtiene un dict con movimientos y golpes y devuelve una lista de tuplas con forma [movimiento, golpe]"""
    movements= steps.get("movimientos")
    strikes= steps.get("golpes")
    if movements is None or strikes is None:
        raise EmptySteps("Se esperaban ambos diccionarios: movimientos y golpes")
    
    if not isinstance(movements, list):
        raise TypeError("El valor de 'movimientos' debe ser una lista")
    
    if not isinstance(strikes, list):
        raise TypeError("El valor de 'golpes' debe ser una lista")
    return list(zip(movements, strikes))

def zip_steps(input_dict: dict):
    """Parea cada serie de combinaciones por jugador"""
    player_1_steps = get_steps(steps=input_dict.get("player1"))
    player_2_steps = get_steps(steps=input_dict.get("player2"))
    # El largo puede variar, por ende parea las restantes con un lista por defecto
    return list(zip_longest(player_1_steps, player_2_steps, fillvalue=["", ""]))

def is_player_1_starter(steps):
    """Intenta hasta el limite de intentos buscar quien inicia segun la menor combinacion de botones por turno"""
    for i, step in enumerate(steps[:STARTING_DRAW_LIMIT]):
        player_1_keys = "".join(step[0])
        player_2_keys = "".join(step[1])
        if len(player_1_keys) < len(player_2_keys):
            return True
        if len(player_1_keys) > len(player_2_keys):
            return False
    # si hay empate inicia el player 1 (total el player 2 siempre es del hermano chico)
    return True


def fight_loop(steps:list[tuple]):
    """Recorre cada step"""
    player_1 = Player(data=PLAYER_1)
    player_2 = Player(data=PLAYER_2)

    starter = is_player_1_starter(steps)
    player_turn = starter
