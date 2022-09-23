import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite ClearChat] database.db загружен!")


class ClearChat(commands.Cog):
    @commands.slash_command(description=Localized("Clear chat", key="CLEAR_CHAT_DESCRIPTION_SLASH_COMMAND"))
    @commands.has_permissions(manage_messages = True)
    async def clear(ctx, amount: int, member: discord.User = None):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        global x

        if member == None:
            x = await ctx.channel.purge(limit=amount)
        else:
            x = await ctx.channel.purge(limit=amount, check=lambda m: m.author==member)

        if len(x) == 0:
            if langCodeReal == "ru": await ctx.send(f"Удаление сообщений не удалось. Возможно у бота недостаточно прав", ephemeral=True)
            if langCodeReal == "en": await ctx.send(f"The deletion of messages failed. Perhaps the bot does not have enough permissions", ephemeral=True)
        else:
            if langCodeReal == "ru": await ctx.send(f"Чат очищен. Удалено {len(x)} сообщений", ephemeral=True)
            if langCodeReal == "en": await ctx.send(f"Chat cleared. Deleted {len(x)} messages", ephemeral=True)

    
    @clear.error
    async def clear_error(ctx, error, argument):
        if isinstance(error, commands.MissingPermissions):
            cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
            langCode = cursor.fetchone()
            langCodeStr = str(langCode)
            langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
            if langCodeReal == "ru":
                await ctx.send(f"{ctx.author.mention}, У вас недостаточно прав!", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send(f"{ctx.author.mention}, You don't have enough permissions!", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(ClearChat(bot))