import disnake as discord
from disnake.ext import commands
from disnake.utils import get
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite ModUnbanUser] database.db загружен!")

embedColor = 0x520500

class ModUnbanUser(commands.Cog):
    @commands.slash_command(description=Localized("Unban a user", key="MOD_UNBAN_DESCRIPTION"))
    @commands.has_permissions(ban_members = True)
    async def unban(ctx, member: discord.Member, *, reason=None):
        langCodeReal = "en"

        if member.id == ctx.author.id:
            if langCodeReal == "ru":
                embed = discord.Embed(title="Разбан", description=f"Вы не можете разбанить себя", color=embedColor)
                await ctx.send(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title="Unban", description=f"You can't unban yourself", color=embedColor)
                await ctx.send(embed = embed)
        else:
            await member.unban(reason=reason)
            if langCodeReal == "ru":
                embed = discord.Embed(title="Разбан", description=f"Пользователь {member.name} был разбанен по причине {reason}", color=embedColor)
                await ctx.send(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title="Unban", description=f"User {member.name} was unbanned for the reason {reason}", color=embedColor)
                await ctx.send(embed = embed)


def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(ModUnbanUser(bot))