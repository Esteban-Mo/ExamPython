from dataclasses import dataclass
from typing import List

@dataclass
class Livre:
    titre: str
    auteur: str
    isbn: str
    disponible: bool = True

class Bibliotheque:
    def __init__(self):
        self.livres: List[Livre] = []
    
    def ajouter_livre(self, livre: Livre) -> None:
        self.livres.append(livre)
    
    def supprimer_livre(self, isbn: str) -> None:
        self.livres = [l for l in self.livres if l.isbn != isbn]
    
    def rechercher_par_titre(self, titre: str) -> List[Livre]:
        return [l for l in self.livres if titre.lower() in l.titre.lower()]
    
    def rechercher_par_auteur(self, auteur: str) -> List[Livre]:
        return [l for l in self.livres if auteur.lower() in l.auteur.lower()]
    
    def emprunter_livre(self, isbn: str) -> None:
        livre = next((l for l in self.livres if l.isbn == isbn), None)
        if not livre:
            raise ValueError("Livre non trouvé")
        if not livre.disponible:
            raise ValueError("Livre déjà emprunté")
        livre.disponible = False
    
    def retourner_livre(self, isbn: str) -> None:
        livre = next((l for l in self.livres if l.isbn == isbn), None)
        if not livre:
            raise ValueError("Livre non trouvé")
        livre.disponible = True 