from itertools import zip_longest
from errors.fight import EmptySteps

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

