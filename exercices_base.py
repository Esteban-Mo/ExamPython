import time
import functools
from typing import Generator, List
from exceptions import InvalidDataError
import sys
import re

def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """Générateur de nombres de Fibonacci jusqu'à une limite donnée"""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

class StringIterator:
    """Itérateur pour convertir des chaînes en majuscules"""
    def __init__(self, strings: List[str]):
        self.strings = strings
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> str:
        if self.index >= len(self.strings):
            raise StopIteration
        result = self.strings[self.index].upper()
        self.index += 1
        return result

def execution_timer(func):
    """Décorateur pour mesurer le temps d'exécution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        debut = time.time()
        resultat = func(*args, **kwargs)
        fin = time.time()
        print(f"Temps d'exécution de {func.__name__}: {fin - debut:.4f} secondes")
        return resultat
    return wrapper

def read_numeric_file(filename: str) -> List[float]:
    """Lit un fichier contenant des données numériques"""
    numbers = []
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                value = float(line.strip())
                numbers.append(value)
            except ValueError:
                raise InvalidDataError(f"Ligne {line_num}: données non numériques détectées")
    return numbers 

def compare_memory_usage():
    numbers_list = list(range(1000000))
    numbers_gen = (x for x in range(1000000))
    
    print(f"Liste: {sys.getsizeof(numbers_list)} bytes")
    print(f"Générateur: {sys.getsizeof(numbers_gen)} bytes")

def validate_phone(text):
    pattern = r'^\+\d{1,3}[-\s]?\d{1,14}$'
    return bool(re.match(pattern, text))

def extract_emails(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

class UnderscoreMetaclass(type):
    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if callable(value) and not key.startswith('_'):
                raise ValueError(f"La méthode {key} doit commencer par un underscore")
        return super().__new__(cls, name, bases, dct)