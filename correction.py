import pandas as pd

# Chemin du fichier Excel et CSV
excel_chemin = r'C:\Users\arobin\Documents\projet\Projet Claire-Philippe-Kyota.xlsx'
csv_file_path = r'C:\Users\arobin\Documents\projet\recuperation.csv'
csv_file_path_corrected = r'C:\Users\arobin\Documents\projet\recuperation_corrected.csv'
excel_chemin_corrige = r'C:\Users\arobin\Documents\projet\Projet Claire-Philippe-Kyota_Corrige.xlsx'

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

# Supprimer les lignes et colonnes vides
df.dropna(how='all', inplace=True)  # Supprimer les lignes vides
df.dropna(axis=1, how='all', inplace=True)  # Supprimer les colonnes vides

# Supprimer les colonnes indésirables
columns_to_keep = ['Région', 'Département', 'Type d\'établissement', 'Association / Fondation', 'Nom de l\'établissement', 'Capacité', 'Descrption']
df = df[columns_to_keep]

# Remplacer les valeurs manquantes par une valeur par défaut
df.fillna('Valeur par défaut', inplace=True)

# Conversion de la colonne 'Capacité' en numérique
df['Capacité'] = pd.to_numeric(df['Capacité'], errors='coerce')

# Corriger les valeurs incorrectes dans 'Type d\'établissement'
df['Type d\'établissement'] = df['Type d\'établissement'].str.strip()
df['Type d\'établissement'].replace({
    'Centre Educatif ': 'Centre Educatif',
    # Ajoutez d'autres corrections si nécessaire
}, inplace=True)

# Sauvegarder les données corrigées en CSV
df.to_csv(csv_file_path_corrected, index=False)
print(f"\nCSV file saved to: {csv_file_path_corrected}")

# Lire le fichier CSV corrigé
df_corrected = pd.read_csv(csv_file_path_corrected)

# Vérifier les données corrigées
print("\nPremières lignes du dataframe corrigé :")
print(df_corrected.head())

# Sauvegarder les données corrigées en Excel
with pd.ExcelWriter(excel_chemin_corrige, engine='openpyxl') as writer:
    df_corrected.to_excel(writer, index=False, sheet_name=sheet_name)

print(f"\nFichier Excel corrigé sauvegardé sous : {excel_chemin_corrige}")


# Corriger les valeurs incorrectes dans les colonnes spécifiques
# Ajouter des corrections manuelles si nécessaire
df['Région'] = df['Région'].str.strip()
df['Département'] = df['Département'].str.strip()
df['Type d\'établissement'] = df['Type d\'établissement'].str.strip()
df['Association / Fondation'] = df['Association / Fondation'].str.strip()
df['Nom de l\'établissement'] = df['Nom de l\'établissement'].str.strip()

# Vérifiez les valeurs uniques après correction pour vous assurer que tout est en ordre
for column in df.columns:
    unique_values = df[column].unique()
    print(f"\nValeurs uniques dans la colonne '{column}' après correction :")
    print(unique_values)
