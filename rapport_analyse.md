# 📊 Rapport d'Analyse des Données

## 1. 🛠️ Étapes de Préparation des Données

### 1.1 📥 Collecte des Données
- Importation des données brutes depuis le fichier CSV contenant les ventes et données météo
- Vérification approfondie de la qualité et cohérence des 40 enregistrements
- Identification des éventuelles valeurs manquantes dans les colonnes prix, quantité et météo

### 1.2 🧹 Nettoyage des Données
- Traitement des valeurs manquantes par imputation ou suppression selon le contexte
- Correction des erreurs de saisie dans les noms de produits et régions
- Standardisation des formats de date et des unités de mesure (€, °C, mm)

### 1.3 ⚡ Transformation des Données
- Encodage des variables catégorielles (produits, régions, vendeurs)
- Normalisation des variables numériques (prix, température, pluviométrie)
- Création de nouvelles variables : chiffre d'affaires total, moyenne mobile des ventes

## 2. 📈 Graphiques et Analyses Descriptives

### 2.1 📊 Analyse Univariée
- Distribution des prix par type de produit (499€ à 1299€ pour les ordinateurs)
- Statistiques descriptives des ventes par région et par vendeur
- Identification des pics de vente inhabituels et conditions météo extrêmes

### 2.2 🔄 Analyse Bivariée
- Corrélations entre température et ventes de produits
- Tableaux croisés des ventes par vendeur et par région
- Visualisation de l'impact de la météo sur les performances commerciales

### 2.3 📉 Visualisations
- Histogrammes des distributions de prix et quantités
- Boîtes à moustaches comparant les ventes entre régions
- Graphiques de dispersion prix vs quantité avec segmentation

## 3. 🎯 Conclusions et Recommandations

### 3.1 💡 Principales Conclusions
- Forte saisonnalité des ventes d'ordinateurs et smartphones
- Impact significatif de la météo sur certaines catégories
- Performance exceptionnelle de certains vendeurs dans des régions spécifiques

### 3.2 📋 Recommandations
- Ajuster les stocks selon les prévisions météorologiques
- Optimiser la répartition des vendeurs par région
- Mettre en place des promotions ciblées selon la saison

### 3.3 ⚠️ Limites de l'Analyse
- Période d'observation limitée à 4 mois
- Données météo parfois incomplètes
- Besoin d'enrichir avec des données concurrentielles