import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3

global itemid
global itemNameReal

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite Economic] database.db загружен!")

itemsRealList = ""

class Economic(commands.Cog):
    @commands.slash_command(description=Localized("Your balance", key="ECONOMIC_BALANCE_DESCRIPTION"))
    async def balance(ctx):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        cursor.execute(f"SELECT balance FROM balanceUsers WHERE user_id = {ctx.author.id}")
        balance = cursor.fetchone()
        balanceStr = str(balance)
        balanceReal = balanceStr.replace('(', '').replace(')', '').replace(',', '')
        if balanceReal == 'None':
            if langCodeReal == "ru":
                await ctx.send(f"Ваш баланс: 0$", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send(f"Your balance: 0$", ephemeral=True)
        else:
            if langCodeReal == "ru":
                await ctx.send(f"Ваш баланс: {balanceReal}$", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send(f"Your balance: {balanceReal}$", ephemeral=True)

    @commands.slash_command(description=Localized("Buy item from the store", key="ECONOMIC_BUY_DESCRIPTION"))
    async def buy(ctx, itemname):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        cursor.execute(f"SELECT balance FROM balanceUsers WHERE user_id = {ctx.author.id}")
        balance = cursor.fetchone()
        balanceStr = str(balance)
        balanceReal = balanceStr.replace('(', '').replace(')', '').replace(',', '')
        balanceRealInt = int(balanceReal)
        cursor.execute(f"SELECT balance FROM balanceUsers WHERE user_id = 982395358841827379")
        balanceDF = cursor.fetchone()
        balanceDFStr = str(balanceDF)
        balanceDFReal = balanceDFStr.replace('(', '').replace(')', '').replace(',', '')
        balanceRealDFInt = int(balanceDFReal)
        cursor.execute(f"SELECT item_price FROM shop_items WHERE itemName = '{itemname}'")
        itemPrice = cursor.fetchone()
        itemPriceStr = str(itemPrice)
        itemPriceReal = itemPriceStr.replace('(', '').replace(')', '').replace(',', '')
        itemPriceRealInt = int(itemPriceReal)
        cursor.execute(f"SELECT itemName FROM shop_items WHERE itemName = '{itemname}'")
        itemName = cursor.fetchone()
        itemNameStr = str(itemName)
        itemNameReal = itemNameStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
        if itemName == None:
            if langCodeReal == "ru":
                embed = discord.Embed(title="Ошибка", description=f"Предмета с данным ID не существует")
                await ctx.send(embed = embed)
            if langCodeReal == "en":
                embed = discord.Embed(title="Error", description=f"Item with this ID does not exist")
                await ctx.send(embed = embed)
        else:
            if itemPriceRealInt == None:
                if langCodeReal == "ru":
                    embed = discord.Embed(title="Ошибка", description=f"Ваш баланс: {balanceReal}$")
                    await ctx.send(embed = embed)
                if langCodeReal == "en":
                    embed = discord.Embed(title="Error", description=f"Your balance: {balanceReal}$")
                    await ctx.send(embed = embed)
            if itemPriceRealInt > balanceRealInt:
                if langCodeReal == "ru":
                    embed = discord.Embed(title="Ошибка", description=f"Ваш баланс: {balanceReal}$")
                    await ctx.send(embed = embed)
                if langCodeReal == "en":
                    embed = discord.Embed(title="Error", description=f"Your balance: {balanceReal}$")
                    await ctx.send(embed = embed)
            else:
                cursor.execute(f"UPDATE balanceUsers SET balance = {balanceRealInt - itemPriceRealInt} WHERE user_id = {ctx.author.id}")
                connection.commit()

                cursor.execute(f"UPDATE balanceUsers SET balance = {balanceRealDFInt + itemPriceRealInt} WHERE user_id = 982395358841827379")
                connection.commit()

                if langCodeReal == "ru":
                    await ctx.send(f"Успешно! Вы купили **{itemNameReal}**")
                if langCodeReal == "en":
                    await ctx.send(f"Success! You bought **{itemNameReal}**")

    @commands.slash_command(description=Localized("Shop", key="ECONOMIC_SHOP_DESCRIPTION"))
    async def shop(ctx):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        cursor.execute(f"SELECT itemName FROM shop_items")
        items = cursor.fetchall()

        cursor.execute(f"SELECT item_price FROM shop_items")
        item_prices = cursor.fetchall()
        for item in items:
            itemsStr = str(item)
            itemsReal = itemsStr.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
            global itemsRealList
            itemsRealList = itemsRealList + itemsReal + "\n"
        
        if langCodeReal == "ru":
            embed = discord.Embed(title="Магазин", description=f"{itemsRealList}")
            await ctx.send(embed = embed)
        if langCodeReal == "en":
            embed = discord.Embed(title="Shop", description=f"{itemsRealList}")
            await ctx.send(embed = embed)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(Economic(bot))