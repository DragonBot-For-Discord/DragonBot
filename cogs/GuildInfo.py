import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3

from DBLib import DBLib

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite GuildInfo] database.db загружен!")

embedColor = 0x520500

membersEmoji = DBLib.emoji("964235369090527292")

class GuildInfo(commands.Cog):
    # guild info
    @commands.slash_command(description=Localized("Server information", key="SERVER_INFO_DESCRIPTION_SLASH_COMMAND"))
    async def guild_info(ctx):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        if langCodeReal == "ru":
            if ctx.guild.description == None:
                description = "Нет описания"
            else:
                description = ctx.guild.description
            embed = discord.Embed(title="Информация о сервере", description=f"Информация о сервере {ctx.guild.name}", color=embedColor)
            embed.add_field(name="Имя сервера: ", value=f"{ctx.guild.name}", inline=True)
            embed.add_field(name="ID сервера: ", value=f"{ctx.guild.id}", inline=True)
            embed.add_field(name="Описание сервера: ", value=f"{description}", inline=True)
            embed.add_field(name="Количество участников: ", value=f"{membersEmoji} | {ctx.guild.member_count}", inline=True)
            embed.add_field(name="Количество ролей: ", value=f"{len(ctx.guild.roles)}", inline=True)
            embed.add_field(name="Количество каналов: ", value=f"{len(ctx.guild.channels)}", inline=True)
            embed.add_field(name="Количество голосовых каналов: ", value=f"{len(ctx.guild.voice_channels)}", inline=True)
            embed.add_field(name="Количество текстовых каналов: ", value=f"{len(ctx.guild.text_channels)}", inline=True)
            embed.add_field(name="Количество категорий: ", value=f"{len(ctx.guild.categories)}", inline=True)
            embed.add_field(name="Количество эмодзи: ", value=f"{len(ctx.guild.emojis)}", inline=True)
            embed.add_field(name="Количество стикеров: ", value=f"{len(ctx.guild.stickers)}", inline=True)
            embed.add_field(name="Сервер создан: ", value=f"<t:{round(ctx.guild.created_at.timestamp())}:f>", inline=True)
            embed.add_field(name="Владелец сервера: ", value=f"{ctx.guild.owner}", inline=True)
            await ctx.send(embed = embed, ephemeral=True)
        if langCodeReal == "en":
            if ctx.guild.description == None:
                description = "No description"
            else:
                description = ctx.guild.description
            embed = discord.Embed(title="Guild info", description=f"Guild info {ctx.guild.name}", color=embedColor)
            embed.add_field(name="Guild name: ", value=f"{ctx.guild.name}", inline=True)
            embed.add_field(name="Guild ID: ", value=f"{ctx.guild.id}", inline=True)
            embed.add_field(name="Guild description: ", value=f"{description}", inline=True)
            embed.add_field(name="Guild members: ", value=f"{ctx.guild.member_count}", inline=True)
            embed.add_field(name="Guild roles: ", value=f"{len(ctx.guild.roles)}", inline=True)
            embed.add_field(name="Guild channels: ", value=f"{len(ctx.guild.channels)}", inline=True)
            embed.add_field(name="Guild voice channels: ", value=f"{len(ctx.guild.voice_channels)}", inline=True)
            embed.add_field(name="Guild text channels: ", value=f"{len(ctx.guild.text_channels)}", inline=True)
            embed.add_field(name="Guild categories: ", value=f"{len(ctx.guild.categories)}", inline=True)
            embed.add_field(name="Guild emojis: ", value=f"{len(ctx.guild.emojis)}", inline=True)
            embed.add_field(name="Guild stickers: ", value=f"{len(ctx.guild.stickers)}", inline=True)
            embed.add_field(name="Guild created: ", value=f"<t:{round(ctx.guild.created_at.timestamp())}:f>", inline=True)
            embed.add_field(name="Guild owner: ", value=f"{ctx.guild.owner}", inline=True)
            await ctx.send(embed = embed, ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(GuildInfo(bot))