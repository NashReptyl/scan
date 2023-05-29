import os
import tweepy
import requests
from bs4 import BeautifulSoup
import time

# API Twitter variables d'access
bearer=os.environ.get('BEARER')
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# Creation client API
api = tweepy.Client(bearer_token=bearer,
                    access_token=access_token,
                    access_token_secret=access_token_secret,
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret)
LIST_MANGAS = ["Eternal Club",
               "Ao No Hako",
               "Forget Vivian"]

# Fonction pour tweeter les scans
def tweet_latest_japscan(j):
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
        chapitre = scan.find('div', class_='mb-0').find('a')['title'].split(":")[0]
        if titre in LIST_MANGAS:
            if (titre+'/'+chapitre) not in scans_tweetes:
                print(f'Titre : {titre} / {chapitre}')

                #Faire le tweet
                api.create_tweet(text='Le '+chapitre.lower()+' de '+titre+' est sorti !')
                                
                # Ajouter le scan à la liste des scans publiés
                scans_tweetes.append(titre+'/'+chapitre)

    # Enregistrer les scans dans le fichier
    with open('scans_tweetes.txt', 'w',encoding='utf-8') as file:
        file.write('\n'.join(scans_tweetes))

    print('Tous les nouveaux tweets ont été publiés !')


# Exécuter en boucle
n=1
tweet_latest_japscan(n)
#while True:
#    tweet_latest_japscan(n)
#    n=n+1
#    time.sleep(60) 
