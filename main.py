# Read license before changes: https://github.com/DragonBot-For-Discord/DragonBot/blob/main/LICENCE
#
# Made by DragonFire Community

print('Starting DragonBot...')

import disnake as discord
from disnake.ext import commands
from disnake import Localized
from disnake.utils import get
import os
import datetime
from datetime import *
import sqlite3
import badwords
import time
import sys
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from settings import botBranch, botVersion, devCode, footerText, embedColor, devsList, devTestingUsers, botToken
#from googletrans import Translator
import pprint
import asyncio
import random

#def print(content = ""):
#	pprint.pprint(content)

token = botToken

logo = """
██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗██████╗  ██████╗ ████████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗╚══██╔══╝
██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║██████╔╝██║   ██║   ██║   
██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║██╔══██╗██║   ██║   ██║   
██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝╚██████╔╝   ██║   
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝  ╚═════╝	╚═╝   
"""

# Анти-Спам настройки модуля
#
# time_window_milliseconds - Промежуток времени для max_msg_per_window
# max_msg_per_window - Максимальное количество сообщений за промежуток времени time_window_milliseconds
# author_msg_times - Специальная переменная (НЕ ТРОГАТЬ)
time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}


print()
try:
	print(logo)
except:
	print('DragonBot')
print()

for i, arg in enumerate(sys.argv):
	if arg == "--resetCache":
		print("Resetting Python cache please wait...")
		os.system("rmdir __pycache__ /s /q")
		os.system("cd cogs & rmdir __pycache__ /s /q")
		print("Cache removed")
		exit()
	else:
		pass

print(f"Modern Discord bot on Disnake.py")
print(f"Open source (https://github.com/DragonBot-For-Discord/DragonBot)")
print()
print(f"About:")
print(f" - Version: {botVersion}")
print(f" - Branch: {botBranch}")
print()
print(f"Settings:")
print(f" - Footer text: {footerText}")
print()
print("AntiSpam:")
print(f" - time_window_milliseconds: {time_window_milliseconds}")
print(f" - max_msg_per_window: {max_msg_per_window}")
print()


activity = discord.Streaming(name=f"Version {botVersion} branch {botBranch}", url="https://www.twitch.tv/discord")
bot = commands.Bot(
	command_prefix=discord.ext.commands.when_mentioned, #discord.ext.commands.when_mentioned
	activity=activity,
	intents = discord.Intents.all(),
	allowed_mentions = discord.AllowedMentions.all()
)
#translator = Translator()

cogCount = 0

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		a = f[:-3]
		bot.load_extension('cogs.' + a)
		print("[Cog] Загружен ког: " + a)
		cogCount = cogCount + 1

print(f"[Cog] Загружено когов: {cogCount}")

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite] database.db загружен!")

if os.sys.platform == "win32":
	platformNormal = "Windows"
elif os.sys.platform == "linux":
	platformNormal = "Linux"
elif os.sys.platform == "darwin":
	platformNormal = "macOS"
else:
	platformNormal = "Unknown"

# Events
@bot.event
async def on_ready():
	print(f'[DragonBot] Работает на аккаунте {bot.user.name}#{bot.user.discriminator}')
	global start_time
	start_time = datetime.now()

# Защита Сервера
# Анти-Рейд
THRESHOLD = 5
m = []
time_ = time.time()

def antiraid(member):
	global m
	global time_
	m.append(member)
	if time.time() - time_ >= 15.0:
		time_ = time.time()
		if len(m) >= THRESHOLD:
			return True
		else:
			return False
		m = []


# Блокировка команд для некоторых пользователей
# @bot.before_slash_command_invoke
# @bot.before_user_command_invoke
# @bot.before_message_command_invoke
# async def before_commands_invoke(ctx):
# 	cursor.execute(f"SELECT * FROM banned_users WHERE user_id = {ctx.author.id}")
# 	fetched = cursor.fetchone()
# 	if fetched is not None:
# 		#embed = discord.Embed(title="Доступ запрещён", description=f"Привет {ctx.author.mention}! Вы не можете использовать бота за нарушение правил бота.", color=0xFF0000)
# 		#embed.add_field(name="Причина", value=f"{fetched[0][1]}")
# 		#await ctx.send(embed=embed)
# 		raise discord.ext.commands.CommandError('Not available for this user')
# 	else:
# 		return

# Shard
@bot.event
async def on_shard_connect(shard_id):
	print(f'[DragonBot] Был подключен шард с ID: {shard_id}')

@bot.event
async def on_shard_disconnect(shard_id):
	print(f'[DragonBot] Был отключен шард с ID: {shard_id}')

