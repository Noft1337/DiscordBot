import discord
from discord.ext import commands
import music

cog = [music]
client = commands.Bot(command_prefix='?', intents = discord.Intents.all())

for i in range(len(cog)):
    cog[i].setup(client)

client.run("MTAwNzY5NTE3MzM3Mjg3MDcxNw.G1tRMu.QTQPW2vPYi6Uv1uF36t0cOAvmj8driDFW9fm08")

