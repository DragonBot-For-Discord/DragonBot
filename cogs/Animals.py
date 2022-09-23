import disnake as discord
from disnake.ext import commands
from disnake import Localized
import httpx
import json
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite Animals] database.db загружен!")

requests = httpx.AsyncClient()

class AnimalsCommandViewRU(discord.ui.View):
    @discord.ui.button(label="Лиса", style=discord.ButtonStyle.grey)
    async def fox(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото лисы')
        response = await requests.get(f'https://some-random-api.ml/img/fox')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Собака", style=discord.ButtonStyle.grey)
    async def dog(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото собаки')
        response = await requests.get(f'https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Кот", style=discord.ButtonStyle.grey)
    async def cat(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото кота')
        response = await requests.get(f'https://some-random-api.ml/img/cat')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Панда", style=discord.ButtonStyle.grey)
    async def panda(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото панды')
        response = await requests.get(f'https://some-random-api.ml/img/panda')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Красная панда", style=discord.ButtonStyle.grey)
    async def red_panda(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото красной панды')
        response = await requests.get(f'https://some-random-api.ml/img/red_panda')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Коала", style=discord.ButtonStyle.grey)
    async def koala(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото коалы')
        response = await requests.get(f'https://some-random-api.ml/img/red_panda')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Птица", style=discord.ButtonStyle.grey)
    async def bird(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото птицы')
        response = await requests.get(f'https://some-random-api.ml/img/bird')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Енот", style=discord.ButtonStyle.grey)
    async def raccon(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото енота')
        response = await requests.get(f'https://some-random-api.ml/img/raccoon')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Кенгуру", style=discord.ButtonStyle.grey)
    async def kangaroo(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Фото кенгуру')
        response = await requests.get(f'https://some-random-api.ml/img/kangaroo')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

class AnimalsCommandViewEN(discord.ui.View):
    @discord.ui.button(label="Fox", style=discord.ButtonStyle.grey)
    async def fox(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Fox photo')
        response = await requests.get(f'https://some-random-api.ml/img/fox')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Dog", style=discord.ButtonStyle.grey)
    async def dog(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Dog photo')
        response = await requests.get(f'https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Cat", style=discord.ButtonStyle.grey)
    async def cat(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Cat photo')
        response = await requests.get(f'https://some-random-api.ml/img/cat')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="Panda", style=discord.ButtonStyle.grey)
    async def panda(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Panda photo')
        response = await requests.get(f'https://some-random-api.ml/img/panda')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)
    
    @discord.ui.button(label="Red panda", style=discord.ButtonStyle.grey)
    async def red_panda(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Red panda photo')
        response = await requests.get(f'https://some-random-api.ml/img/red_panda')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)
    
    @discord.ui.button(label="Koala", style=discord.ButtonStyle.grey)
    async def koala(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Koala photo')
        response = await requests.get(f'https://some-random-api.ml/img/koala')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)
    
    @discord.ui.button(label="Bird", style=discord.ButtonStyle.grey)
    async def bird(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Bird photo')
        response = await requests.get(f'https://some-random-api.ml/img/bird')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)
    
    @discord.ui.button(label="Raccoon", style=discord.ButtonStyle.grey)
    async def raccon(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Raccoon photo')
        response = await requests.get(f'https://some-random-api.ml/img/raccoon')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)
    
    @discord.ui.button(label="Kangaroo", style=discord.ButtonStyle.grey)
    async def kangaroo(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed( title = f'Kangaroo photo')
        response = await requests.get(f'https://some-random-api.ml/img/kangaroo')
        json_data = json.loads(response.text) 
        embed.set_image(url = json_data['link'])
        await interaction.response.edit_message(embed = embed)

class AnimalsCommand(commands.Cog):
    @commands.slash_command(description=Localized("Shows pictures of animals", key="ANIMALS_DESCRIPTION_SLASH_COMMAND"))
    async def animals(ctx):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
        if langCodeReal == "ru":
            await ctx.response.send_message( embed = discord.Embed( title = 'Животные', description='Выберите кнопку, для просмотров животных'), view=AnimalsCommandViewRU())
        if langCodeReal == "en":
            await ctx.response.send_message( embed = discord.Embed( title = 'Animals', description='Choose button for view animals'), view=AnimalsCommandViewEN())


def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(AnimalsCommand(bot))