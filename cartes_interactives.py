import os
import pandas as pd
import folium
from google.cloud import storage
from google.oauth2 import service_account
from folium.plugins import MarkerCluster

# Chemin du fichier JSON du compte de service Google Cloud
service_account_json = 'C:/Users/arobin/Documents/projet/service_account.json'

# Authentification avec le compte de service
credentials = service_account.Credentials.from_service_account_file(service_account_json)
client = storage.Client(credentials=credentials)
bucket_name = 'carto_acteur'
bucket = client.get_bucket(bucket_name)

# Créer un répertoire pour stocker les fichiers HTML temporairement
local_output_dir = r'C:\Users\arobin\Documents\projet\departements_maps'
if not os.path.exists(local_output_dir):
    os.makedirs(local_output_dir)

# Créer une carte Folium globale
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)  # Centré sur la France

# Créer des clusters pour chaque région et département
region_clusters = {}
department_clusters = {}

# Télécharger les fichiers Excel depuis Google Cloud Storage
blobs = bucket.list_blobs()

for blob in blobs:
    if blob.name.endswith('.xlsx'):
        local_excel_path = os.path.join(local_output_dir, blob.name)
        blob.download_to_filename(local_excel_path)
        print(f"Fichier téléchargé : {local_excel_path}")

        # Charger les données depuis le fichier Excel
        df = pd.read_excel(local_excel_path)

        # Supprimer les colonnes Unnamed
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Vérifier les colonnes disponibles
        print(f"Colonnes disponibles dans {blob.name}: {df.columns.tolist()}")

        region = df['Région'].iloc[0]
        department = df['Département'].iloc[0]

        if region not in region_clusters:
            region_clusters[region] = folium.FeatureGroup(name=region)
            m.add_child(region_clusters[region])

        if department not in department_clusters:
            department_clusters[department] = MarkerCluster(name=department).add_to(region_clusters[region])

        # Ajouter des marqueurs pour chaque établissement
        for idx, row in df.iterrows():
            if not pd.isna(row['Latitude']) and not pd.isna(row['Longitude']):
                popup_text = f"<b>{row['Nom de l\'établissement']}</b><br>"
                if 'Type d\'établissement' in df.columns:
                    popup_text += f"Type: {row['Type d\'établissement']}<br>"
                if 'Association / Fondation' in df.columns:
                    popup_text += f"Association: {row['Association / Fondation']}<br>"
                if 'Descrption' in df.columns:
                    popup_text += f"Description: {row['Descrption']}"

                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=popup_text,
                    tooltip=row['Nom de l\'établissement']
                ).add_to(department_clusters[department])

# Ajouter un contrôle de calques pour gérer l'affichage des régions et départements
folium.LayerControl().add_to(m)

# Générer le code HTML pour la liste des régions et départements
menu_html = '''
<div id="departement-menu">
    <div id="select-buttons">
        <button id="select-all">Tout sélectionner</button>
        <button id="deselect-all">Tout désélectionner</button>
    </div>
    <ul>
'''
for region in region_clusters.keys():
    menu_html += f'<li><input type="checkbox" id="{region}" checked onclick="toggleRegion(\'{region}\')"> <label for="{region}">{region}</label><ul class="region {region} hidden">'
    for department in department_clusters.keys():
        if department in department_clusters:
            menu_html += f'<li><input type="checkbox" id="{department}" checked onclick="toggleDepartment(\'{department}\')"> <label for="{department}">{department}</label><ul class="departement {department} hidden">'
            for idx, row in df.iterrows():
                if not pd.isna(row['Latitude']) and not pd.isna(row['Longitude']) and row['Département'] == department:
                    popup_text = f"<b>{row['Nom de l\'établissement']}</b><br>"
                    if 'Type d\'établissement' in df.columns:
                        popup_text += f"Type: {row['Type d\'établissement']}<br>"
                    if 'Association / Fondation' in df.columns:
                        popup_text += f"Association: {row['Association / Fondation']}<br>"
                    if 'Descrption' in df.columns:
                        popup_text += f"Description: {row['Descrption']}"
                    menu_html += f'<li class="lieu {department} hidden"><a href="#" onclick="showMarker({row["Latitude"]}, {row["Longitude"]}, \'{popup_text}\')">{row["Nom de l\'établissement"]}</a></li>'
            menu_html += '</ul></li>'
    menu_html += '</ul></li>'
menu_html += '</ul></div>'

# Ajouter le bouton pour ouvrir/fermer le menu
menu_toggle_html = '<div id="menu-toggle">Légende</div>'

# Ajouter le lien vers les fichiers JavaScript et CSS, et la liste des régions et départements au HTML de la carte
map_html = m.get_root().render()
map_html = map_html.replace('</body>', f'''
<link rel="stylesheet" href="styles.css">
<script src="toggle_departments.js"></script>
{menu_toggle_html}
{menu_html}
</body>
''')

# Enregistrer la carte sous
map_html = m.get_root().render()
map_html = map_html.replace('</body>', f'''
<link rel="stylesheet" href="styles.css">
<script src="toggle_departments.js"></script>
{menu_toggle_html}
{menu_html}
</body>
''')

# Enregistrer la carte sous forme de fichier HTML avec encodage UTF-8
html_map_path = os.path.join(local_output_dir, "carte_globale.html")
with open(html_map_path, 'w', encoding='utf-8') as f:
    f.write(map_html)
print(f"Carte globale enregistrée sous : {html_map_path}")