@bot.after_slash_command_invoke
@bot.after_user_command_invoke
@bot.after_message_command_invoke
async def after_commands_invoke(ctx):
	print(f'[Команда] Команда: /{ctx.application_command.name} | Выполнил: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) | Сервер: {ctx.guild.name} ({ctx.guild.id})')


@bot.event
async def on_member_join(member):
	print(f'[Сервер] Пользователь {member.name}#{member.discriminator} присоединился к серверу {member.guild.name}')

	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {member.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

	cursor.execute(f"SELECT guild_id FROM automod_botVerified WHERE guild_id = {member.guild.id} AND isEnabled = 1")
	automod_botVerified = cursor.fetchone()

	if automod_botVerified is None: pass
	else:
		if member.bot == True:
			if member.public_flags.verified_bot == True:
				print('[Защита] Добавлен проверенный бот')
			if member.public_flags.verified_bot == False:
				entry = await member.guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=1).get()
				member_added_bot = await member.guild.fetch_member(entry.user.id)

				print('[Защита] Добавлен непроверенный бот')
				if langCodeReal == "ru":
					await member.kick(reason = "Непроверенный бот")
					await member.guild.owner.send(f"Привет {member.guild.owner.mention}!\n\nDragonBot обнаружил, что на ваш сервер **{member.guild.name}** был добавлен непроверенный бот ({member.mention}) (Без галочки)\nДобавил бота: {member_added_bot.mention}\nДля обеспечения безопасности сервера, бот был кикнут")
				if langCodeReal == "en":
					await member.kick(reason = "Unverified Bot")
					await member.guild.owner.send(f"Hello {member.guild.owner.mention}!\n\nDragonBot has discovered that an untested bot has been added to your server **{member.guild.name}** ({member.mention}) (Not discord verified)\nWho added bot: {member_added_bot.mention}\nTo ensure the safety of the server, the bot has been kicked")

	cursor.execute(f"SELECT guild_id FROM automod_raid WHERE guild_id = {member.guild.id} AND isEnabled = 1")
	automod_raid_state = cursor.fetchone()

	if automod_raid_state is None: pass
	else:
		raidState = antiraid(member)
		print(f'[Анти-Рейд]: Статус рейда: {raidState}')

		if raidState == True:
			if langCodeReal == "ru":
				await member.send(f"Привет!\n\nНа сервере {member.guild.name} происходит рейд, поэтому вы не можете зайти на сервер.\nЗайдите позже")
				await member.kick(reason='Обнаружен рейд сервера')
			if langCodeReal == "en":
				await member.send(f"Hi!\n\nThe server {member.guild.name} is being raided, so you can't join.\nCome back later")
				await member.kick(reason='Server raid detected')












# Anti-Crash
@bot.event
async def on_guild_channel_create(channel):
	cursor.execute(f"SELECT guild_id FROM automod_crash WHERE guild_id = {channel.guild.id} AND isEnabled = 1")
	automod_crash_state = cursor.fetchone()

	if automod_crash_state is None: return
	else:
		async for entry in channel.guild.audit_logs(limit=1):
			if entry.user.id == 1015321801133412434: return
			if entry.user.id == 1000994060313571358: return
			else:
				print('[Анти-Краш] Попытка краша сервера: Создание каналов')
				try:
					await asyncio.sleep(2)
					await channel.delete(reason = "Попытка краша сервера: Создание каналов")
				except:
					pass

@bot.event
async def on_guild_channel_delete(channel):
	cursor.execute(f"SELECT guild_id FROM automod_crash WHERE guild_id = {channel.guild.id} AND isEnabled = 1")
	automod_crash_state = cursor.fetchone()

	if automod_crash_state is None: return
	else:
		async for entry in channel.guild.audit_logs(limit=1):
			if entry.user.id == 1015321801133412434: return
			if entry.user.id == 1000994060313571358: return
			else:
				print('[Анти-Краш] Попытка краша сервера: Удаление каналов')
				try:
					await asyncio.sleep(2)
					await channel.clone(reason = "Попытка краша сервера: Удаление каналов")
				except:
					pass

@bot.event
async def on_guild_role_create(role):
	cursor.execute(f"SELECT guild_id FROM automod_crash WHERE guild_id = {role.guild.id} AND isEnabled = 1")
	automod_crash_state = cursor.fetchone()

	if automod_crash_state is None: return
	else:
		async for entry in role.guild.audit_logs(limit=1):
			if entry.user.id == 1015321801133412434: return
			if entry.user.id == 1000994060313571358: return
			else:
				print('[Анти-Краш] Попытка краша сервера: Создание ролей')
				try:
					await asyncio.sleep(2)
					await role.delete(reason = "Попытка краша сервера: Создание ролей")
				except:
					pass

