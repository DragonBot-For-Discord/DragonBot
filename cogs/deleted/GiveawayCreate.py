import disnake as discord
from disnake.ext import commands
from disnake.utils import get
from disnake import Localized
import random
import sqlite3
import asyncio

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite GiveawayCreate] database.db загружен!")


class GiveawayCreate(commands.Cog):
    @commands.slash_command(description="Создать розыгрыш (Альфа)")
    async def gcreate(ctx, time: int, победители: int, channel: discord.TextChannel, prize):
            if not ctx.author.guild_permissions.administrator:
                if ctx.author != ctx.guild.owner:return await ctx.response.send_message(embed=discord.Embed(description='Вы не администратор', color=0x30d5c8),ephemeral=True)
            else:
                global gprize
                global gauthor
                global gmessage
                global gslist
                global gcount

                msg = await ctx.channel.send(f'{ctx.author.mention} разыгрывает {prize}! Конец через {time} секунд')
                await msg.add_reaction(f'🎉')

                await asyncio.sleep(time)

                new_msg = await channel.fetch_message(msg.id)


                users = await new_msg.reactions[0].users().flatten()
                users.pop(users.index(client.user))
                reaction = discord.utils.get(new_msg.reactions, emoji="🎉")
                if reaction:reaction_counter = reaction.count
                if reaction_counter == 0:
                    embed = discord.Embed(title='<:NO:989831387567771698>|Ошибка', description=f'Кто то убрал реакцию бота, и я не могу подсчитать', color=discord.Color.red())
                    try:await channel.send(embed = embed)   
                    except:pass
                    return
                reaction_counter = reaction_counter - 1
                if reaction_counter < победители:
                    победители = reaction_counter
                if reaction_counter == 0:
                    embed = discord.Embed(title='<:NO:989831387567771698>|Неудача', description=f'Никто не выиграл(', color=discord.Color.red())
                    try:await channel.send(embed = embed)   
                    except:pass
                    return
                l = ""
                lu = []
                for i in range (победители):
                    winner=random.choice(users)
                    users.pop(users.index(winner))
                    l += winner.mention + " "
                    lu.append(winner.id)
                gprize = prize
                gauthor = ctx.author.id
                gslist = users
                gscount = reaction_counter - len(lu)
                buttons = discord.ui.View()
                if gscount == 0:buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.red, custom_id="reroll",label="перевыбрать", disabled=True))
                else:
                    buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="reroll",label="перевыбрать"))
                    gcount = gscount
                embed = discord.Embed(title='Победитель', description=f'{l} только что выиграл(и) **{prize}**, мои поздравления ^•^', color=discord.Color.green())
                try:gmessage = await channel.send(embed=embed, view=buttons)
                except discord.Forbidden:return await ctx.response.send_message(embed=discord.Embed(title='<:NO:989831387567771698>|Ошибка', description='У меня нет прав', color=discord.Color.red()),ephemeral=True)
                for i in lu:
                    member = await ctx.guild.fetch_member(int(i))
                    try:await member.send(embed=discord.Embed(title='Вы победили в розыгрыше', description=f'Вы выиграли **{prize}**, мои поздравления ^•^', color=discord.Color.green()))
                    except:pass

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(GiveawayCreate(bot))