import disnake as discord
from disnake import Localized
from disnake.ext import commands
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite BotConfig] database.db загружен!")

class BotConfig(commands.Cog):
    @commands.slash_command(description=Localized("View bot settings on this server", key="VIEW_BOT_SETTINGS_SLASH_COMMAND"))
    async def config(ctx):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        cursor.execute(f"SELECT isEnabled FROM automod_spam WHERE guild_id = {ctx.guild.id}")
        automod_spam = cursor.fetchone()
        automod_spamStr = str(automod_spam)
        automod_spamReal = automod_spamStr.replace("(", "").replace(")", "").replace(",", "")
        try:
            automod_spamRealInt = int(automod_spamReal)
        except:
            automod_spamRealInt = 0

        if automod_spamRealInt == 1:
            if langCodeReal == "ru":
                isEnabledAMSpam = "Включено"
            if langCodeReal == "en":
                isEnabledAMSpam = "Enabled"
        else:
            if langCodeReal == "ru":
                isEnabledAMSpam = "Выключено"
            if langCodeReal == "en":
                isEnabledAMSpam = "Disabled"




        cursor.execute(f"SELECT isEnabled FROM automod_raid WHERE guild_id = {ctx.guild.id}")
        automod_raid = cursor.fetchone()
        automod_raidStr = str(automod_raid)
        automod_raidReal = automod_raidStr.replace("(", "").replace(")", "").replace(",", "")
        try:
            automod_raidRealInt = int(automod_raidReal)
        except:
            automod_raidRealInt = 0

        if automod_raidRealInt == 1:
            if langCodeReal == "ru":
                isEnabledAMRaid = "Включено"
            if langCodeReal == "en":
                isEnabledAMRaid = "Enabled"
        else:
            if langCodeReal == "ru":
                isEnabledAMRaid = "Выключено"
            if langCodeReal == "en":
                isEnabledAMRaid = "Disabled"




        cursor.execute(f"SELECT isEnabled FROM automod_badwords WHERE guild_id = {ctx.guild.id}")
        automod_badwords = cursor.fetchone()
        automod_badwordsStr = str(automod_badwords)
        automod_badwordsReal = automod_badwordsStr.replace("(", "").replace(")", "").replace(",", "")
        try:
            automod_badwordsRealInt = int(automod_badwordsReal)
        except:
            automod_badwordsRealInt = 0

        if automod_badwordsRealInt == 1:
            if langCodeReal == "ru":
                isEnabledAMBW = "Включено"
            if langCodeReal == "en":
                isEnabledAMBW = "Enabled"
        else:
            if langCodeReal == "ru":
                isEnabledAMBW = "Выключено"
            if langCodeReal == "en":
                isEnabledAMBW = "Disabled"

        if langCodeReal == "ru":
            embed = discord.Embed(
                title = f"Настройки бота на сервере {ctx.guild.name}",
                description = f"Тут показаны настройки DragonBot на сервере **{ctx.guild.name}**"
            )
            embed.add_field(name=f'Автомодерация-АнтиСпам', value=isEnabledAMSpam, inline=False)
            embed.add_field(name=f'Автомодерация-АнтиРейд', value=isEnabledAMRaid, inline=False)
            embed.add_field(name=f'Автомодерация-Плохие Слова', value=isEnabledAMBW, inline=False)
            embed.add_field(name=f'Язык', value=langCodeReal, inline=False)
            await ctx.send(embed=embed, ephemeral=True)
        if langCodeReal == "en":
            embed = discord.Embed(
                title = f"Bot Config on server {ctx.guild.name}",
                description = f"Here are shown the bot config on server **{ctx.guild.name}**"
            )
            embed.add_field(name=f'Automod-Spam', value=isEnabledAMSpam, inline=False)
            embed.add_field(name=f'Automod-Raid', value=isEnabledAMRaid, inline=False)
            embed.add_field(name=f'Automod-Badwords', value=isEnabledAMBW, inline=False)
            embed.add_field(name=f'Language', value=langCodeReal, inline=False)
            await ctx.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(BotConfig(bot))