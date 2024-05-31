STARTING_DRAW_LIMIT = 2
DEFAULT_STARTING_PLAYER = 1
DEFAULT_LIFE = 6

PLAYER_1 = {
    "number" : 1,
    "name": "Tonyn Stallone"
}

PLAYER_2 = {
    "number" :2,
    "name": "Arnaldor Shuatseneguer"
}

HABILITIES = {
    "Tonyn Stallone": {
        "DSDP": {
            "name": "Taladoken",
            "damage": 3,
            "phrase": "usa un Taladoken"
        },
        "SDK": {
            "name": "Remuyuken",
            "damage": 2,
            "phrase": "conecta un Remuyuken"
        },
        "P": {
            "name": "Puño",
            "damage": 1,
            "phrase": "le da un puñetazo al pobre"
        },
        "K": {
            "name": "Patada",
            "damage": 1,
            "phrase": "da una patada"
        }
    },
    "Arnaldor Shuatseneguer" : {
        "SAK": {
            "name": "Remuyuken",
            "damage": 3,
            "phrase": "conecta un Remuyuken"
        },
        "ASAP": {
            "name": "Taladoken",
            "damage": 2,
            "phrase": "usa un Taladoken"
        },
        "P": {
            "name": "Puño",
            "damage": 1,
            "phrase": "da un puñetazo"
        },
        "K": {
            "name": "Patada",
            "damage": 1,
            "phrase": "da una patada"
        }
    },

}

MOVEMENT_INTERPRETER = {
    "Tonyn Stallone": {
        "W": "se levanta",
        "S": "se agacha",
        "D": "avanza",
        "A": "retrocede",
        "DEFAULT": "se mueve"}, 
    "Arnaldor Shuatseneguer": {
        "W": "se levanta",
        "S": "se agacha",
        "D": "retrocede",
        "A": "avanza",
        "DEFAULT": "se mueve"
    }
}