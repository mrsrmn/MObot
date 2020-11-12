import discord
from discord.ext import commands
import datetime
import sqlite3
import os
import random
import time_utils

start_time = datetime.datetime.utcnow()


x = 1
if x == 0:
    DIR = os.path.dirname(__file__)
    db = sqlite3.connect(os.path.join(DIR, "C:/Users/emirs/PycharmProjects/mobot/tags.db"))
    sql = db.cursor()
elif x == 1:
    print("# VPS MODE")
    DIR = os.path.dirname(__file__)
    db = sqlite3.connect(os.path.join(DIR, "/root/mobot/tags.db"))
    sql = db.cursor()
else:
    sql = None


class core(commands.Cog):

    def __init__(self, client):
        self.client = client

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

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        sql.execute(f'create table if not exists "{guild.id}"("id" integer not null,'
                    '"tags_name" text not null, "tags_content" text not null, "tags_date" integer not null)')

    @commands.command(aliases=["add", "c"])
    async def create(self, ctx, name, *, content=None):
        if ctx.guild.id in self.client.epic_servers:
            attachment = ctx.message.attachments
            compensation = datetime.timedelta(hours=9)
            now = datetime.datetime.now() + compensation

            sql.execute(f'select tags_name from "{ctx.guild.id}" where tags_name = "{name}"')
            does_exist = sql.fetchone()

            if does_exist is not None:
                await ctx.send(f"Taq named `{name}` already exists!")
            else:
                if attachment and content is None:
                    sql.execute(f'insert into "773249498104201228"(id, tags_name, tags_content, tags_date) '
                                f'values(?,?,?,?)', (ctx.author.id, name, ctx.message.attachments[0].url, now))
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
                        sql.execute(
                            f'insert into "773249498104201228"(id, tags_name, tags_content, tags_date) values(?,?,?,?)',
                            (ctx.author.id, name, content, now))
                        db.commit()
                        await ctx.send(f":white_check_mark: Created taq with the name `{name}`")
        else:
            attachment = ctx.message.attachments
            compensation = datetime.timedelta(hours=9)
            now = datetime.datetime.now() + compensation

            sql.execute(f'create table if not exists "{ctx.guild.id}"("id" integer not null,'
                        '"tags_name" text not null, "tags_content" text not null, "tags_date" integer not null)')

            sql.execute(f'select tags_name from "{ctx.guild.id}" where tags_name = "{name}"')
            does_exist = sql.fetchone()

            if does_exist is not None:
                await ctx.send(f"Tag named `{name}` already exists!")
            else:
                if attachment and content is None:
                    sql.execute(f'insert into "{ctx.guild.id}"(id, tags_name, tags_content, tags_date) values(?,?,?,?)',
                                (ctx.author.id, name, ctx.message.attachments[0].url, now))
                    db.commit()
                    await ctx.send(f":white_check_mark: Created tag with the name `{name}`")
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
                        sql.execute(
                            f'insert into "{ctx.guild.id}"(id, tags_name, tags_content, tags_date) values(?,?,?,?)',
                            (ctx.author.id, name, content, now))
                        db.commit()
                        await ctx.send(f":white_check_mark: Created tag with the name `{name}`")

    @commands.command(aliases=["t", "taq"])
    async def tag(self, ctx, tag=None):
        if ctx.guild.id in self.client.epic_servers:
            if tag is None:
                embed = discord.Embed(
                    title=":x: Command Raised an Exception!",
                    color=0xff0000
                )
                embed.add_field(name="Error:",
                                value=f"```taq is a required argument that is missing```")
                embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                await ctx.send(embed=embed)
            else:
                sql.execute(f'SELECT tags_content FROM "773249498104201228" WHERE tags_name= "{tag}"')
                final = sql.fetchone()

                if final:
                    await ctx.send(final[0])
                else:
                    await ctx.send(f"Taq named `{tag}` doesn't exist!")
        else:
            if tag is None:
                embed = discord.Embed(
                    title=":x: Command Raised an Exception!",
                    color=0xff0000
                )
                embed.add_field(name="Error:",
                                value=f"```tag is a required argument that is missing```")
                embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                await ctx.send(embed=embed)
            else:
                sql.execute(f'SELECT tags_content FROM "{ctx.guild.id}" WHERE tags_name= "{tag}"')
                final = sql.fetchone()

                if final:
                    await ctx.send(final[0])
                else:
                    await ctx.send(f"Tag named `{tag}` doesn't exist!")

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["d"])
    async def delete(self, ctx, tag):
        if ctx.guild.id in self.client.epic_servers:
            user = ctx.author.id
            sql.execute(f'SELECT tags_content FROM "773249498104201228" WHERE tags_name= "{tag}"')
            final = sql.fetchone()

            sql.execute(f'SELECT id FROM "773249498104201228" WHERE tags_name = "{tag}"')
            id1 = sql.fetchone()

            if final:
                if id1[0] == user or ctx.author.id in self.client.admin_ids:
                    sql.execute(f'DELETE from "773249498104201228" where tags_name = "{tag}"')
                    db.commit()
                    await ctx.send(f"Taq named `{tag}` deleted successfully")
                else:
                    await ctx.send(":x: You can't delete that taq!")
            else:
                await ctx.send(f"Taq named `{tag}` doesn't exist!")
        else:
            user = ctx.author.id
            sql.execute(f'SELECT tags_content FROM "{ctx.guild.id}" WHERE tags_name= "{tag}"')
            final = sql.fetchone()

            sql.execute(f'SELECT id FROM "{ctx.guild.id}" WHERE tags_name = "{tag}"')
            id1 = sql.fetchone()

            if final:
                if id1[0] == user or ctx.author.id in self.client.admin_ids:
                    sql.execute(f'DELETE from "{ctx.guild.id}" where tags_name = "{tag}"')
                    db.commit()
                    await ctx.send(f"Tag named `{tag}` deleted successfully")
                else:
                    await ctx.send(":x: You can't delete that tag! If you are the owner or an admin"
                                   " of this server, please enter the support server and create ticket"
                                   " so we can whitelist you about the tag deletement\n https://discord.gg/6PX24ZPnDt")
            else:
                await ctx.send(f"Taq named `{tag}` doesn't exist!")

    @commands.command(aliases=["e"])
    async def edit(self, ctx, thing, tag, *, value=None):
        if ctx.guild.id in self.client.epic_servers:
            attachment = ctx.message.attachments
            user = ctx.author.id
            sql.execute(f'SELECT tags_content FROM "773249498104201228" WHERE tags_name= "{tag}"')
            final = sql.fetchone()

            sql.execute(f'SELECT id FROM "773249498104201228" WHERE tags_name = "{tag}"')
            id1 = sql.fetchone()

            if final:
                if id1[0] == user or ctx.author.id in self.client.admin_ids:
                    if thing.lower() == "content":
                        if attachment and value is None:
                            sql.execute(
                                f'UPDATE "773249498104201228" set tags_content = "{ctx.message.attachments[0].url}" '
                                f'WHERE tags_name = "{tag}"')
                            db.commit()
                            await ctx.send(f"Tag named `{tag}` edited successfully")
                        else:
                            if value is None:
                                embed = discord.Embed(
                                    title=":x: Command Raised an Exception!",
                                    color=0xff0000
                                )
                                embed.add_field(name="Error:",
                                                value=f"```value is a required argument that is missing```")
                                embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                                await ctx.send(embed=embed)
                            else:
                                sql.execute(f'UPDATE "773249498104201228"'
                                            f' set tags_content = "{value}" WHERE tags_name = "{tag}"')
                                db.commit()
                                await ctx.send(f"Tag named `{tag}` edited successfully")
                    elif thing.lower() == "name":
                        if value is None:
                            embed = discord.Embed(
                                title=":x: Command Raised an Exception!",
                                color=0xff0000
                            )
                            embed.add_field(name="Error:",
                                            value=f"```value is a required argument that is missing```")
                            embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                            await ctx.send(embed=embed)
                        else:
                            sql.execute(
                                f'UPDATE "773249498104201228" set tags_name = "{value}" WHERE tags_name = "{tag}"')
                            db.commit()
                            await ctx.send(f"Tag named `{tag}` edited successfully")
                    else:
                        await ctx.send(":x: That is not the correct formatting of the"
                                       " command! Do `h.help` for detailed help of the command.")
                else:
                    await ctx.send(":x: You can't edit that taq!")
            else:
                await ctx.send(f"Tag named `{tag}` doesn't exist!")
        else:
            attachment = ctx.message.attachments
            user = ctx.author.id
            sql.execute(f'SELECT tags_content FROM "{ctx.guild.id}" WHERE tags_name= "{tag}"')
            final = sql.fetchone()

            sql.execute(f'SELECT id FROM "{ctx.guild.id}" WHERE tags_name = "{tag}"')
            id1 = sql.fetchone()

            if final:
                if id1[0] == user or ctx.author.id in self.client.admin_ids:
                    if thing.lower() == "content":
                        if attachment and value is None:
                            sql.execute(
                                f'UPDATE "{ctx.guild.id}" set tags_content = "{ctx.message.attachments[0].url}" '
                                f'WHERE tags_name = "{tag}"')
                            db.commit()
                            await ctx.send(f"Tag named `{tag}` edited successfully")
                        else:
                            if value is None:
                                embed = discord.Embed(
                                    title=":x: Command Raised an Exception!",
                                    color=0xff0000
                                )
                                embed.add_field(name="Error:",
                                                value=f"```content is a required argument that is missing```")
                                embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                                await ctx.send(embed=embed)
                            else:
                                sql.execute(f'UPDATE "{ctx.guild.id}"'
                                            f' set tags_content = "{value}" WHERE tags_name = "{tag}"')
                                db.commit()
                                await ctx.send(f"Tag named `{tag}` edited successfully")
                    elif thing.lower() == "name":
                        if value is None:
                            embed = discord.Embed(
                                title=":x: Command Raised an Exception!",
                                color=0xff0000
                            )
                            embed.add_field(name="Error:",
                                            value=f"```content is a required argument that is missing```")
                            embed.set_footer(text=f"MissingRequiredArgument | Occurred in: {ctx.command}")
                            await ctx.send(embed=embed)
                        else:
                            sql.execute(
                                f'UPDATE "{ctx.guild.id}" set tags_name = "{value}" WHERE tags_name = "{tag}"')
                            db.commit()
                            await ctx.send(f"Tag named `{tag}` edited successfully")
                    else:
                        await ctx.send(":x: That is not the correct formatting of the"
                                       " command! Do `h.help` for detailed help of the command.")
                else:
                    await ctx.send(":x: You can't delete that tag! If you are the owner or an admin"
                                   " of this server, please enter the support server and create ticket"
                                   " so we can whitelist you about the tag deletement\n https://discord.gg/6PX24ZPnDt")
            else:
                await ctx.send(f"Tag named `{tag}` doesn't exist!")

    @commands.command(aliases=["l", "list"])
    async def _list(self, ctx):
        if ctx.guild.id in self.client.epic_servers:
            user = ctx.author.id
            sql.execute(f'SELECT tags_name FROM "773249498104201228" WHERE id = {user}')
            final = sql.fetchall()
            finallist = str(final)
            finalc = len(final)

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
                embed.set_footer(text=f"Taq Count: {finalc}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Taq List",
                    colour=discord.Colour.purple()
                )
                embed.add_field(name="**Taqs:**", value=h)
                embed.set_footer(text=f"Taq Count: {finalc}")
                await ctx.send(embed=embed)
        else:
            user = ctx.author.id
            sql.execute(f'SELECT tags_name FROM "{ctx.guild.id}" WHERE id = {user}')
            final = sql.fetchall()
            finallist = str(final)
            finalc = len(final)

            h = finallist.replace("('", "")
            h = h.replace("[", "")
            h = h.replace("',),", "\n")
            h = h.replace("',)]", "")

            if h == "]":
                embed = discord.Embed(
                    title="Tag List",
                    colour=discord.Colour.purple()
                )
                embed.add_field(name="**Tags:**", value="You don't own any lol")
                embed.set_footer(text=f"Tag Count: {finalc}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Taq List",
                    colour=discord.Colour.purple()
                )
                embed.add_field(name="**Tags:**", value=h)
                embed.set_footer(text=f"Tag Count: {finalc}")
                await ctx.send(embed=embed)

    @commands.command(aliases=["la"])
    async def listall(self, ctx):
        if ctx.guild.id in self.client.epic_servers:
            sql.execute(f'SELECT tags_name FROM "773249498104201228"')
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
        else:
            sql.execute(f'SELECT tags_name FROM "{ctx.guild.id}"')
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
        if ctx.guild.id in self.client.epic_servers:
            sql.execute(f'SELECT tags_name FROM "773249498104201228"')
            name = sql.fetchall()
            the = random.choice(name)

            sql.execute(f'SELECT tags_content FROM "773249498104201228" WHERE tags_name= "{the[0]}"')
            final = sql.fetchone()

            sql.execute(f'SELECT tags_name FROM "773249498104201228" WHERE tags_name= "{the[0]}"')
            tagname = sql.fetchone()

            sql.execute(f'SELECT id FROM "773249498104201228" WHERE tags_name= "{the[0]}"')
            owner = sql.fetchone()
            user = self.client.get_user(owner[0])

            await ctx.send(f"**Taqs Name:** {tagname[0]}\n**Taqs Owner:** {user}\n{final[0]}")
        else:
            sql.execute(f'SELECT tags_name FROM "{ctx.guild.id}"')
            name = sql.fetchall()
            the = random.choice(name)

            sql.execute(f'SELECT tags_content FROM "{ctx.guild.id}" WHERE tags_name= "{the[0]}"')
            final = sql.fetchone()

            sql.execute(f'SELECT tags_name FROM "{ctx.guild.id}" WHERE tags_name= "{the[0]}"')
            tagname = sql.fetchone()

            sql.execute(f'SELECT id FROM "{ctx.guild.id}" WHERE tags_name= "{the[0]}"')
            owner = sql.fetchone()
            user = self.client.get_user(owner[0])

            await ctx.send(f"**Tags Name:** {tagname[0]}\n**Tags Owner:** {user}\n{final[0]}")

    @commands.command(aliases=["i"])
    async def info(self, ctx, taq):
        if ctx.guild.id in self.client.epic_servers:
            sql.execute(f'SELECT id FROM "773249498104201228" WHERE tags_name = "{taq}"')
            ownerid = sql.fetchone()

            sql.execute(f'SELECT tags_date FROM "773249498104201228" WHERE tags_name = "{taq}"')
            date = sql.fetchone()

            sql.execute(f'SELECT tags_content FROM "773249498104201228" WHERE tags_name= "{taq}"')
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
        else:
            sql.execute(f'SELECT id FROM "{ctx.guild.id}" WHERE tags_name = "{taq}"')
            ownerid = sql.fetchone()

            sql.execute(f'SELECT tags_date FROM "{ctx.guild.id}" WHERE tags_name = "{taq}"')
            date = sql.fetchone()

            sql.execute(f'SELECT tags_content FROM "{ctx.guild.id}" WHERE tags_name= "{taq}"')
            content = sql.fetchone()

            if content:
                embed = discord.Embed(
                    title=f"Tag Info of {taq}",
                    colour=discord.Colour.purple()
                )
                embed.add_field(name="Owner:", value=f"<@{ownerid[0]}>")
                embed.add_field(name="Creation Date:", value=date[0][:-7])
                await ctx.send(embed=embed)
            else:
                await ctx.send(":x: That tag doesn't seem to exist!")

    @commands.command()
    async def about(self, ctx):
        if ctx.guild.id in self.client.epic_servers:
            sql.execute(f'SELECT tags_name FROM "773249498104201228"')
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
        else:

            user = self.client.get_user(444550944110149633)

            embed = discord.Embed(
                title="MOBot Info ",
                description="MO is a very powerful tag bot powered with SQLite",
                color=discord.Colour.purple()
            )
            embed.add_field(name="Ping:", value=f"{round(self.client.latency * 1000)}ms")
            embed.add_field(name="Command Count:", value=f"{len(self.client.commands)}")
            embed.add_field(name="Made by:", value=f"{user}")
            embed.add_field(name="Uptime", value=time_utils.get_bot_uptime(start_time))
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(core(client))
