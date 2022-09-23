import disnake as discord
from disnake.ext import commands
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite Logs] database.db загружен!")

class Logs(commands.Cog):
    # guild info
    @commands.slash_command(description="Включить/выключить логи сервера")
    async def logs_set(ctx, channel: discord.TextChannel, isenabled: bool):
        if isenabled:
            cursor.execute(f"INSERT INTO logs (guild_id, channel_id, isEnabled) VALUES ({ctx.guild.id}, {channel.id}, 1)")
            connection.commit()
            await ctx.send(f"Логи включены в {channel.mention}")
        else:
            cursor.execute(f"UPDATE logs SET isEnabled = 0 WHERE guild_id = {ctx.guild.id}")
            connection.commit()
            await ctx.send(f"Логи выключены")

def setup(bot):
    bot.add_cog(Logs(bot))