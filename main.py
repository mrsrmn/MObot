from discord.ext import commands

client = commands.Bot(command_prefix="h.")
client.remove_command("help")

client.load_extension("cogs.core")

client.run("NzczODM5NDA3NTk2OTYxODAz.X6PEHA.nFjMaVNHsTfFXLTuU7DrCsyqoFg")
