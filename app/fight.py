import re
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

    def read_movements(self, movements: str):
        return self.movement_interpreter.get(
            movements, self.movement_interpreter["DEFAULT"]
        )

    def read_combo(self, combo: str):
        """Retorna el daño y el relato del combo"""
        data = self.combos.get(combo)
        return data.get("damage"), data.get("phrase")
    
    def find_combo(self, movements:str, strike:str):
        """Se asume que el botón de golpe es justo después de la secuencia de movimiento, 
        por ende busca con regex si existe un combo al final de las instrucciones, 
        si cumple lo enuncia y lo retira de las instrucciones, entregando los movimientos iniciales si hay"""
        joined_instructions = movements+strike
        combo = ""
        damage = 0
        for key in self.combos.keys():
            if ends_with_word(text=joined_instructions, keyword=key):
                damage, combo = self.read_combo(combo=key)
                joined_instructions = joined_instructions.removesuffix(key)
        return joined_instructions, combo, damage
    
    def run_step(self, step:tuple[str]):
        """Retorna el relato del turno y si se ejecuto un combo el daño que hizo con este"""
        movements, strike = step

        # Formamos el enunciado uniendo strings partiendo por el nombre del jugador correspondiente
        phrase = self.name

        # Vemos si hay un combo al final de los movimientos, actualizamos la secuencia si coincide
        # Vemos si quedan movimientos luego de intentar obtener un combo y añadimos su relato
        if new_movements:
            phrase += " " + self.read_movements(movements=new_movements)
            if combo:
                phrase += " y "
        else:
            phrase += " "

        # Añadimos el combo al relato si existe
        phrase += combo if combo else ""

        return phrase, damage

    def deal_damage(self, damage: int):
        """Recibe daño aplicado, si la vida resultante es menor que 0 retorna True por lo contrario False"""
        self.life -= damage
        return self.life <= 0


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

def ends_with_word(text:str, keyword:str) -> bool:
    """Revisa si una frase incluye al final una palabra clave"""
    reg = rf"{keyword}\b$"
    return re.search(reg, text) is not None


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

    for step in steps:
        # Por cada turno, ambos jugadores realizan su combinacion de teclas
        for _ in range(2):
            if player_turn:
                # Si player turn es True usamos al jugador 1
                player = player_1
                phrase, damage = player.run_step(step[0])
                finish = player_2.deal_damage(damage=damage)
            else:
                # por el contrario usamos al jugador 2
                player = player_2
                phrase, damage = player.run_step(step[1])
                finish = player_1.deal_damage(damage=damage)

            print(phrase)

            if finish:
                print(
                    f"{player.name} Gana la pelea y aun le queda {player.life} de energía"
                )
                return

            player_turn = not player_turn