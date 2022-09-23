import disnake as discord
from disnake.ext import commands

class DeleteSpamRoles(commands.Cog):
    @commands.slash_command(description="Удалить роли с одинаковым названием")
    async def del_spam_roles(inter, rolename):
        if inter.author.guild_permissions.manage_roles:
            await inter.response.send_message(f'Начало удаления спам ролей с именем **{rolename}**', ephemeral=True)
            length = 0
            l = 0
            for role in inter.guild.roles:
                if role.name == rolename:
                    length +=1
                    l +=1
            msg = await inter.channel.send(embed=discord.Embed(title='Удаление спам ролей', description='Осталось: ...', color=0xFF0000))
            if length == 0:
                await msg.edit(embed=discord.Embed(title='Удаление спам ролей', description=f'Канал с таким именем не найдены', color=0xFF0000))
            else:
                for role in inter.guild.roles:
                    if role.name == rolename:
                        await role.delete()
                        length -= 1
                        await msg.edit(embed=discord.Embed(title='Удаление спам ролей', description=f'Осталось: {length}', color=0xFF0000))
                await msg.edit(embed=discord.Embed(title='Удаление спам ролей', description=f'Удалено {l} ролей', color=0xFF0000))
        else:
            await inter.response_send_message(f'{inter.author.mention}, У вас недостаточно прав!', ephemeral=True)

def setup(bot):
    bot.add_cog(DeleteSpamRoles(bot))