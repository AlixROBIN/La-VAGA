from django.shortcuts import render
import pandas as pd
import json
from google.cloud import storage
import os
import tempfile
from google.auth.exceptions import DefaultCredentialsError
from google.api_core.exceptions import NotFound

def index(request):
    try:
        # Configuration de l'authentification
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/arobin/Documents/projet/service_account.json"

        # Nom du bucket
        bucket_name = "carto_acteur"

        # Créer un client de stockage
        client = storage.Client()

        # Obtenir le bucket
        bucket = client.bucket(bucket_name)

        # Lister tous les blobs (fichiers) dans le bucket
        blobs = bucket.list_blobs()

        # Créer un répertoire temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            all_data = []
            for blob in blobs:
                file_path = os.path.join(temp_dir, blob.name)
                try:
                    blob.download_to_filename(file_path)
                    df = pd.read_excel(file_path)
                    all_data.append(df)
                except NotFound:
                    return render(request, 'error.html', {'error': f"Le fichier {blob.name} n'a pas été trouvé dans le bucket {bucket_name}."})
                except Exception as e:
                    return render(request, 'error.html', {'error': f"Erreur lors du téléchargement du fichier {blob.name} : {str(e)}"})

            if not all_data:
                return render(request, 'error.html', {'error': "Aucun fichier trouvé dans le bucket."})

            # Concaténer toutes les données
            df = pd.concat(all_data, ignore_index=True)

            # Supprimer les colonnes non nécessaires
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Afficher les noms de colonnes disponibles pour le diagnostic
            print("Colonnes disponibles dans le dataframe :", df.columns.tolist())

            # Vérifier si 'Région' et 'Latitude' et 'Longitude' sont des colonnes
            if 'Région' not in df.columns or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
                raise KeyError("'Région', 'Latitude' et 'Longitude' ne sont pas des colonnes disponibles dans le dataframe.")

            # Préparer les données pour les régions et départements
            regions = {}
            for _, row in df.iterrows():
                region = row['Région']
                department = row['Département']
                establishment = row["Nom de l'établissement"]
                latitude = row['Latitude']
                longitude = row['Longitude']

                if region not in regions:
                    regions[region] = {}

                if department not in regions[region]:
                    regions[region][department] = []

                regions[region][department].append({
                    "name": establishment,
                    "latitude": latitude,
                    "longitude": longitude
                })

            # Convertir le dictionnaire en format JSON
            regions_json = json.dumps(regions)
        
            return render(request, 'index.html', {'regions': regions_json})
    except DefaultCredentialsError as e:
        return render(request, 'error.html', {'error': f"Erreur d'authentification : {str(e)}"})
    except Exception as e:
        return render(request, 'error.html', {'error': f"Erreur générale : {str(e)}"})

