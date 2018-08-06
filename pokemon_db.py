import os
import requests
import numpy as np
import csv
import pickle
import imagehash
from bs4 import BeautifulSoup as bf
from PIL import Image
from io import BytesIO

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://bulbapedia.bulbagarden.net/wiki/File:'

def read_csv(file_name):
    with open(file_name) as f:
        pkmn = [tuple(line) for line in csv.reader(f)]
        return(pkmn)

def get_img(base_url, pkmn_no, pkmn_name):
    try:
        url = '{0}{1}{2}.png'.format(base_url,pkmn_no,pkmn_name)
        req = requests.get(url)
        img_url = 'https:'+bf(req.content, 'html.parser').find_all('img')[0]['src']
        req = requests.get(img_url)
        return(req)
    except requests.exceptions.HTTPError:
        print('Could not download page.')
        return(None)

def get_hash(req):
    return imagehash.average_hash(Image.open(BytesIO(req.content)))

def create_hash(userpath):
    pkmn_db = {} 
    for img,name in zip([os.path.join(userpath, path) for path in os.listdir(userpath)],[name[3:-4] for name in os.listdir(userpath)]):
        hash = imagehash.average_hash(Image.open(img))
        pkmn_db[hash] = name
    return(pkmn_db)

def save_pkl(d, file):
    with open(file, 'wb') as f:
        pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)

def open_pkl(file):
    with open(file, 'rb') as f:
        return pickle.load(f)
