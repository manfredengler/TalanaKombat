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