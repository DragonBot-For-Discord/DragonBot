import disnake as discord
from disnake.ext import commands
from disnake.utils import get
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite ModBanUser] database.db загружен!")

embedColor = 0x520500

class ModBanUser(commands.Cog):
    @commands.slash_command(description=Localized("Ban a user", key="MOD_BAN_DESCRIPTION"))
    @commands.has_permissions(ban_members = True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        langCodeReal = "en"

        if member.id == ctx.author.id:
            if langCodeReal == "ru":
                embed = discord.Embed(title="Бан", description=f"Вы не можете банить себя", color=embedColor)
                await ctx.send(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title="Ban", description=f"You can't ban yourself", color=embedColor)
                await ctx.send(embed = embed)
        else:
            roleOne = get(ctx.guild.roles, id=ctx.guild.get_member(ctx.author.id).top_role.id) # Высшая роль
            roleMember = get(ctx.guild.roles, id=ctx.guild.get_member(member.id).top_role.id) # Высшая роль у пользователя

            if roleOne.position > roleMember.position:
                if langCodeReal == "ru":
                    await member.send(f"{ctx.author.mention} вы были забанены на сервере {ctx.guild.name} по причине: {reason}")
                    await member.ban(reason=reason)
                    embed = discord.Embed(title="Бан", description=f"Пользователь {member.name}#{member.discriminator} был забанен по причине {reason}", color=embedColor)
                    await ctx.send(embed = embed)
                if langCodeReal == "en":
                    await member.send(f"{ctx.author.mention} you were banned on the server {ctx.guild.name} because: {reason}")
                    await member.ban(reason=reason)
                    embed = discord.Embed(title="Ban", description=f"User {member.name}#{member.discriminator} was banned for {reason}", color=embedColor)
                    await ctx.send(embed = embed)
            else:
                if langCodeReal == "ru":
                    await ctx.send("Этот человек не может быть забанен, потому что его роль выше вашей", ephemeral=True)
                if langCodeReal == "en":
                    await ctx.send("This person can't be banned, because his role is higher than yours", ephemeral=True)


def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(ModBanUser(bot))