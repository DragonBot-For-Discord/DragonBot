import disnake as discord
from disnake.ext import commands
from disnake.utils import get
import sqlite3

embedColor = 0x520500
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

class EventOnGuildJoin(commands.Cog):
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f'[DragonBot] Меня добавили на {guild.name}')

        cursor.execute(f"INSERT INTO guilds_lang(guild_id, lang_code) VALUES({guild.id}, 'ru')")
        conn.commit()

        channel = guild.text_channels[0]
        embed = discord.Embed(title="Спасибо за добавление DragonBot!", description="Совсем немного осталось для нормальной работы бота!", color=embedColor)
        embed.add_field(name="Шаг 1", value=f"Выдайте DragonBotу права администратора", inline=False)
        embed.add_field(name="Шаг 2", value=f"Сделайте роль DragonBotа выше всех (Кроме создателя)", inline=False)
        embed.add_field(name="Шаг 3", value=f"Установите язык бота на сервере (По умолчанию стоит Русский): /switch_lang [ru, en] yes", inline=False)
        embed.add_field(name="Шаг 4", value=f"Всё уже настроено! Для работы команд модераций, такие как /ban, /kick, /mute, нужно выполнить первые 2 шага", inline=False)
        await channel.send(embed = embed)

def setup(bot):
    bot.add_cog(EventOnGuildJoin(bot))