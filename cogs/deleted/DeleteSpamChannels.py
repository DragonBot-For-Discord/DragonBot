import disnake as discord
from disnake.ext import commands

class DeleteSpamChannels(commands.Cog):
    @commands.slash_command(description="Удалить каналы с одинаковым названием")
    async def del_spam_channels(inter, channelname):
        if inter.author.guild_permissions.manage_channels:
            await inter.response.send_message(f'Начало удаления спам каналов с именем **{channelname}**', ephemeral=True)
            length = 0
            l = 0
            for channel in inter.guild.channels:
                if channel.name == channelname:
                    length +=1
                    l +=1
            msg = await inter.channel.send(embed=discord.Embed(title='Удаление спам каналов', description='Осталось: ...', color=0xFF0000))
            if length == 0:
                await msg.edit(embed=discord.Embed(title='Удаление спам каналов', description=f'Канал с таким именем не найдены', color=0xFF0000))
            else:
                for channel in inter.guild.channels:
                    if channel.name == channelname:
                        await channel.delete()
                        length -= 1
                        await msg.edit(embed=discord.Embed(title='Удаление спам каналов', description=f'Осталось: {length}', color=0xFF0000))
                await msg.edit(embed=discord.Embed(title='Удаление спам каналов', description=f'Удалено {l} каналов', color=0xFF0000))
        else:
            await inter.response_send_message(f'{inter.author.mention}, У вас недостаточно прав!', ephemeral=True)

def setup(bot):
    bot.add_cog(DeleteSpamChannels(bot))