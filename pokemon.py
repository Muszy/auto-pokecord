import config

import pokemon_db as pk
import requests
import discord
import asyncio
import time
import random

PKMN_DB = pk.open_pkl(pk.BASE_PATH+'\pkmn_db.pkl')
WAIT = 4
CLIENT = discord.Client()

def main():
    CLIENT.run(config.EMAIL,config.PASSWORD)

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('-----')

@CLIENT.event
async def on_message(message):
    try:
        if message.server.id == config.SERVER_ID:
            print("{tstamp}:{author}".format(
                tstamp=message.timestamp,
                author=message.author.name))
        
        if message.author.id == config.POKEBOT_ID:
            title = message.embeds[0]['title']
            print(title)
            if (title == 'A wild pokémon has appeared!'):
                pkmn_url = message.embeds[0]['image']['url']
                print(pkmn_url)
                req = requests.get(pkmn_url)
                print('website read')
                pkmn_name = PKMN_DB[pk.get_hash(req)]
                print(pkmn_name)
                print('waiting 4s')
                time.sleep(WAIT)
                print('waited 4s')
                await CLIENT.send_message(message.channel, '.catch '+pkmn_name)
    except:
        pass

if __name__ == "__main__":
    main()
