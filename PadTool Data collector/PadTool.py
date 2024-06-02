import requests
import time
import os

# URL du fichier JSON
url_json = "https://paas-out-dc2.rplusd.io/f72a8b9c-2b87-41bd-8501-0c387fd12ed8/"

# Chemins des dossiers de destination
dls_path = "/home/odr/config/mot/P04/dls.dls"
slide_folder_path = "/home/odr/config/mot/P04/slide/"

def download_image(image_url, save_path):
    # Construire le chemin complet du fichier image à sauvegarder
    save_path = os.path.join(save_path, "slide.jpg")
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)

def fetch_and_save_data():
    response = requests.get(url_json)
    if response.status_code == 200:
        data = response.json()
        if "artist" in data and "title" in data and "slide" in data:
            artist_title = f"{data['artist']} - {data['title']}"
            slide_url = data["slide"]

            # Écrire artiste et titre dans le fichier dls.dls
            with open(dls_path, 'w') as file:
                file.write(artist_title)

            # Télécharger et sauvegarder l'image
            download_image(slide_url, slide_folder_path)
            print(f"Data saved: {artist_title}, image downloaded to {slide_folder_path}/slide.jpg")
        else:
            print("Required data not found in JSON.")
    else:
        print("Failed to fetch data.")

# Exécuter la tâche toutes les 30 secondes
while True:
    fetch_and_save_data()
    time.sleep(30)