@bot.event
async def on_guild_update(before, after):
	cursor.execute(f"SELECT guild_id FROM automod_crash WHERE guild_id = {before.id} AND isEnabled = 1")
	automod_crash_state = cursor.fetchone()

	if automod_crash_state is None: return
	else:
		async for entry in after.audit_logs(limit=1):
			if entry.user.id == 1015321801133412434: return
			if entry.user.id == 1000994060313571358: return
			else:
				print('[Анти-Краш] Попытка краша сервера: Изменение сервера')
				try:
					await asyncio.sleep(2)
					await after.edit(reason = "Попытка краша сервера: Изменение сервера", name = before.name)
				except:
					pass

# # Logs
# @bot.event
# async def on_message_delete(ctx):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {ctx.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])

# 		embed = discord.Embed(title="Сообщение удалено", description=f"Сообщение от {ctx.author.mention} было удалено: ```{ctx.content}```", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_message_edit(before, after):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {before.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Сообщение изменено", description=f"Сообщение от {before.author.mention} было изменено: ```{before.content}```\nНа новое: ```{after.content}```", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_guild_channel_create(channel):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {channel.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Канал создан", description=f"Канал {channel.mention} был создан", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_guild_channel_delete(channel):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {channel.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])

# 		embed = discord.Embed(title="Канал удален", description=f"Канал {channel.mention} был удален", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_guild_channel_update(before, after):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {before.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Канал изменен", description=f"Канал {before.mention} был изменен", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_guild_channel_pins_update(channel, last_pin):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {channel.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Пины обновлены", description=f"Пины в канале {channel.mention} были обновлены", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_member_ban(guild, user):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Пользователь забанен", description=f"Пользователь {user.mention} был забанен", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_member_unban(guild, user):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Пользователь разбанен", description=f"Пользователь {user.mention} был разбанен", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_application_command_permissions_update(app, before, after):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {app.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Права команды изменены", description=f"Права команды {app.name} были изменены", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_invite_create(invite):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {invite.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Инвайт создан", description=f"Инвайт {invite.url} был создан", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return

# @bot.event
# async def on_invite_delete(invite):
# 	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {invite.guild.id}")
# 	logs_channel_id = cursor.fetchone()

# 	if logs_channel_id is not None:
# 		logsChannel = bot.get_channel(logs_channel_id[0])
# 		embed = discord.Embed(title="Инвайт удален", description=f"Инвайт {invite.url} был удален", color=0x540303)
# 		await logsChannel.send(embed=embed)
# 	else:
# 		return





