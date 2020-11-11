from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="h.", intents=intents)
client.remove_command("help")

client.load_extension("cogs.core")

client.run("NzczODM5NDA3NTk2OTYxODAz.X6PEHA.nFjMaVNHsTfFXLTuU7DrCsyqoFg")
