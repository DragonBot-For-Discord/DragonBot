import disnake
from disnake.ext import commands
from disnake import Localized
import sqlite3
from typing import List
import asyncio

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite BackupServer] database.db загружен!")

backupsType = ["create", "restore", "delete"]

async def autocomplete_backup_types(inter, string: str) -> List[str]:
    return [lang for lang in backupsType if string.lower() in lang.lower()]

class BackupServer(commands.Cog):
    @commands.slash_command(description=Localized("Server backup management (Beta)", key="BACKUP_SERVER_DESCRIPTION_SLASH_COMMAND"))
    @commands.has_permissions(administrator = True)
    async def backup(ctx, action: str = commands.Param(autocomplete=autocomplete_backup_types)):
        if action == "create":
            cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
            langCode = cursor.fetchone()
            langCodeStr = str(langCode)
            langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

            if langCodeReal == "ru":
                await ctx.send(f"Бэкап сервера создаётся...", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send(f"Creating server backup...", ephemeral=True)

            cursor.execute(f"DELETE FROM guilds_backup WHERE guild_id = {ctx.guild.id}")
            connection.commit()

            for channel in ctx.guild.channels:
                if channel.category is not None:
                    cursor.execute(f"INSERT INTO guilds_backup (guild_id, item_name, item_type, item_category) VALUES ({ctx.guild.id}, '{channel.name}', '{channel.type}', '{channel.category.name}')")
                    connection.commit()
                else:
                    cursor.execute(f"INSERT INTO guilds_backup (guild_id, item_name, item_type, item_category) VALUES ({ctx.guild.id}, '{channel.name}', '{channel.type}', 'None')")
                    connection.commit()
            
            for role in ctx.guild.roles:
                cursor.execute(f"INSERT INTO guilds_backup (guild_id, item_name, item_type, item_category) VALUES ({ctx.guild.id}, '{role.name}', 'role', '{role.position}')")
                connection.commit()

            if langCodeReal == "ru":
                await ctx.send(f"Бэкап сервера создан. Вы можете восстановить сервер по команде /backup restore", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send(f"Backup of server created. You can restore server by command /backup restore", ephemeral=True)

        if action == "restore":
            cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
            langCode = cursor.fetchone()
            langCodeStr = str(langCode)
            langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
            # restore server backup
            cursor.execute(f"SELECT * FROM guilds_backup WHERE guild_id = {ctx.guild.id} AND NOT item_type = 'role'")
            backup_channels = cursor.fetchall()

            cursor.execute(f"SELECT * FROM guilds_backup WHERE guild_id = {ctx.guild.id} AND item_type = 'role'")
            backup_roles = cursor.fetchall()

            for channel in ctx.guild.channels:
                asyncio.sleep(1)
                try:
                    await channel.delete()
                except:
                    pass

            for role in ctx.guild.roles:
                asyncio.sleep(1)
                try:
                    await role.delete()
                except:
                    pass

            for channel in backup_channels:
                asyncio.sleep(1)
                channelName = channel[1]
                channelType = channel[2]
                channelCategory = channel[3]

                if channelType == "category":
                    try:
                        newChannelCategory = await ctx.guild.create_category_channel(channelName)
                    except:
                        print('[Ошибка] Не удалось создать категорию ' + channelName)
                        pass
                if channelType == "text":
                    try:
                        newChannel = await ctx.guild.create_text_channel(channelName, category = newChannelCategory)
                    except:
                        print('[Ошибка] Не удалось создать канал #' + channelName)
                        pass
                if channelType == "voice":
                    try:
                        newChannel = await ctx.guild.create_voice_channel(channelName, category = newChannelCategory)
                        await newChannel.move(before = channelCategory)
                    except:
                        print('[Ошибка] Не удалось создать канал ' + channelName)
                        pass

            for role in backup_roles:
                asyncio.sleep(1)
                roleName = role[1]
                await ctx.guild.create_role(name=roleName)

        if action == "delete":
            cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
            langCode = cursor.fetchone()
            langCodeStr = str(langCode)
            langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

            cursor.execute(f"DELETE FROM guilds_backup WHERE guild_id = {ctx.guild.id}")
            connection.commit()

            if langCodeReal == "ru":
                await ctx.send(f"Бэкап сервера удален", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send(f"Backup of server deleted", ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(BackupServer(bot))