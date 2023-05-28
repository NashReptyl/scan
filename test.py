import tweepy
import requests
from bs4 import BeautifulSoup
import time

# Clés d'accès à l'API Twitter
bearer='AAAAAAAAAAAAAAAAAAAAAF88nwEAAAAATw0r6XIz63hlh2p9hL7eHRQ%2Bb48%3DfS0ff3ik1acX4l54c5tVW5NcEEuXvTEgfqwkuhTTUGLWh0lUdj'
consumer_key = 'I2LbMWoVqpzGbTMUud7ye4Qgk'
consumer_secret = '3uUmpD3tfsLvdt4WzawBJX6mDRv4qxrdGiVR3LWXr7EzIFVuTt'
access_token = '1662587430539493376-jBSwx86BJ82N5FbfMEW1ntnpuJClZ3'
access_token_secret = '1XUyLjX3R1b5velJq4SrUZ6PwYspwepqMBETJUreEjBgu'

# Configuration de l'API Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.Client(bearer_token=bearer,
                    access_token=access_token,
                    access_token_secret=access_token_secret,
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret)
LIST_MANGAS = ["Black Clover",
               "Jujutsu Kaisen",
               "Killing Killer"]

# Fonction pour tweeter les scans
def tweet_latest_scan(j):
    # Récupération des scans à partir du site japscan
    news_url = 'https://www.japscan.lol/'
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraction du conteneur des nouveaux scans
    container = soup.find('div', id="tab-1")
    scan_div = container.find_all('div', class_='py-1')

    # Vérification des derniers scans tweetés
    with open('scans_tweetes.txt', 'r', encoding='utf-8') as file:
        scans_tweetes = [line.strip() for line in file.readlines()]

    # Publier uniquement les nouveaux scans
    for scan in scan_div:
        titre = scan.find('h3', class_='mb-0').find('a')['title']
        chapitre = scan.find('div', class_='mb-0').find('a')['title']
        if titre in LIST_MANGAS:
            if (titre+'/'+chapitre) not in scans_tweetes:
                print(f'Titre : {titre} / {chapitre}')

                #Faire le tweet
                #api.create_tweet(text='Nouveau scan de '+titre+' '+chapitre+'.')
                time.sleep(2)
                                
                # Ajouter le scan à la liste des scans publiés
                scans_tweetes.append(titre+'/'+chapitre)

    # Enregistrer les scans dans le fichier
    with open('scans_tweetes.txt', 'w',encoding='utf-8') as file:
        file.write('\n'.join(scans_tweetes))

    print('Tous les nouveaux tweets ont été publiés !')


# Exécuter en boucle
n=1
while True:
    tweet_latest_scan(n)
    n=n+1
    time.sleep(100) 