# Анти-Спам
@bot.event
async def on_message(ctx):
	#print(f'[Сообщение] {ctx.author.name} ({ctx.author.id}) | {ctx.guild.name} ({ctx.guild.id}) | {ctx.content}')
	if ctx.author.id == 1000994060313571358: return

	global interserverChannelReal

	try:
		cursor.execute(f"SELECT channel_id FROM forum_enabled WHERE channel_id = {ctx.channel.id} AND guild_id = {ctx.guild.id} AND isEnabled = 1")
		forums_enabled = cursor.fetchone()
		forumsChannelStr = str(forums_enabled)
		forumsChannelReal = forumsChannelStr.replace('(', '').replace(')', '').replace(',', '')
	except:
		print("[on_message] Ошибка при получении статуса forums_enabled на сервере")

	if forums_enabled is None: pass
	else:
		await ctx.create_thread(name = f"{ctx.author.name} | {ctx.content}")

	cursor.execute(f"SELECT guild_id FROM automod_spam WHERE guild_id = {ctx.guild.id} AND isEnabled = 1")
	automod_spam_state = cursor.fetchone()
	if automod_spam_state is None: pass
	else:
		global author_msg_counts

		author_id = ctx.author.id
		# Get current epoch time in milliseconds
		curr_time = datetime.now().timestamp() * 1000

		# Make empty list for author id, if it does not exist
		if not author_msg_times.get(author_id, False):
			author_msg_times[author_id] = []

		# Append the time of this message to the users list of message times
		author_msg_times[author_id].append(curr_time)

		# Find the beginning of our time window.
		expr_time = curr_time - time_window_milliseconds

		# Find message times which occurred before the start of our window
		expired_msgs = [
			msg_time for msg_time in author_msg_times[author_id]
			if msg_time < expr_time
		]

		# Remove all the expired messages times from our list
		for msg_time in expired_msgs:
			author_msg_times[author_id].remove(msg_time)
		# ^ note: we probably need to use a mutex here. Multiple threads
		# might be trying to update this at the same time. Not sure though.

		if len(author_msg_times[author_id]) > max_msg_per_window:
			print("[Анти-Спам] Обнаружен спам от пользователя " + ctx.author.name + "#" + ctx.author.discriminator + " на сервере " + ctx.guild.name)
			try:
				await ctx.delete()
			except:
				print("[Анти-Спам] Ошибка удаления сообщения со спамом! Требуются права")

			try:
				await ctx.author.timeout(duration=60, reason="Спам в канале #" + ctx.channel.name)
			except discord.errors.Forbidden:
				print("[Анти-Спам] Ошибка мута! Требуются права")
			except AttributeError:
				print("[Анти-Спам] Ошибка мута! Почему-то, таймаута нету")

			return

	if ctx.author.bot == True: return

	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

	msgOrig = ctx.content
	msg = ctx.content.lower()

	try:
		cursor.execute(f"INSERT INTO genai_messages(message) VALUES('{msgOrig}')")
		connection.commit()
	except:
		print('[on_message] Ошибка записи сообщения в БД')

	try:
		cursor.execute(f"INSERT INTO rank_level(user_id) VALUES({ctx.author.id})")
		connection.commit()
	except:
		print('[on_message] Ошибка записи сообщения в БД')

	cursor.execute(f"SELECT user_id FROM rank_level WHERE user_id = {ctx.author.id}")
	rank_level_state = cursor.fetchall()
	if len(rank_level_state) == 100:
		if langCodeReal == "ru":
			await ctx.reply("Поздравляю, ты достиг уровня в 100 сообщений!")
		if langCodeReal == "en":
			await ctx.reply("Congratulations, you have reached the 100 messages level!")
	if len(rank_level_state) == 200:
		if langCodeReal == "ru":
			await ctx.reply("Поздравляю, ты достиг уровня в 200 сообщений!")
		if langCodeReal == "en":
			await ctx.reply("Congratulations, you have reached the 200 messages level!")
	if len(rank_level_state) == 300:
		if langCodeReal == "ru":
			await ctx.reply("Поздравляю, ты достиг уровня в 300 сообщений!")
		if langCodeReal == "en":
			await ctx.reply("Congratulations, you have reached the 300 messages level!")
	if len(rank_level_state) == 400:
		if langCodeReal == "ru":
			await ctx.reply("Поздравляю, ты достиг уровня в 400 сообщений!")
		if langCodeReal == "en":
			await ctx.reply("Congratulations, you have reached the 400 messages level!")
	if len(rank_level_state) == 500:
		if langCodeReal == "ru":
			await ctx.reply("Поздравляю, ты достиг уровня в 500 сообщений! Кстати после этого сообщения, сообщения о новом уровне больше не будет")
		if langCodeReal == "en":
			await ctx.reply("Congratulations, you have reached the 500 messages level! By the way, after this message, the message about the new level will no longer be")






	try:
		cursor.execute(f"SELECT guild_id FROM automod_badwords WHERE guild_id = {ctx.guild.id} AND isEnabled = 1")
		automod_badwords_state = cursor.fetchone()
	except:
		print("[on_message] Ошибка при получении статуса автомода на сервере")

	try:
		cursor.execute(f"SELECT channel_id FROM genai_enabled WHERE guild_id = {ctx.guild.id} AND isEnabled = 1")
		genAiChannel = cursor.fetchone()
		genAiChannelStr = str(genAiChannel)
		genAiChannelReal = genAiChannelStr.replace('(', '').replace(')', '').replace(',', '')
	except:
		print("[on_message] Ошибка при получении статуса genai_enabled на сервере")

	try:
		cursor.execute(f"SELECT channel_id FROM interserver_enabled WHERE guild_id = {ctx.guild.id} AND isEnabled = 1")
		interserver_enabled = cursor.fetchone()
		interserverChannelStr = str(interserver_enabled)
		interserverChannelReal = interserverChannelStr.replace('(', '').replace(')', '').replace(',', '')
	except:
		print("[on_message] Ошибка при получении статуса interserver_enabled на сервере")

	if interserver_enabled is None: pass
	else:
		if ctx.channel.id == int(interserverChannelReal):
			cursor.execute(f"SELECT author_id FROM interserver_bans WHERE author_id = {ctx.author.id}")
			authoridBanned = cursor.fetchone()
			global isBanned
			if authoridBanned is None: isBanned = False
			else:
				cursor.execute(f"SELECT reason FROM interserver_bans WHERE author_id = {ctx.author.id}")
				reasonBanned = cursor.fetchone()
				reasonBannedStr = str(reasonBanned)
				reasonBannedReady = reasonBannedStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
				if langCodeReal == "ru":
					await ctx.reply(f"❌ | Вы были заблокированы в меж-сервере. Причина: {reasonBannedReady}")
				if langCodeReal == "en":
					await ctx.reply(f"❌ | You were banned from interserver. Reason: {reasonBannedReady}")
				isBanned = True
			if isBanned == False:
				cursor.execute(f"SELECT channel_id FROM interserver_enabled WHERE isEnabled = 1")
				connection.commit()
				interserver_channel = cursor.fetchall()
				for channelx in interserver_channel:
					channely = str(channelx)
					channelReal = channely.replace('(', '').replace(')', '').replace(',', '')
					channelToSend = bot.get_channel(int(channelReal))
					contentReady = ctx.content.replace("@everyone", "").replace("@here", "")
					if int(channelReal) == ctx.channel.id: pass
					else:
						embed = discord.Embed(
							title=f"{ctx.author.name}#{ctx.author.discriminator}",
							description=f"{contentReady}",
							url=f"https://discord.com/users/{ctx.author.id}"
						)
						embed.set_thumbnail(url = ctx.author.display_avatar.url)
						if not ctx.attachments: pass
						else: embed.set_image(url = ctx.attachments[0].url)
						embed.set_footer(text = f"{ctx.guild.name} ({ctx.guild.id})\nMessage ID: {ctx.id}")

						try:
							await asyncio.sleep(2)
							await channelToSend.send(embed = embed)
						except:
							pass
				await ctx.add_reaction("📨")
				await asyncio.sleep(3)
				await ctx.clear_reaction("📨")
	
	if genAiChannel is None: pass
	else:
		if ctx.channel.id == int(genAiChannelReal):
			await asyncio.sleep(1.5)
			try:
				cursor.execute(f"SELECT message FROM genai_messages ORDER BY RANDOM() LIMIT 1")
				genAiMessage = cursor.fetchone()
				genAiMessageReady = str(genAiMessage).replace("('", '').replace("',)", '').replace("'", '').replace("@", "")
			except:
				cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
				langCode = cursor.fetchone()
				langCodeStr = str(langCode)
				langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

				if langCodeReal == "ru":
					genAiMessageReady = "Произошла ошибка во время генераций сообщения."
				if langCodeReal == "en":
					genAiMessageReady = "An error occurred during generation of message."
			await ctx.channel.send(genAiMessageReady)
		else:
			pass

	if automod_badwords_state is None: pass
	else:
		for msg in badwords.bad_words:
			if msg in ctx.content.lower():
				try:
					await ctx.delete()
				except:
					print(f"[Фильтр матов] Не удалось удалить сообщение от {ctx.author.name}")

				try:
					cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
					langCode = cursor.fetchone()
					langCodeStr = str(langCode)
					langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
					if langCodeReal == "ru":
						await ctx.author.send(f"{ ctx.author.name }, мы обнаружили плохие слова в вашем сообщений\nСообщение было удалено")
					if langCodeReal == "en":
						await ctx.author.send(f"{ ctx.author.name }, we found bad words in your message\nMessage was deleted")
				except:
					print(f"[Фильтр матов] Не удалось отправить сообщение {ctx.author.name}")
				break

