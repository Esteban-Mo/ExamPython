from analyse_donnees import AnalyseDonnees

def main():
    try:
        analyse = AnalyseDonnees("donnees.csv")
        analyse.explorer_donnees()
        analyse.nettoyer_donnees()
        
        colonnes_pour_clustering = ['prix_unitaire', 'quantite']
        df_segmente, centres = analyse.segmenter_donnees(colonnes_pour_clustering)
        
        print("\nRésultats de la segmentation par région et type de produit:")
        print(df_segmente.groupby(['Cluster', 'region', 'produit']).size().unstack(fill_value=0))
        
        print("\nAffichage des graphiques...")
        analyse.visualiser_donnees()
        
    except FileNotFoundError:
        print("Fichier de données non trouvé")
    except Exception as e:
        print(f"Une erreur est survenue: {str(e)}")
        
    input("\nAppuyez sur Entrée pour fermer les graphiques...")

if __name__ == "__main__":
    main() 