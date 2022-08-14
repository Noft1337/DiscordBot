import discord
from discord.ext import commands
import music

with open(r'.\Token.txt', 'r') as file:
    TOKEN = file.read()
cog = [music]
client = commands.Bot(command_prefix='?', intents=discord.Intents.all())

for i in range(len(cog)):
    cog[i].setup(client)

client.run(TOKEN)

