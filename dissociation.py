import pandas as pd
import os
from google.cloud import storage
from google.oauth2 import service_account
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut

# Remplacez par votre clé API Google
google_api_key = 'AIzaSyCX2Zuba7Tvb4uJbMKrcIRW749ElrWyhB0'

# Chemin du fichier JSON du compte de service Google Cloud
service_account_json = 'C:/Users/arobin/Documents/projet/service_account.json'

# Initialiser le géocodeur
geolocator = GoogleV3(api_key=google_api_key)

# Authentification avec le compte de service
credentials = service_account.Credentials.from_service_account_file(service_account_json)
client = storage.Client(credentials=credentials)
bucket_name = 'carto_acteur'
bucket = client.get_bucket(bucket_name)

# Fonction pour géocoder une adresse avec des tentatives répétées en cas de timeout
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return geocode_address(address)

# Chemin du fichier Excel source
excel_chemin = r'C:\Users\arobin\Documents\projet\Projet Claire-Philippe-Kyota.xlsx'

# Créer un répertoire pour stocker les fichiers Excel temporairement
local_output_dir = r'C:\Users\arobin\Documents\projet\departements_excels'
if not os.path.exists(local_output_dir):
    os.makedirs(local_output_dir)

# Charger les données depuis le fichier Excel
sheet_name = 'Données brutes'  # Remplacez par le nom de la feuille dans Excel
df = pd.read_excel(excel_chemin, sheet_name=sheet_name)

# Supprimer les lignes vides
df.dropna(how='all', inplace=True)

# Supprimer les colonnes vides
df.dropna(axis=1, how='all', inplace=True)

# Remplacer les valeurs manquantes par une valeur par défaut
df.fillna('Valeur par défaut', inplace=True)

# Conversion de la colonne 'Capacité' en numérique
df['Capacité'] = pd.to_numeric(df['Capacité'], errors='coerce')

# Corriger les valeurs incorrectes dans 'Type d\'établissement'
df['Type d\'établissement'] = df['Type d\'établissement'].str.strip().replace({
    'Centre Educatif ': 'Centre Educatif',
    # Ajoutez d'autres corrections si nécessaire
})

# Ajouter des colonnes pour Latitude et Longitude
df['Latitude'] = None
df['Longitude'] = None

# Géocoder chaque établissement
for idx, row in df.iterrows():
    address = f"{row['Nom de l\'établissement']}, {row['Département']}, {row['Région']}, France"
    print(f"Géocodage de l'adresse : {address}")
    location = geocode_address(address)
    if location:
        df.at[idx, 'Latitude'] = location[0]
        df.at[idx, 'Longitude'] = location[1]

# Sauvegarder les données géocodées pour utilisation ultérieure
geocoded_excel_path = r'C:\Users\arobin\Documents\projet\Projet Claire-Philippe-Kyota_Geocoded.xlsx'
df.to_excel(geocoded_excel_path, index=False)
print(f"Données géocodées sauvegardées sous : {geocoded_excel_path}")

# Liste des départements uniques
departements = df['Département'].unique()

# Créer un fichier Excel distinct pour chaque département
for departement in departements:
    df_departement = df[df['Département'] == departement]
    
    # Sauvegarder le département dans un fichier Excel séparé localement
    local_output_path = os.path.join(local_output_dir, f'{departement}.xlsx')
    df_departement.to_excel(local_output_path, index=False, sheet_name=departement[:30])  # Limiter le nom de la feuille à 30 caractères
    print(f"Fichier Excel créé pour le département {departement} : {local_output_path}")

    # Télécharger le fichier sur Google Cloud Storage
    blob = bucket.blob(f'{departement}.xlsx')
    blob.upload_from_filename(local_output_path)
    print(f"Fichier {local_output_path} téléchargé sur Google Cloud Storage dans le bucket {bucket_name}")

print(f"Tous les fichiers Excel par département ont été sauvegardés dans le bucket Google Cloud Storage : {bucket_name}")
