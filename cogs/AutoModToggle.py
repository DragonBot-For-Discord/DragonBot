import disnake as discord
from disnake.ext import commands
from disnake.utils import get
from disnake import Localized
import sqlite3
from typing import List

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite AutoModToggle] database.db загружен!")

actionsAutoModToggle = [
    "spam",
    "raid",
    "badwords",
    "crash",
    "botVerified"
]

async def autocomplete_automod_actions(inter, string: str) -> List[str]:
    return [lang for lang in actionsAutoModToggle if string.lower() in lang.lower()]

class AutoModToggle(commands.Cog):
    @commands.slash_command(description=Localized("Enable/disable auto moderation", key="ENABLE_OR_DISABLE_AUTOMOD_DESCRIPTION_SLASH_COMMAND"))
    @commands.has_permissions(manage_messages = True)
    async def automod(ctx, isenabled: bool, action: str = commands.Param(autocomplete=autocomplete_automod_actions)):
        try:
            cursor.execute(f"SELECT guild_id FROM automod_{action} WHERE guild_id = {ctx.guild.id}")
            result =  cursor.fetchone()
        except:
            await ctx.send("Неизвестное действие | Unknown action", ephemeral=True)

        if result is None:
            try:
                cursor.execute(f"INSERT INTO automod_{action}(guild_id, isEnabled) VALUES({ctx.guild.id},{isenabled})")
                connection.commit()

                await ctx.send(":white_check_mark:")
            except:
                await ctx.send("Неизвестное действие | Unknown action", ephemeral=True)
        else:
            try:
                cursor.execute(f"UPDATE automod_{action} SET isEnabled = {isenabled} WHERE guild_id = {ctx.guild.id}")
                connection.commit()

                await ctx.send(":white_check_mark:")
            except:
                await ctx.send("Неизвестное действие | Unknown action", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(AutoModToggle(bot))