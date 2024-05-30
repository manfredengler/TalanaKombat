def get_steps(steps:dict):
    """Obtiene un dict con movimientos y golpes y devuelve una lista de tuplas con forma [movimiento, golpe]"""
    return list(zip(steps.get("movimientos"), steps.get("golpes")))