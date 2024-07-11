import pandas as pd

# Charger les données depuis le fichier Excel
excel_chemin = 'C:/Users/arobin/Documents/projet/Projet Claire-Philippe-Kyota.xlsx'
sheet_name = 'Données brutes'  # Remplacez par le nom de la feuille dans Excel

# Lire les données
df = pd.read_excel(excel_chemin, sheet_name=sheet_name)

# Sauvegarder les données en CSV
csv_file_path = 'C:/Users/arobin/Documents/projet/recuperation.csv'
df.to_csv(csv_file_path, index=False)

print(f"CSV file saved to: {csv_file_path}")




# Chemin du fichier Excel et CSV
excel_chemin = r'C:\Users\arobin\Documents\projet\Projet Claire-Philippe-Kyota.xlsx'
csv_file_path = r'C:\Users\arobin\Documents\projet\recuperation.csv'
csv_file_path_corrected = r'C:\Users\arobin\Documents\projet\recuperation_corrected.csv'

# Charger les données depuis le fichier Excel
sheet_name = 'Données brutes'  # Remplacez par le nom de la feuille dans Excel
df = pd.read_excel(excel_chemin, sheet_name=sheet_name)

# Sauvegarder les données en CSV
df.to_csv(csv_file_path, index=False)
print(f"CSV file saved to: {csv_file_path}")

# Lire le fichier CSV
df = pd.read_csv(csv_file_path)

# Afficher les premières lignes du dataframe
print("Premières lignes du dataframe :")
print(df.head())

# Afficher les types de données par colonne
print("\nTypes de données par colonne :")
print(df.dtypes)

# Vérifier les valeurs manquantes
missing_values = df.isnull().sum()
print("\nValeurs manquantes par colonne :")
print(missing_values)

# Afficher des statistiques descriptives pour comprendre la distribution des données
print("\nStatistiques descriptives :")
print(df.describe(include='all'))

# Identifier les valeurs uniques dans chaque colonne pour détecter les anomalies
for column in df.columns:
    unique_values = df[column].unique()
    print(f"\nValeurs uniques dans la colonne '{column}' :")
    print(unique_values)

# Remplacer les valeurs manquantes par une valeur par défaut
df.fillna('Valeur par défaut', inplace=True)

# Exemple de conversion des colonnes au type de données correct
# Convertir la colonne 'Capacité' en numérique
df['Capacité'] = pd.to_numeric(df['Capacité'], errors='coerce')

# Exemple de conversion d'une colonne de date si nécessaire
# df['colonne_date'] = pd.to_datetime(df['colonne_date'], errors='coerce')

# Corriger les valeurs incorrectes dans une colonne spécifique si nécessaire
# Exemple : remplacer 'Autre' par 'Correct'
# df['Type d\'établissement'].replace('Autre', 'Correct', inplace=True)

# Sauvegarder les données corrigées en CSV
df.to_csv(csv_file_path_corrected, index=False)
print(f"\nCSV file saved to: {csv_file_path_corrected}")

# Lire le fichier CSV corrigé
df_corrected = pd.read_csv(csv_file_path_corrected)

# Vérifier les données corrigées
print("\nPremières lignes du dataframe corrigé :")
print(df_corrected.head())
