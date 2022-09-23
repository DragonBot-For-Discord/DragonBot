import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite InterServer] database.db загружен!")

class interserver(commands.Cog):

    def __init__(self, bot):
        client = bot

    @commands.slash_command(description=Localized("Enable/disable interserver in a certain channel", key="INTERSERVER_CONNECT_DESCRIPTION"))
    @commands.has_permissions(manage_channels = True)
    async def interserver_toggle(ctx, channel: discord.TextChannel, isenabled: bool):
        cursor.execute(f"SELECT channel_id FROM interserver_enabled WHERE guild_id = {ctx.guild.id}")
        result =  cursor.fetchone()

        if result is None:
            cursor.execute(f"INSERT INTO interserver_enabled(guild_id, channel_id, isEnabled) VALUES({ctx.guild.id}, {channel.id}, {isenabled})")
            connection.commit()
        else:
            cursor.execute(f"UPDATE interserver_enabled SET channel_id = {channel.id}, isEnabled = {isenabled} WHERE guild_id = {ctx.guild.id}")
            connection.commit()

        if isenabled == False:
            await ctx.send("**Межсервер** успешно выключен", ephemeral=True)
        if isenabled == True:
            await ctx.send("**Межсервер** успешно включен", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(interserver(bot))