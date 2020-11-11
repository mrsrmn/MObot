from discord.ext import commands
import discord
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="h.", intents=intents)
client.remove_command("help")

client.load_extension("cogs.core")

client.run(TOKEN)
