class EmptySteps(ValueError):
    """Se esperaban ambos diccionarios: movimientos y golpes"""
    def __init__(self, message):
        super().__init__(message)
