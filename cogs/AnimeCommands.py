import disnake as discord
from disnake.ext import commands
from disnake import Localized
import httpx
import json
import sqlite3
from typing import List

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite AnimeCommands] database.db загружен!")

requests = httpx.AsyncClient()

actionsAnimeType = ["wink", "pat", "hug"]

async def autocomplete_anime_actions(inter, string: str) -> List[str]:
    return [lang for lang in actionsAnimeType if string.lower() in lang.lower()]

class AnimeCommands(commands.Cog):
    @commands.slash_command(description=Localized("I don't know what to call this command, but it's related to anime", key="ANIME_DESCRIPTION"))
    async def anime(ctx, user: discord.User, action: str = commands.Param(autocomplete=autocomplete_anime_actions)):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        if action == "wink":
            if langCodeReal == "ru":
                embed = discord.Embed(title = f'{ctx.author.name} подмигнул {user.name}')
                response = await requests.get(f'https://some-random-api.ml/animu/wink')
                json_data = json.loads(response.text) 
                embed.set_image(url = json_data['link'])
                await ctx.response.send_message(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title = f'{ctx.author.name} winked at {user.name}')
                response = await requests.get(f'https://some-random-api.ml/animu/wink')
                json_data = json.loads(response.text) 
                embed.set_image(url = json_data['link'])
                await ctx.response.send_message(embed = embed)
        if action == "pat":
            if langCodeReal == "ru":
                embed = discord.Embed(title = f'{ctx.author.name} погладил {user.name}')
                response = await requests.get(f'https://some-random-api.ml/animu/pat')
                json_data = json.loads(response.text) 
                embed.set_image(url = json_data['link'])
                await ctx.response.send_message(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title = f'{ctx.author.name} strocked {user.name}')
                response = await requests.get(f'https://some-random-api.ml/animu/pat')
                json_data = json.loads(response.text) 
                embed.set_image(url = json_data['link'])
                await ctx.response.send_message(embed = embed)
        if action == "hug":
            if langCodeReal == "ru":
                embed = discord.Embed(title = f'{ctx.author.name} обнял {user.name}')
                response = await requests.get(f'https://some-random-api.ml/animu/hug')
                json_data = json.loads(response.text) 
                embed.set_image(url = json_data['link'])
                await ctx.response.send_message(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title = f'{ctx.author.name} hugged {user.name}')
                response = await requests.get(f'https://some-random-api.ml/animu/hug')
                json_data = json.loads(response.text) 
                embed.set_image(url = json_data['link'])
                await ctx.response.send_message(embed = embed)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(AnimeCommands(bot))