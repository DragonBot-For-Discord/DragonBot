import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3
from typing import List

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite SwitchLang] database.db загружен!")

LangCodes = ["ru", "en"]

async def autocomplete_langs(inter, string: str) -> List[str]:
    return [lang for lang in LangCodes if string.lower() in lang.lower()]

class SwitchLang(commands.Cog):
    @commands.slash_command(description=Localized("Change the bot's language", key="CHANGE_BOT_LANG_DESCRIPTION"))
    @commands.has_permissions(manage_messages = True)
    async def switch_lang(ctx, langcode: str = commands.Param(autocomplete=autocomplete_langs), confirm: str = "no"):
        if langcode == "ru":
            if confirm == "yes":
                cursor.execute(f"SELECT guild_id FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
                result =  cursor.fetchone()

                if result is None:
                    cursor.execute(f"INSERT INTO guilds_lang(guild_id, lang_code) VALUES({ctx.guild.id}, '{langcode}')")
                    connection.commit()
                else:
                    cursor.execute(f"UPDATE guilds_lang SET lang_code = '{langcode}' WHERE guild_id = {ctx.guild.id}")
                    connection.commit()
                await ctx.send("Язык был изменён! Изменения уже применены", ephemeral=True)
            else:
                embed = discord.Embed(title="Изменение языка на Русский")
                embed.add_field("Изменение языка бота на Русский изменит язык бота на всём сервере, включая кнопки в командах, и прочее.", "Подтвердите изменение языка на Русский командой **/switch_lang ru yes**")
                await ctx.send(embed=embed)
        elif langcode == "en":
            if confirm == "yes":
                cursor.execute(f"SELECT guild_id FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
                result =  cursor.fetchone()

                if result is None:
                    cursor.execute(f"INSERT INTO guilds_lang(guild_id, lang_code) VALUES({ctx.guild.id}, '{langcode}')")
                    connection.commit()
                else:
                    cursor.execute(f"UPDATE guilds_lang SET lang_code = '{langcode}' WHERE guild_id = {ctx.guild.id}")
                    connection.commit()
                await ctx.send("Language has been changed! Changes have already been applied", ephemeral=True)
            else:
                embed = discord.Embed(title="Switch language to English")
                embed.add_field("Switch bot language to English will change language on all server, including buttons in commands, and etc", "Confirm change language by command **/switch_lang en yes**")
                await ctx.send(embed=embed)
        else:
            await ctx.send("Неизвесный языковой код | Unknown language code", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(SwitchLang(bot))