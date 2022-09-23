import disnake as discord
from disnake.ext import commands
from disnake import Localized
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import sqlite3
import os
import io
import requests
from settings import blurTimes

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite RankCard] database.db загружен!")

# Rank card generation settings
blured = 0

class RankCard(commands.Cog):
    @commands.slash_command(description=Localized("Set your own font for the rank card", key="RANK_CARD_SET_OWN_FONT_DESCRIPTION"))
    async def rank_card_set_font(ctx, font: discord.Attachment):
        await ctx.response.defer()

        if font.filename.endswith(".ttf"):
            await font.save(f"./user/font/{ctx.author.id}.ttf")
            await ctx.send("Шрифт для карточки ранга был обновлён\nThe font for the rank card has been updated")
        else:
            await ctx.send("Шрифт не поддерживается! Поддерживается: TTF\nFont not supported! Supported: TTF")

    @commands.slash_command(description=Localized("Put your banner for the rank card", key="RANK_CARD_SET_OWN_BACKGROUND_DESCRIPTION"))
    async def rank_card_set_background(ctx, image: discord.Attachment):
        await ctx.response.defer()

        if image.filename.endswith(".png"):
            if image.height == 200:
                if image.width == 600:
                    await image.save(f"./user/card/{ctx.author.id}.png")
                    await ctx.send("Баннер для карточки ранга был обновлён\nThe banner for the rank card has been updated")
                else:
                    await ctx.send("Изображение не поддерживается! Ширина картинки должна быть 600 пикселей\nImage not supported! The width of the picture must be 600 pixels")
            else:
                await ctx.send("Изображение не поддерживается! Высота картинки должна быть 200 пикселей\nImage not supported! The height of the picture must be 200 pixels")
        else:
            await ctx.send("Изображение не поддерживается! Поддерживается: PNG\nImage not supported! Supported: PNG")

    @commands.slash_command(description=Localized("Set your color for nickname and level in the rank card", key="RANK_CARD_SET_OWN_COLOR_USERNAME_AND_LEVEL_DESCRIPTION"))
    async def rank_card_set_color(ctx, headerr: int, headerg: int, headerb: int, underr: int, underg: int, underb: int):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        await ctx.response.defer()

        try:
            cursor.execute(f"DELETE FROM rank_card_customization WHERE user_id = {ctx.author.id}")
            connection.commit()
        except:
            pass

        cursor.execute(f"INSERT INTO rank_card_customization(user_id, colorHeaderR, colorHeaderG, colorHeaderB, colorUnderR, colorUnderG, colorUnderB) VALUES ({ctx.author.id}, {headerr}, {headerg}, {headerb}, {underr}, {underg}, {underb})")
        connection.commit()
        
        await ctx.send("Цвет для ника и уровня в карточке был обновлён! | The color for the nickname and level in the card has been updated!")

    @commands.slash_command(description=Localized("View my rank", key="RANK_CARD_VIEW_MY_RANK_DESCRIPTION"))
    async def rank_card(ctx):
        cursor.execute(f"SELECT * FROM rank_level WHERE user_id = {ctx.author.id}")
        messages = cursor.fetchall()

        await ctx.response.defer()

        try: img = Image.open(f"./user/card/{ctx.author.id}.png")
        except: img = Image.open(f"./user/card/Default.png")
        
        try:
            fontHeader = ImageFont.truetype(f"./user/font/{ctx.author.id}.ttf", 48)
            fontUnderText = ImageFont.truetype(f"./user/font/{ctx.author.id}.ttf", 30)
        except:
            fontHeader = ImageFont.truetype(f"./user/font/Default.ttf", 48)
            fontUnderText = ImageFont.truetype("./user/font/Default.ttf", 30)

        for i in range(1, blurTimes + 1):
            if i != blurTimes + 1:
                img = img.filter(ImageFilter.BLUR)
                img.save(f"./temp/rank/CardOutput_{ctx.author.id}_{i}" + ".png")
                img = Image.open(f"./temp/rank/CardOutput_{ctx.author.id}_{i}.png")
                global blured
                blured = blured + 1

        cursor.execute(f"SELECT colorHeaderR FROM rank_card_customization WHERE user_id = {ctx.author.id}")
        headerColor = cursor.fetchone()
        headerColorStr = str(headerColor)
        headerColorRealR = headerColorStr.replace('(', '').replace(')', '').replace("'", '')

        cursor.execute(f"SELECT colorHeaderG FROM rank_card_customization WHERE user_id = {ctx.author.id}")
        headerColorG = cursor.fetchone()
        headerColorGStr = str(headerColorG)
        headerColorRealG = headerColorGStr.replace('(', '').replace(')', '').replace("'", '')

        cursor.execute(f"SELECT colorHeaderB FROM rank_card_customization WHERE user_id = {ctx.author.id}")
        headerColorB = cursor.fetchone()
        headerColorBStr = str(headerColorB)
        headerColorRealB = headerColorBStr.replace('(', '').replace(')', '').replace("'", '')




        cursor.execute(f"SELECT colorUnderR FROM rank_card_customization WHERE user_id = {ctx.author.id}")
        underColor = cursor.fetchone()
        underColorStr = str(underColor)
        underColorRealR = underColorStr.replace('(', '').replace(')', '').replace("'", '')

        cursor.execute(f"SELECT colorUnderG FROM rank_card_customization WHERE user_id = {ctx.author.id}")
        underColorG = cursor.fetchone()
        underColorGStr = str(underColorG)
        underColorRealG = underColorGStr.replace('(', '').replace(')', '').replace("'", '')

        cursor.execute(f"SELECT colorUnderB FROM rank_card_customization WHERE user_id = {ctx.author.id}")
        underColorB = cursor.fetchone()
        underColorBStr = str(underColorB)
        underColorRealB = underColorBStr.replace('(', '').replace(')', '').replace("'", '')




        cardReal = Image.open(f"./temp/rank/CardOutput_{ctx.author.id}_{blured}.png")
        draw = ImageDraw.Draw(cardReal)

        if headerColorRealR == "None":
            draw.text((130, 15),f"{ctx.author.name}#{ctx.author.discriminator}",(255,255,255),font=fontHeader)
        else:
            draw.text((130, 15),f"{ctx.author.name}#{ctx.author.discriminator}",(int(headerColorRealR.replace(",", "")),int(headerColorRealG.replace(",", "")),int(headerColorRealB.replace(",", ""))),font=fontHeader)
        messagesLen = len(messages)

        cursor.execute(f"SELECT role FROM members_roles WHERE user_id = {ctx.author.id}")
        members_roles = cursor.fetchone()
        members_rolesStr = str(members_roles)
        members_rolesReal = members_rolesStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        if members_rolesReal == "None": members_rolesRealX = "User"
        if members_rolesReal == "dev": members_rolesRealX = "Developer"

        if messagesLen < 99:
            if headerColorRealR == "None":
                draw.text((130, 15),f"\n\nMessages: {messagesLen}\nRole: {members_rolesRealX}",(255,255,255),font=fontUnderText)
            else:
                draw.text((130, 15),f"\n\nMessages: {messagesLen}\nRole: {members_rolesRealX}",(int(underColorRealR),int(underColorRealB),int(underColorRealG)),font=fontUnderText)
        if messagesLen > 99:
            if underColorRealR == "None":
                draw.text((130, 15),f"\n\nMessages: {messagesLen} (Level {str(messagesLen)[:-2]})\nRole: {members_rolesRealX}",(255,255,255),font=fontUnderText)
            else:
                draw.text((130, 15),f"\n\nMessages: {messagesLen} (Level {str(messagesLen)[:-2]})\nRole: {members_rolesRealX}",(int(underColorRealR.replace(",", "")),int(underColorRealG.replace(",", "")),int(underColorRealB.replace(",", ""))),font=fontUnderText)

        url = str(ctx.author.avatar.url)[:-10]

        response = requests.get(url, stream = True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.ANTIALIAS)

        cardReal.paste(response, (15, 15, 115, 115))
        cardReal.save(f'./temp/rank/CardOutput_{ctx.author.id}_{blured + 1}.png')

        await ctx.send(file=discord.File(f"./temp/rank/CardOutput_{ctx.author.id}_{blured + 1}.png"))

        for i in range(1, 6):
            try: os.remove(f"./temp/rank/CardOutput_{ctx.author.id}_{i}.png")
            except: pass
        
        blured = 0

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(RankCard(bot))