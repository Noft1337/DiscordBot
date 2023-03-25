import discord
from discord.ext import commands
import music
from dotenv import load_dotenv
import os
import init_spotify


load_dotenv()
TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
print("[*] - Starting bot...")

SPOTIFY_TOKEN = init_spotify.get_token(client_secret=CLIENT_SECRET, client_id=CLIENT_ID)

cog = [music]
client = commands.Bot(command_prefix='?', intents=discord.Intents.all())

for i in range(len(cog)):
    cog[i].setup(client)


spotify_token = client.run(TOKEN)

