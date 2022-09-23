import disnake as discord
from disnake.ext import commands
from disnake.utils import get
import sqlite3
import httpx
import json
import asyncio

requests = httpx.AsyncClient()

embedColor = 0x520500

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite EventOnGuildLeave] database.db загружен!")

actionsAutoModToggle = [
    "spam",
    "raid",
    "badwords",
    "crash",
    "botVerified"
]

class EventOnGuildLeave(commands.Cog):
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		print(f'[DragonBot] Меня убрали с {guild.name}')
		request = await requests.get(f"https://discord.com/api/guilds/{guild.id}/widget.json")
		data = json.loads(request.text)
		message = "message" in data
		await asyncio.sleep(10)
		if message != False:
			if data['message'] == "Unknown Guild":
				for automodFeature in actionsAutoModToggle:
					try:
						cursor.execute(f"DELETE * FROM automod_{actionsAutoModToggle} WHERE guild_id = {guild.id}")
						connection.commit()
					except:
						pass

				try:
					cursor.execute(f"DELETE * FROM genai_enabled WHERE guild_id = {guild.id}")
					connection.commit()
				except:
					pass

				try:
					cursor.execute(f"DELETE * FROM guilds_backup WHERE guild_id = {guild.id}")
					connection.commit()
				except:
					pass

				try:
					cursor.execute(f"DELETE * FROM guilds_lang WHERE guild_id = {guild.id}")
					connection.commit()
				except:
					pass

				try:
					cursor.execute(f"DELETE * FROM interserver_enabled WHERE guild_id = {guild.id}")
					connection.commit()
				except:
					pass

				try:
					cursor.execute(f"DELETE * FROM forum_enabled WHERE guild_id = {guild.id}")
					connection.commit()
				except:
					pass

def setup(bot):
    bot.add_cog(EventOnGuildLeave(bot))