# Commands
# User commands
# Avatar
@bot.user_command(name=Localized("Avatar", key="VIEW_USER_AVATAR_BUTTON"))
async def avatar(inter: discord.ApplicationCommandInteraction, user: discord.User):
	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {inter.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
	if langCodeReal == "ru":
		emb = discord.Embed(title=f"Аватар {user}")
		emb.set_image(url=user.display_avatar.url)
		await inter.response.send_message(embed=emb, ephemeral=True)
	if langCodeReal == "en":
		emb = discord.Embed(title=f"Avatar {user}")
		emb.set_image(url=user.display_avatar.url)
		await inter.response.send_message(embed=emb, ephemeral=True)

# info user
@bot.user_command(name=Localized("User info", key="VIEW_USER_INFO_BUTTON"))
async def info(inter: discord.ApplicationCommandInteraction, user: discord.User):
	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {inter.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
	if langCodeReal == "ru":
		usrStatus = str(user.status)
		if usrStatus == "idle":
			stat = "Неактивен"
		elif usrStatus == "dnd":
			stat = "Не беспокоить"
		elif usrStatus == "online":
			stat = "Онлайн"
		elif usrStatus == "offline":
			stat = "Оффлайн"
		elif usrStatus == None:
			stat = '**Активность Отсутствует**'
		else:
			stat = f"Неизвесно ({user.status})"
		embed = discord.Embed(title=f"Информация о {user.name}", description=f"""
		Имя пользователя и тэг: **{user.name}#{user.discriminator}**
		ID: **{user.id}**
		Создан: **<t:{round(user.created_at.timestamp())}:f>**
		Статус: **{stat}**
		Ролей: **{len(user.roles)}**
		""",
		color=embedColor)
		embed.set_thumbnail(url = user.display_avatar.url)
		await inter.response.send_message(embed = embed, ephemeral=True)
	elif langCodeReal == "en":
		usrStatus = str(user.status)
		if usrStatus == "idle":
			stat = "Idle"
		elif usrStatus == "dnd":
			stat = "Do Not Disturb"
		elif usrStatus == "online":
			stat = "Online"
		elif usrStatus == "offline":
			stat = "Offline"
		elif usrStatus == None:
			stat = '**Activity is Absent**'
		else:
			stat = f"Unknown ({user.status})"
		embed = discord.Embed(title=f"Information about {user.name}", description=f"""
		User name and tag: **{user.name}#{user.discriminator}**
		ID: **{user.id}**
		Created: **<t:{round(user.created_at.timestamp())}:f>**
		Status: **{stat}**
		Roles: **{len(user.roles)}**
		""",
		color=embedColor)
		embed.set_thumbnail(url = user.display_avatar.url)
		await inter.response.send_message(embed = embed, ephemeral=True)

# Message commands
# Report bad word
@bot.message_command(name=Localized("Report bad word", key="REPORT_BAD_WORD_BUTTON"))
async def report_bad_word(inter: discord.ApplicationCommandInteraction, message: discord.Message):
	rbw_channel = bot.get_channel(998476757416026153)
	embed = discord.Embed(title="Репорт плохого слова для улучшения фильтра матов", description=f"Репорт от: {inter.author}", color=embedColor)
	embed.add_field(name="Сервер: ", value=f"{inter.guild}", inline=False)
	embed.add_field(name="Сообщение с плохим словом: ", value=f"```{message.content}```", inline=False)
	await rbw_channel.send(embed = embed)
	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {inter.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
	if langCodeReal == "ru":
		await inter.response.send_message("Репорт отправлен. Спасибо что помогаете улучшать нашего бота!", ephemeral=True)
	elif langCodeReal == "en":
		await inter.response.send_message("Report sent. Thank you for helping to improve our bot!", ephemeral=True)

# @bot.message_command(name=Localized("Translate to Russian", key="TRANSLATE_TO_RUSSIAN_BUTTON"))
# async def translate_to_russian(inter: discord.ApplicationCommandInteraction, message: discord.Message):
# 	translatedText = translator.translate(message.content, dest="ru")
# 	await inter.response.send_message(translatedText.text, ephemeral=True)

# @bot.message_command(name=Localized("Translate to English", key="TRANSLATE_TO_ENGLISH_BUTTON"))
# async def translate_to_english(inter: discord.ApplicationCommandInteraction, message: discord.Message):
# 	translatedText = translator.translate(message.content, dest="en")
# 	await inter.response.send_message(translatedText.text, ephemeral=True)

# Slash commands
@bot.slash_command(description=Localized("Send bug report", key="SEND_BUG_REPORT_SLASH_COMMAND"))
async def report_bug(ctx, bugreporttext: str):
	rbw_channel = bot.get_channel(998583563857432597)
	embed = discord.Embed(title="Баг репорт", description=f"Репорт от: {ctx.author}", color=embedColor)
	embed.add_field(name="Сервер: ", value=f"{ctx.guild}", inline=False)
	embed.add_field(name="Текст репорта: ", value=f"```{bugreporttext}```", inline=False)
	await rbw_channel.send(embed = embed)
	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
	if langCodeReal == "ru":
		await ctx.response.send_message("Репорт отправлен. Спасибо что помогаете улучшать нашего бота!", ephemeral=True)
	elif langCodeReal == "en":
		await ctx.response.send_message("Report sent. Thank you for helping to improve our bot!", ephemeral=True)

# Slash commands
# about bot
@bot.slash_command(description=Localized("About DragonBot", key="ABOUT_DRAGONBOT_SLASH_COMMAND"))
async def about(ctx):
	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
	if langCodeReal == "ru":
		embed = discord.Embed(title="О DragonBot", description="Ниже показана информания о DragonBot", color=embedColor)
		embed.add_field(name="Версия Python: ", value=f"{os.sys.version}", inline=False)
		embed.add_field(name="Версия Disnake.py: ", value=f"{discord.__version__}", inline=False)
		embed.add_field(name="Версия и ветка бота: ", value=f"{botVersion} ({botBranch})", inline=False)
		embed.add_field(name="Система на которой работает бот: ", value=f"{os.sys.platform} ({platformNormal})", inline=False)
		embed.add_field(name="Задержка: ", value=f"{round(bot.latency * 1000)}ms", inline=False)
		embed.add_field(name="Аптайм: ", value=f"{datetime.now() - start_time}", inline=False)
		embed.add_field(name="Разработчики: ", value=devsList, inline=False)
		await ctx.send(embed = embed, ephemeral=True)
	if langCodeReal == "en":
		embed = discord.Embed(title="About DragonBot", description="Below is information about DragonBot", color=embedColor)
		embed.add_field(name="Python version: ", value=f"{os.sys.version}", inline=False)
		embed.add_field(name="Disnake.py version: ", value=f"{discord.__version__}", inline=False)
		embed.add_field(name="Bot version and branch: ", value=f"{botVersion} ({botBranch})", inline=False)
		embed.add_field(name="System on which the bot is working: ", value=f"{os.sys.platform} ({platformNormal})", inline=False)
		embed.add_field(name="Delay: ", value=f"{round(bot.latency * 1000)}ms", inline=False)
		embed.add_field(name="Uptime: ", value=f"{datetime.now() - start_time}", inline=False)
		embed.add_field(name="Developers: ", value=devsList, inline=False)
		await ctx.send(embed = embed, ephemeral=True)

@bot.slash_command(description=Localized("DragonBot stats", key="STATS_DRAGONBOT_SLASH_COMMAND"))
async def stats(ctx):
	cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
	langCode = cursor.fetchone()
	langCodeStr = str(langCode)
	langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
	if langCodeReal == "ru":
		embed = discord.Embed(title="Статистика DragonBot", description="Ниже показана статистика бота DragonBot", color=embedColor)
		embed.add_field(name = "Серверов", value = len(bot.guilds))
		embed.add_field(name = "Пользователей", value = len(set(bot.get_all_members())))
		embed.add_field(name = "Каналов", value = len(set(bot.get_all_channels())))
		embed.add_field(name = "Голосовых соединений", value = len(bot.voice_clients))
		embed.add_field(name = "Эмодзи", value = len(bot.emojis))
		embed.add_field(name = "Стикеров", value = len(bot.stickers))
		cursor.execute("SELECT * FROM genai_messages")
		embed.add_field(name = "Сообщений в DBotAi (или же GenAi)", value = len(cursor.fetchall()))
		await ctx.send(embed = embed, ephemeral=True)
	if langCodeReal == "en":
		embed = discord.Embed(title="DragonBot statistics", description="Below is shown DragonBot statistics", color=embedColor)
		embed.add_field(name = "Servers", value = len(bot.guilds))
		embed.add_field(name = "Users", value = len(set(bot.get_all_members())))
		embed.add_field(name = "Channels", value = len(set(bot.get_all_channels())))
		embed.add_field(name = "Voice connections", value = len(bot.voice_clients))
		embed.add_field(name = "Emojis", value = len(bot.emojis))
		embed.add_field(name = "Stickers", value = len(bot.stickers))
		cursor.execute("SELECT * FROM genai_messages")
		embed.add_field(name = "Messages in DBotAi (or GenAi)", value = len(cursor.fetchall()))
		await ctx.send(embed = embed, ephemeral=True)




class DeveloperMenuView(discord.ui.View):
	@discord.ui.button(label="Выключить бота", style=discord.ButtonStyle.grey)
	async def shutdown(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
		await bot.close()


	@discord.ui.button(label="Выйти с сервера", style=discord.ButtonStyle.grey)
	async def leave(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
		await interaction.message.guild.leave()


	@discord.ui.button(label="Список серверов", style=discord.ButtonStyle.grey)
	async def servers(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
		guildsList = ""
		for guild in bot.guilds:
			guildsList += f"{guild.name} ({guild.id})\n"

		embed = discord.Embed(title="Список серверов", description=f"{guildsList}", color=embedColor)
		await interaction.send(embed = embed, ephemeral=True)


	@discord.ui.button(label="Забанить пользователя в меж-сервере", style=discord.ButtonStyle.red)
	async def ban_interserver_user(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
		await interaction.response.send_modal(
			title="Введите данные ниже",
			custom_id="dev_panel_control_user_interserver_modal",
			components=[
				discord.ui.TextInput(
					label="ID пользователя",
					placeholder="Введите ID пользователя",
					custom_id="user_id",
					style=discord.TextInputStyle.short,
					min_length=1,
					max_length=50
				),
				discord.ui.TextInput(
					label="Причина блокировки",
					placeholder="Введите причину блокировки",
					custom_id="ban_reason",
					style=discord.TextInputStyle.short,
					min_length=1,
					max_length=200
				)
			]
		)

		# Waits until the user submits the modal.
		try:
			modal_inter: discord.ModalInteraction = await bot.wait_for(
				"modal_submit",
				check=lambda i: i.custom_id == "dev_panel_control_user_interserver_modal" and i.author.id == interaction.author.id,
				timeout=300,
			)
		except:
			return

		userIDtoBan = modal_inter.text_values["user_id"]
		cursor.execute(f"INSERT INTO interserver_bans(author_id, reason) VALUES({userIDtoBan}, '" + modal_inter.text_values["ban_reason"] + "')")
		connection.commit()

		await modal_inter.response.send_message("Готово", ephemeral=True)


	@discord.ui.button(label="Сбросить GenAi", style=discord.ButtonStyle.red)
	async def reset_genai(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
		await interaction.send("Идёт сброс сообщений GenAi, это может занять некоторое время...", ephemeral=True)
		cursor.execute(f"DELETE FROM genai_messages")
		connection.commit()
		await interaction.send("Сообщения GenAi сброшен успешно", ephemeral=True)

	@discord.ui.button(label="Посмотреть ошибку", style=discord.ButtonStyle.grey)
	async def view_error_by_code(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
		await interaction.response.send_modal(
			title="Введите код ошибки",
			custom_id="dev_panel_error_code_view_modal",
			components=[
				discord.ui.TextInput(
					label="Код ошибки",
					placeholder="Введите код ошибки",
					custom_id="error_code",
					style=discord.TextInputStyle.short,
					min_length=1,
					max_length=30
				)
			]
		)

		# Waits until the user submits the modal.
		try:
			modal_inter: discord.ModalInteraction = await bot.wait_for(
				"modal_submit",
				check=lambda i: i.custom_id == "dev_panel_error_code_view_modal" and i.author.id == interaction.author.id,
				timeout=300,
			)
		except:
			return

		for custom_id, value in modal_inter.text_values.items():
			cursor.execute(f"SELECT error FROM errorCodes WHERE errorCode = {value}")
			output = cursor.fetchone()[0]
			await modal_inter.response.send_message(output, ephemeral=True)
	
	@discord.ui.button(label="Сменить статус", style=discord.ButtonStyle.blurple)
	async def change_status(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
		await interaction.response.send_modal(
			title="Введите новый статус",
			custom_id="dev_panel_new_status_modal",
			components=[
				discord.ui.TextInput(
					label="Новый статус",
					placeholder="Введите новый статус",
					custom_id="new_status",
					style=discord.TextInputStyle.short,
					min_length=1,
					max_length=30
				)
			]
		)

		# Waits until the user submits the modal.
		try:
			modal_inter: discord.ModalInteraction = await bot.wait_for(
				"modal_submit",
				check=lambda i: i.custom_id == "dev_panel_new_status_modal" and i.author.id == interaction.author.id,
				timeout=300,
			)
		except:
			return

		for custom_id, value in modal_inter.text_values.items():
			newActivity = discord.Streaming(name = value, url = "https://www.twitch.tv/discord")
			await bot.change_presence(activity=newActivity)
			await modal_inter.response.send_message("Статус был изменён", ephemeral=True)


# Developer commands
# Disable bot
@bot.slash_command(description=Localized("Developer panel (Developers only)", key="DEV_PANEL_DEV_ONLY_DESCRIPTION_SLASH_COMMAND"))
async def dev(inter):
	await inter.response.send_modal(
		title="Введите код разработчика",
		custom_id="dev_panel_modal",
		components=[
			discord.ui.TextInput(
				label="Код разработчика",
				placeholder="Введите код",
				custom_id="code",
				style=discord.TextInputStyle.short,
				min_length=8,
				max_length=30
			)
		]
	)

	# Waits until the user submits the modal.
	try:
		modal_inter: discord.ModalInteraction = await bot.wait_for(
			"modal_submit",
			check=lambda i: i.custom_id == "dev_panel_modal" and i.author.id == inter.author.id,
			timeout=300,
		)
	except:
		return

	for custom_id, value in modal_inter.text_values.items():
		if value == devCode:
			guild = [guild for guild in bot.guilds]
			embedGuilds = discord.Embed(title=f'Серверов: {len(bot.guilds)}', description=f"\n".join(guild.name for guild in guild), color=0xED4245)

			await modal_inter.response.send_message(embed = discord.Embed(title="Панель разработчика", description="Выберите действие", color=embedColor), ephemeral=True, view=DeveloperMenuView())
			#await inter.send(embed = embedGuilds, ephemeral=True)
			return
		else:
			await modal_inter.response.send_message("Неверный код", ephemeral=True)
			return

bot.i18n.load("locale/")
bot.run(token)