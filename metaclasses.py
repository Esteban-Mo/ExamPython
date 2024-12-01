class UnderscoreMethodsMetaclass(type):
    """Métaclasse vérifiant que toutes les méthodes commencent par un underscore"""
    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if callable(value) and not key.startswith('_'):
                raise ValueError(
                    f"La méthode {key} doit commencer par un underscore"
                )
        return super().__new__(cls, name, bases, dct) 