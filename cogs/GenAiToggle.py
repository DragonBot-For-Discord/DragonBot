import disnake as discord
from disnake.ext import commands
from disnake import Localized
from disnake.utils import get
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite GenAiToggle] database.db загружен!")

class GenAiToggle(commands.Cog):
    @commands.slash_command(description=Localized("Enable/disable GenAi in a certain channel", key="GENAI_TOGGLE_DESCRIPTION"))
    @commands.has_permissions(manage_channels = True)
    async def genai_toggle(ctx, channel: discord.TextChannel, isenabled: bool):
        cursor.execute(f"SELECT channel_id FROM genai_enabled WHERE guild_id = {ctx.guild.id}")
        result =  cursor.fetchone()

        if result is None:
            cursor.execute(f"INSERT INTO genai_enabled(guild_id, channel_id, isEnabled) VALUES({ctx.guild.id}, {channel.id}, {isenabled})")
            connection.commit()
        else:
            cursor.execute(f"UPDATE genai_enabled SET channel_id = {channel.id}, isEnabled = {isenabled} WHERE guild_id = {ctx.guild.id}")
            connection.commit()
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        if isenabled == False:
            if langCodeReal == "ru":
                await ctx.send("**GenAi** успешно выключен", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send("**GenAi** successfully disabled", ephemeral=True)
        if isenabled == True:
            if langCodeReal == "ru":
                await ctx.send("**GenAi** успешно включен", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send("**GenAi** successfully enabled", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(GenAiToggle(bot))