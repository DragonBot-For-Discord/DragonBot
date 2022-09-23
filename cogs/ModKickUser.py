import disnake as discord
from disnake.ext import commands
from disnake.utils import get
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite ModKickUser] database.db загружен!")

embedColor = 0x520500

class ModKickUser(commands.Cog):
    @commands.slash_command(description=Localized("Kick a user", key="MOD_KICK_DESCRIPTION"))
    @commands.has_permissions(kick_members = True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        langCodeReal = "en"

        if member.id == ctx.author.id:
            if langCodeReal == "ru":
                embed = discord.Embed(title="Кик", description=f"Вы не можете кикать себя", color=embedColor)
                await ctx.send(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title="Kick", description=f"You can't kick yourself", color=embedColor)
                await ctx.send(embed = embed)
        else:
            roleOne = get(ctx.guild.roles, id=ctx.guild.get_member(ctx.author.id).top_role.id) # Высшая роль
            roleMember = get(ctx.guild.roles, id=ctx.guild.get_member(member.id).top_role.id) # Высшая роль у пользователя

            if roleOne.position > roleMember.position:
                await member.kick(reason=reason)
                if langCodeReal == "ru":
                    embed = discord.Embed(title="Кик", description=f"Пользователь {member.name} был кикнут по причине {reason}", color=embedColor)
                    await ctx.send(embed = embed)
                if langCodeReal == "en":
                    embed = discord.Embed(title="Kick", description=f"User {member.name} was kicked for {reason}", color=embedColor)
                    await ctx.send(embed = embed)
            else:
                if langCodeReal == "ru":
                    await ctx.send("Этот человек не может быть кикнут, потому что его роль выше вашей", ephemeral=True)
                if langCodeReal == "en":
                    await ctx.send("This user can't be kicked, because his role is higher than yours", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(ModKickUser(bot))