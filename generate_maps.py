import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim
import os

# Définir le chemin vers votre fichier Excel
excel_path = 'C:/Users/arobin/Documents/projet/Projet Claire-Philippe-Kyota.xlsx'

# Lire le fichier Excel
df = pd.read_excel(excel_path)

# Nettoyer les données (supprimer les colonnes Unnamed)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="geoapiExercises")

# Fonction de géocodage
def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Ajouter des colonnes de latitude et de longitude si elles n'existent pas
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    df['Latitude'], df['Longitude'] = zip(*df.apply(lambda row: geocode_address(f"{row['Nom de l\'établissement']}, {row['Département']}, {row['Région']}, France"), axis=1))

# Créer un objet GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# Créer un répertoire pour les fichiers GeoJSON
if not os.path.exists('geojson'):
    os.makedirs('geojson')

# Enregistrer les fichiers GeoJSON pour chaque département
for department in df['Département'].unique():
    dept_gdf = gdf[gdf['Département'] == department]
    dept_gdf.to_file(f"geojson/{department}.geojson", driver='GeoJSON')

# Créer la carte Folium
map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

# Ajouter les départements à la carte
for department in df['Département'].unique():
    folium.GeoJson(f"geojson/{department}.geojson", name=department).add_to(map)

# Enregistrer la carte
map.save('templates/map.html')
