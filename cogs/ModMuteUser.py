import disnake as discord
from disnake.ext import commands
from disnake.utils import get
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite ModMuteUser] database.db загружен!")

embedColor = 0x520500

class ModMuteUser(commands.Cog):
    @commands.slash_command(description=Localized("Mute a user", key="MOD_MUTE_DESCRIPTION"))
    @commands.has_permissions(moderate_members = True)
    async def mute(ctx, member: discord.Member, duration: int, *, reason=None):
        langCodeReal = "en"

        if member.id == ctx.author.id:
            if langCodeReal == "ru":
                embed = discord.Embed(title="Мут", description=f"Вы не можете мутить себя", color=embedColor)
                await ctx.send(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title="Mute", description=f"You can't mute yourself", color=embedColor)
                await ctx.send(embed = embed)
        else:
            roleOne = get(ctx.guild.roles, id=ctx.guild.get_member(ctx.author.id).top_role.id) # Высшая роль
            roleMember = get(ctx.guild.roles, id=ctx.guild.get_member(member.id).top_role.id) # Высшая роль у пользователя

            if roleOne.position > roleMember.position:
                await member.timeout(duration=duration, reason=reason)
                if langCodeReal == "ru":
                    embed = discord.Embed(title="Мут", description=f"Пользователь {member.name} был отправлен в мут по причине {reason}", color=embedColor)
                    await ctx.send(embed = embed)
                if langCodeReal == "en":
                    embed = discord.Embed(title="Mute", description=f"User {member.name} was sent to mute by reason {reason}", color=embedColor)
                    await ctx.send(embed = embed)
            else:
                if langCodeReal == "ru":
                    await ctx.send("Этот человек не может быть отправлен в мут, потому что его роль выше вашей", ephemeral=True)
                if langCodeReal == "en":
                    await ctx.send("This person can't be sent to mute, because his role is higher than yours", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(ModMuteUser(bot))