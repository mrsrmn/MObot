import discord
from discord.ext import commands
import datetime
import sqlite3
import os
import asyncio
import random
import time_utils

start_time = datetime.datetime.utcnow()

x = 0
if x == 0:
    DIR = os.path.dirname(__file__)
    db = sqlite3.connect(os.path.join(DIR, "C:/Users/emirs/PycharmProjects/mobot/tags.db"))
    sql = db.cursor()
elif x == 1:
    print("# VPS MODE")
    DIR = os.path.dirname(__file__)
    db = sqlite3.connect(os.path.join(DIR, "/root/mobot/tags.db"))
    sql = db.cursor()

sql.execute('create table if not exists tags_list("id" integer not null,'
            '"tags_name" text not null, "tags_content" text not null, "tags_date" integer not null)')

sql.execute(f'SELECT tags_name FROM tags_list')
final1 = sql.fetchall()
final2 = len(final1)

admin_ids = [444550944110149633, 429935667737264139, 603635602809946113]


class core(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def status_task(self):
        while True:
            await self.client.change_presence(status=discord.Status.idle,
                                              activity=discord.Game(f"Servinq h2.1 with {final2} taqs"))
            await asyncio.sleep(300)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title=":x: Command Raised an Exception!",
                color=0xff0000
            )
            embed.add_field(name="Error:", value=f"```{error}```")
            embed.set_footer(text=f"{error.__class__.__name__} | Occurred in: {ctx.command}")
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title=":x: Command Raised an Exception!",
                color=0xff0000
            )
            embed.add_field(name="Error:", value=f"**You don't have enough permissions to do that!")
            embed.set_footer(text=f"{error.__class__.__name__} | Occurred in: {ctx.command}")
            await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready")
        self.client.loop.create_task(self.status_task())

    @commands.command(aliases=["help","h"])
    async def _help(self, ctx):
        embed = discord.Embed(
            title="MOBot Help",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="taq <taq>", value="Shows you the specified taq")
        embed.add_field(name="create <name> <content>", value="Creates a taq")
        embed.add_field(name="delete <taq>", value="Deletes a taq")
        embed.add_field(name="edit <name/content> <taq> <content>", value="Edits a taq you own")
        embed.add_field(name="list", value="Qives a list of the taqs you've created")
        embed.add_field(name="listall", value="Qives a list of the taqs (all of them)")
        embed.add_field(name="pinq", value="Qives the latency")
        embed.add_field(name="info <taq>", value="Qives info about a taq")
        embed.add_field(name="about", value="About the bot")
        embed.add_field(name="random", value="Qives a random taq")
        embed.add_field(name="credits", value="Bots credits")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/7738394075969618"
                                "03/c32e9d106e4204ca6e68f2ec5b959c32.webp?size=1024")
        await ctx.send(embed=embed)

    @commands.command(aliases=["add", "c"])
    async def create(self, ctx, name, *, content=None):
        attachment = ctx.message.attachments
        compensation = datetime.timedelta(hours=9)
        now = datetime.datetime.now() + compensation
        sql.execute(f'select tags_name from tags_list where tags_name = "{name}"')
        does_exist = sql.fetchone()

        if does_exist is not None:
            await ctx.send(f"Taq named `{name}` already exists!")
        else:
            if attachment and content is None:
                sql.execute('insert into tags_list(id, tags_name, tags_content, tags_date) values(?,?,?,?)',
                            (ctx.author.id, name, ctx.message.attachments[0].url, now))
                db.commit()
                await ctx.send(f":white_check_mark: Created taq with the name `{name}`")
            else:
                if content is None:
                    embed = discord.Embed(
                        title=":x: Command Raised an Exception!",
                        color=0xff0000
                    )
                    embed.add_field(name="Error:",
                                    value=f"```content is a required argument that is missing```")
                    embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                    await ctx.send(embed=embed)
                else:
                    sql.execute('insert into tags_list(id, tags_name, tags_content, tags_date) values(?,?,?,?)',
                            (ctx.author.id, name, content, now))
                    db.commit()
                    await ctx.send(f":white_check_mark: Created taq with the name `{name}`")

    @commands.command(aliases=["t"])
    async def taq(self, ctx, taq):
        sql.execute(f'SELECT tags_content FROM tags_list WHERE tags_name= "{taq}"')
        final = sql.fetchone()

        if final:
            await ctx.send(final[0])
        else:
            await ctx.send(f"Taq named `{taq}` doesn't exist!")

    @commands.command()
    async def tag(self, ctx):
        await ctx.send("It's `h.taq` you fucking g-spy")

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["d"])
    async def delete(self, ctx, taq):
        user = ctx.author.id
        sql.execute(f'SELECT tags_content FROM tags_list WHERE tags_name= "{taq}"')
        final = sql.fetchone()

        sql.execute(f'SELECT id FROM tags_list WHERE tags_name = "{taq}"')
        id1 = sql.fetchone()

        if final:
            if id1[0] == user or ctx.author.id in admin_ids:
                sql.execute(f'DELETE from tags_list where tags_name = "{taq}"')
                db.commit()
                await ctx.send(f"Taq named `{taq}` deleted successfully")
            else:
                await ctx.send(":x: You can't delete that taq!")
        else:
            await ctx.send(f"Taq named `{taq}` doesn't exist!")

    @commands.command(aliases=["e"])
    async def edit(self, ctx, thinq, taq, *, content=None):
        attachment = ctx.message.attachments
        user = ctx.author.id
        sql.execute(f'SELECT tags_content FROM tags_list WHERE tags_name= "{taq}"')
        final = sql.fetchone()

        sql.execute(f'SELECT id FROM tags_list WHERE tags_name = "{taq}"')
        id1 = sql.fetchone()

        if final:
            if id1[0] == user or ctx.author.id in admin_ids:
                if thinq.lower() == "content":
                    if attachment and content is None:
                        sql.execute(
                            f'UPDATE tags_list set tags_content = "{ctx.message.attachments[0].url}" WHERE tags_name = "{taq}"')
                        db.commit()
                        await ctx.send(f"Tag named `{taq}` edited successfully")
                    else:
                        if content is None:
                            embed = discord.Embed(
                                title=":x: Command Raised an Exception!",
                                color=0xff0000
                            )
                            embed.add_field(name="Error:",
                                            value=f"```content is a required argument that is missing```")
                            embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                            await ctx.send(embed=embed)
                        else:
                            sql.execute(f'UPDATE tags_list set tags_content = "{content}" WHERE tags_name = "{taq}"')
                            db.commit()
                            await ctx.send(f"Tag named `{taq}` edited successfully")
                elif thinq.lower() == "name":
                    if content is None:
                        embed = discord.Embed(
                            title=":x: Command Raised an Exception!",
                            color=0xff0000
                        )
                        embed.add_field(name="Error:", value=f"```content is a required argument that is missing```")
                        embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                        await ctx.send(embed=embed)
                    else:
                        sql.execute(
                            f'UPDATE tags_list set tags_name = "{content}" WHERE tags_name = "{taq}"')
                        db.commit()
                        await ctx.send(f"Tag named `{taq}` edited successfully")
                else:
                    await ctx.send(":x: That is not the correct formatting of the command! Do `h.help` for detailed help of the command.")
            else:
                await ctx.send(":x: You can't edit that tag!")
        else:
            await ctx.send(f"Tag named `{taq}` doesn't exist!")

    @commands.command(aliases=["l", "list"])
    async def _list(self, ctx):
        user = ctx.author.id
        sql.execute(f'SELECT tags_name FROM tags_list WHERE id = {user}')
        final = sql.fetchall()
        finallist = str(final)
        final2 = len(final)

        h = finallist.replace("('", "")
        h = h.replace("[", "")
        h = h.replace("',),", "\n")
        h = h.replace("',)]", "")

        if h == "]":
            embed = discord.Embed(
                title="Taq List",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="**Taqs:**", value="You don't own any lol")
            embed.set_footer(text=f"Taq Count: {final2}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Taq List",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="**Taqs:**", value=h)
            embed.set_footer(text=f"Taq Count: {final2}")
            await ctx.send(embed=embed)

    @commands.command(aliases=["la"])
    async def listall(self, ctx):
        sql.execute(f'SELECT tags_name FROM tags_list')
        final = sql.fetchall()
        finalstr = str(final)
        finalcount = len(final)

        h = finalstr.replace("('", "")
        h = h.replace("[", "")
        h = h.replace("',)]", "")
        h = h.replace("',),", "\n")

        if h == "]":
            embed = discord.Embed(
                title="Taq List",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="**Taqs:**", value="there isnt any lol")
            embed.set_footer(text=f"Taq Count: {finalcount}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Taq List",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="**Taqs:**", value=h)
            embed.set_footer(text=f"Taq Count: {finalcount}")
            await ctx.send(embed=embed)

    @commands.command()
    async def random(self, ctx):
        sql.execute(f'SELECT tags_name FROM tags_list')
        name = sql.fetchall()
        the = random.choice(name)

        sql.execute(f'SELECT tags_content FROM tags_list WHERE tags_name= "{the[0]}"')
        final = sql.fetchone()

        sql.execute(f'SELECT tags_name FROM tags_list WHERE tags_name= "{the[0]}"')
        tagname = sql.fetchone()

        sql.execute(f'SELECT id FROM tags_list WHERE tags_name= "{the[0]}"')
        owner = sql.fetchone()
        user = self.client.get_user(owner[0])

        await ctx.send(f"**Taqs Name:** {tagname[0]}\n**Taqs Owner:** {user}\n{final[0]}")

    @commands.command(aliases=["i"])
    async def info(self, ctx, taq):
        sql.execute(f'SELECT id FROM tags_list WHERE tags_name = "{taq}"')
        ownerid = sql.fetchone()

        sql.execute(f'SELECT tags_date FROM tags_list WHERE tags_name = "{taq}"')
        date = sql.fetchone()

        sql.execute(f'SELECT tags_content FROM tags_list WHERE tags_name= "{taq}"')
        content = sql.fetchone()

        if content:
            embed = discord.Embed(
                title=f"Taq Info of {taq}",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="Owner:", value=f"<@{ownerid[0]}>")
            embed.add_field(name="Creation Date:", value=date[0][:-7])
            await ctx.send(embed=embed)
        else:
            await ctx.send(":x: That taq doesn't seem to exist!")

    @commands.command(aliases=["shutup", "die"])
    async def fuckoff(self, ctx):
        await ctx.send("qoodbye cruel world :pensive: :v:")
        exit()

    @commands.command()
    async def pinq(self, ctx):
        await ctx.send(f"**{round(self.client.latency * 1000)}ms**")

    @commands.command()
    async def reload(self, ctx):
        if ctx.author.id in admin_ids:
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
    async def about(self, ctx):
        sql.execute(f'SELECT tags_name FROM tags_list')
        final = sql.fetchall()
        finalcount = len(final)

        user = self.client.get_user(444550944110149633)

        embed = discord.Embed(
            title="MOBot Info :flushed:",
            description="MO is an epic bot made for h2.1 :sunglasses:",
            color=discord.Colour.purple()
        )
        embed.add_field(name="Pinq:", value=f"{round(self.client.latency * 1000)}ms")
        embed.add_field(name="Command Count:", value=f"{len(self.client.commands)}")
        embed.add_field(name="Made by:", value=f"{user} :sunglasses:")
        embed.add_field(name="Taq Count:", value=f"{finalcount}")
        embed.add_field(name="Uptime", value=time_utils.get_bot_uptime(start_time))
        await ctx.send(embed=embed)

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


def setup(client):
    client.add_cog(core(client))
