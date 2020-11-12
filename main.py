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

client.epic_servers = [773249498104201228, 713675042143076352]
client.admin_ids = [444550944110149633, 429935667737264139, 603635602809946113]

client.load_extension("cogs.core")
client.load_extension("cogs.utility")

client.run(TOKEN)
