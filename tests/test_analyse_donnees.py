import unittest
import pandas as pd
from analyse_donnees import AnalyseDonnees, VisualisationApp

class TestAnalyseDonnees(unittest.TestCase):
    def setUp(self):
        """Préparation des données de test"""
        self.df_test = pd.DataFrame({
            'date': ['2023-01-15', '2023-01-16'],
            'produit': ['Ordinateur', 'Smartphone'],
            'prix_unitaire': [999.99, 599.99],
            'quantite': [5, 10],
            'region': ['Paris', 'Lyon'],
            'vendeur': ['Jean Dupont', 'Marie Martin']
        })
        self.analyse = AnalyseDonnees(self.df_test)

    def test_creation_analyse(self):
        """Test de la création de l'objet AnalyseDonnees"""
        self.assertIsInstance(self.analyse, AnalyseDonnees)
        self.assertIsInstance(self.analyse.df, pd.DataFrame)

    def test_structure_donnees(self):
        """Test de la structure des données"""
        colonnes_attendues = ['date', 'produit', 'prix_unitaire', 'quantite', 'region', 'vendeur']
        self.assertListEqual(list(self.analyse.df.columns), colonnes_attendues)

    def test_types_donnees(self):
        """Test des types de données"""
        self.assertEqual(self.analyse.df['prix_unitaire'].dtype, 'float64')
        self.assertEqual(self.analyse.df['quantite'].dtype, 'int64')

class TestVisualisationApp(unittest.TestCase):
    def setUp(self):
        """Préparation des données de test"""
        self.df_test = pd.DataFrame({
            'date': ['2023-01-15', '2023-01-16'],
            'produit': ['Ordinateur', 'Smartphone'],
            'prix_unitaire': [999.99, 599.99],
            'quantite': [5, 10],
            'region': ['Paris', 'Lyon'],
            'vendeur': ['Jean Dupont', 'Marie Martin']
        })

    def test_creation_app(self):
        """Test de la création de l'application"""
        app = VisualisationApp(self.df_test)
        self.assertIsNotNone(app.root)
        self.assertIsNotNone(app.fig)
        self.assertIsNotNone(app.ax)
        app.root.destroy()

if __name__ == '__main__':
    unittest.main()