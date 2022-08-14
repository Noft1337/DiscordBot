import discord
from discord.ext import commands
import music
"""
if ffmpeg is not found then install it via choco
then run on cmd
cp C:\ProgramData\chocolatey\bin\ffmpeg.exe %APPDATA%\..\Local\Programs\Python39\Scripts
of course it will vary depending on your python version
"""

with open(r'.\Token.txt', 'r') as file:
    TOKEN = file.read()
cog = [music]
client = commands.Bot(command_prefix='?', intents = discord.Intents.all())

for i in range(len(cog)):
    cog[i].setup(client)

client.run(TOKEN)

