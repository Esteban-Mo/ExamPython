class InvalidDataError(Exception):
    """Exception personnalisée pour les données invalides"""
    def __init__(self, message="Données invalides détectées"):
        self.message = message
        super().__init__(self.message) 