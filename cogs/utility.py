import discord
from discord.ext import commands
import os


class utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["help", "h"])
    async def _help(self, ctx):
        if ctx.guild.id in self.client.epic_servers:
            embed = discord.Embed(
                title="MOBot Help",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="taq <taq>", value="Shows you the specified taq")
            embed.add_field(name="create <name> <content>", value="Creates a taq")
            embed.add_field(name="delete <taq>", value="Deletes a taq")
            embed.add_field(name="edit <name/content> <taq> <value>", value="Edits the name or the content of "
                                                                            "a taq you own")
            embed.add_field(name="list", value="Qives a list of the taqs you've created")
            embed.add_field(name="listall", value="Qives a list of the taqs (all of them)")
            embed.add_field(name="pinq", value="Qives the latency")
            embed.add_field(name="info <taq>", value="Qives info about a taq")
            embed.add_field(name="about", value="About the bot")
            embed.add_field(name="random", value="Qives a random taq")
            embed.add_field(name="credits", value="Bots credits")
            embed.add_field(name="invite", value="Invite link for MO")
            embed.add_field(name="support", value="Support server for MO")
            embed.add_field(name="vote", value="Vote link for MO")
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/7738394075969618"
                                    "03/c32e9d106e4204ca6e68f2ec5b959c32.webp?size=1024")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="MOBot Help",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="tag <tag>", value="Shows you the specified tag")
            embed.add_field(name="create <name> <content>", value="Creates a tag")
            embed.add_field(name="delete <tag>", value="Deletes a tag")
            embed.add_field(name="edit <name/content> <tag> <value>", value="Edits the name or the content of "
                                                                            "a tag you own")
            embed.add_field(name="list", value="Gives a list of the tags you've created")
            embed.add_field(name="listall", value="Gives a list of the tags (all of them)")
            embed.add_field(name="ping", value="Gives the latency")
            embed.add_field(name="info <tag>", value="Gives info about a tag")
            embed.add_field(name="about", value="About the bot")
            embed.add_field(name="random", value="Gives a random tag")
            embed.add_field(name="credits", value="Bots credits")
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/7738394075969618"
                                    "03/c32e9d106e4204ca6e68f2ec5b959c32.webp?size=1024")
            await ctx.send(embed=embed)

    @commands.command(aliases=["shutup", "die"])
    async def fuckoff(self, ctx):
        if ctx.author.id in self.client.admin_ids:
            await ctx.send("goodbye cruel world :pensive: :v:")
            exit()
        else:
            return

    @commands.command(aliases=["ping"])
    async def pinq(self, ctx):
        await ctx.send(f"**{round(self.client.latency * 1000)}ms**")

    @commands.command()
    async def reload(self, ctx):
        if ctx.author.id in self.client.admin_ids:
            await ctx.send("reloadinq coqs lol")
            try:
                for element in os.listdir("cogs"):
                    if element != "__pycache__":
                        self.client.unload_extension(f"cogs.{element.replace('.py', '')}")
                        self.client.load_extension(f"cogs.{element.replace('.py', '')}")
                await ctx.send("done :flushed:")
            except Exception as e:
                await ctx.send(repr(e))
        else:
            await ctx.send("you cant use that :rage:")

    @commands.command()
    async def credits(self, ctx):
        makufon = self.client.get_user(444550944110149633)
        human = self.client.get_user(429935667737264139)
        lunah = self.client.get_user(603635602809946113)
        embed = discord.Embed(
            title="MOBot Credits",
            description="These are the epic people who made MOBot possible",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Developer:", value=makufon)
        embed.add_field(name="Special Thanks:", value=f"{lunah}\n{human}")
        embed.add_field(name="Library:", value=f"discord.py {discord.__version__}")
        embed.add_field(name="DB Used:", value="SQLite")
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("**You can add MO to your servers with using this link:** https://bit.ly/2UewLw5")

    @commands.command()
    async def support(self, ctx):
        await ctx.send("**Here is the invite link for the support server of MO:** https://discord.gg/6PX24ZPnDt")

    @commands.command()
    async def vote(self, ctx):
        await ctx.send("**Here is the vote link for MO:** https://top.gg/bot/773839407596961803/vote")


def setup(client):
    client.add_cog(utility(client))
