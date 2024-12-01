import pandas as pd
import seaborn as sns
from typing import Tuple, List
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class AnalyseDonnees:
    def __init__(self, fichier: str):
        self.df = pd.read_csv(fichier)
    
    def explorer_donnees(self) -> None:
        """Affiche les informations de base sur le dataset"""
        print("Premières lignes:")
        print(self.df.head())
        print("\nInformations sur les colonnes:")
        print(self.df.info())
        print("\nStatistiques descriptives:")
        print(self.df.describe())
    
    def nettoyer_donnees(self) -> None:
        """Nettoie les données en gérant les valeurs manquantes et aberrantes"""
        self.df = self.df.dropna()
        
        colonnes_numeriques = self.df.select_dtypes(include=['int64', 'float64']).columns
        
        for colonne in colonnes_numeriques:
            Q1 = self.df[colonne].quantile(0.25)
            Q3 = self.df[colonne].quantile(0.75)
            IQR = Q3 - Q1
            condition = ~((self.df[colonne] < (Q1 - 1.5 * IQR)) | (self.df[colonne] > (Q3 + 1.5 * IQR)))
            self.df = self.df[condition]

    def analyser_correlations(self) -> pd.DataFrame:
        """
        Analyse les corrélations entre les variables numériques du dataset
        
        Returns:
            pd.DataFrame: Matrice de corrélation
        """
        colonnes_numeriques = self.df.select_dtypes(include=['int64', 'float64']).columns
        return self.df[colonnes_numeriques].corr()
    
    def segmenter_donnees(self, colonnes: List[str], n_clusters: int = 3) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Segmente les données en utilisant l'algorithme K-means
        
        Args:
            colonnes (list): Liste des colonnes à utiliser pour la segmentation
            n_clusters (int): Nombre de clusters souhaité
            
        Returns:
            tuple: (données avec clusters, centres des clusters)
        """
        X = self.df[colonnes].copy()
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Ajout des clusters au DataFrame
        self.df['Cluster'] = clusters
        
        centres_clusters = pd.DataFrame(
            scaler.inverse_transform(kmeans.cluster_centers_),
            columns=colonnes
        )
        
        return self.df, centres_clusters
    
    def analyser_clusters(self, df_clusters: pd.DataFrame) -> pd.DataFrame:
        """
        Analyse les caractéristiques de chaque cluster
        
        Args:
            df_clusters (pd.DataFrame): DataFrame avec les clusters assignés
            
        Returns:
            pd.DataFrame: Statistiques descriptives par cluster
        """
        colonnes_numeriques = df_clusters.select_dtypes(include=['int64', 'float64']).columns
        colonnes_numeriques = colonnes_numeriques.drop('Cluster') if 'Cluster' in colonnes_numeriques else colonnes_numeriques
        
        stats_clusters = []
        
        for cluster in df_clusters['Cluster'].unique():
            cluster_data = df_clusters[df_clusters['Cluster'] == cluster][colonnes_numeriques]
            stats = cluster_data.describe()
            stats['Cluster'] = cluster
            stats_clusters.append(stats)
            
        return pd.concat(stats_clusters, axis=0)
    
    def segmenter_villes_climat(self, n_clusters: int = 3) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Segmente les villes selon leurs caractéristiques climatiques
        
        Args:
            n_clusters (int): Nombre de clusters souhaité
            
        Returns:
            tuple: (données avec clusters, centres des clusters)
        """
        colonnes_climat = ['temperature_moy', 'pluviometrie', 'ensoleillement']
        X = self.df[['region'] + colonnes_climat].drop_duplicates()
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X[colonnes_climat])
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Création d'un DataFrame avec les résultats
        resultats = X.copy()
        resultats['Cluster_Climat'] = clusters
        
        centres_clusters = pd.DataFrame(
            scaler.inverse_transform(kmeans.cluster_centers_),
            columns=colonnes_climat
        )
        
        return resultats, centres_clusters

    class VisualisationManager:
        def __init__(self, df):
            self.df = df
            self.root = tk.Tk()
            self.root.title("Visualisation des données")
            self.root.state('zoomed')
            
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            self.style = ttk.Style()
            self.style.theme_use('clam')
            
            self.main_frame = ttk.Frame(self.root)
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            self.button_frame = ttk.Frame(self.main_frame)
            self.button_frame.pack(fill=tk.X, padx=5, pady=5)
            
            self.create_buttons()
            
            self.graph_frame = ttk.Frame(self.main_frame)
            self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            self.fig = Figure(figsize=(10, 6))
            self.ax = self.fig.add_subplot(111)
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
            self.toolbar.update()
            
            self.plot_correlation()
        
        def create_buttons(self):
            button_style = {'width': 15, 'padding': 5}
            
            ttk.Button(self.button_frame, text="Corrélations", 
                      command=self.plot_correlation, **button_style).pack(side=tk.LEFT, padx=5)
            ttk.Button(self.button_frame, text="Prix", 
                      command=self.plot_prix, **button_style).pack(side=tk.LEFT, padx=5)
            ttk.Button(self.button_frame, text="Quantités", 
                      command=self.plot_quantite, **button_style).pack(side=tk.LEFT, padx=5)
            ttk.Button(self.button_frame, text="Clusters", 
                      command=self.plot_clusters, **button_style).pack(side=tk.LEFT, padx=5)
        
        def clear_plot(self):
            self.fig.clear()
            self.ax = self.fig.add_subplot(111)
        
        def plot_correlation(self):
            self.clear_plot()
            colonnes_numeriques = self.df.select_dtypes(include=['int64', 'float64'])
            sns.heatmap(colonnes_numeriques.corr(), annot=True, cmap='coolwarm', 
                       ax=self.ax, cbar=True)
            self.ax.set_title("Matrice de corrélation des variables numériques")
            self.fig.tight_layout()
            self.canvas.draw()
        
        def plot_prix(self):
            self.clear_plot()
            sns.boxplot(x='produit', y='prix_unitaire', data=self.df, ax=self.ax)
            self.ax.set_title("Distribution des prix par produit")
            self.ax.tick_params(axis='x', rotation=45)
            self.fig.tight_layout()
            self.canvas.draw()
        
        def plot_quantite(self):
            self.clear_plot()
            sns.barplot(x='region', y='quantite', data=self.df, ax=self.ax)
            self.ax.set_title("Quantités vendues par région")
            self.ax.tick_params(axis='x', rotation=45)
            self.fig.tight_layout()
            self.canvas.draw()
            
        def plot_clusters(self):
            self.clear_plot()
            if 'Cluster' in self.df.columns:
                cols = self.df.select_dtypes(include=['int64', 'float64']).columns[:2]
                scatter = self.ax.scatter(
                    self.df[cols[0]], 
                    self.df[cols[1]], 
                    c=self.df['Cluster'], 
                    cmap='viridis'
                )
                self.fig.colorbar(scatter, ax=self.ax, label='Cluster')
                self.ax.set_title(f"Segmentation des données ({cols[0]} vs {cols[1]})")
                self.ax.set_xlabel(cols[0])
                self.ax.set_ylabel(cols[1])
            else:
                self.ax.text(0.5, 0.5, "Exécutez d'abord la segmentation des données", 
                           ha='center', va='center')
            self.fig.tight_layout()
            self.canvas.draw()
        
        def plot_clusters_climat(self):
            self.clear_plot()
            if 'Cluster_Climat' in self.df.columns:
                sns.scatterplot(
                    data=self.df.drop_duplicates('region'),
                    x='temperature_moy',
                    y='pluviometrie',
                    hue='Cluster_Climat',
                    size='ensoleillement',
                    ax=self.ax
                )
                self.ax.set_title("Segmentation des villes par climat")
            else:
                self.ax.text(0.5, 0.5, "Exécutez d'abord la segmentation climatique", 
                            ha='center', va='center')
            self.fig.tight_layout()
            self.canvas.draw()
        
        def on_closing(self):
            """Gère la fermeture propre de l'application"""
            self.root.quit()
            self.root.destroy()

    def visualiser_donnees(self) -> None:
        """Crée une interface graphique moderne pour la visualisation des données"""
        try:
            app = self.VisualisationManager(self.df)
            app.root.mainloop()
        except tk.TclError:
            pass