import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3
from PIL import Image, ImageDraw, ImageFilter
from typing import List
import os
from settings import limitsHeight, limitsWidth

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite ImageTools] database.db загружен!")

actionsImages = [
    "gray",
    "inverse",
    "shades of gray",
    "blur",
    "contour",
    "detail",
    "edge_enhance",
    "edge_enhance_more",
    "emboss",
    "find_edges",
    "smooth",
    "smooth_more",
    "sharpen"
]

async def autocomplete_image_actions(inter, string: str) -> List[str]:
    return [lang for lang in actionsImages if string.lower() in lang.lower()]

class ImageTools(commands.Cog):
    @commands.slash_command(description=Localized("Tools for working with images", key="IMAGE_TOOLS_DESCRIPTION"))
    async def image(ctx, image: discord.Attachment, action: str = commands.Param(autocomplete=autocomplete_image_actions)):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        if image.height > limitsHeight:
            await ctx.send("Невозможно обработать изображение: Разрешение больше 8К | Unable to process image: Resolution greater than 8K")
            noRender = True
        if image.width > limitsWidth:
            await ctx.send("Невозможно обработать изображение: Разрешение больше 8К | Unable to process image: Resolution greater than 8K")
            noRender = True

        try: await ctx.response.defer()
        except: pass

        if image.filename.endswith(".png"):
            await image.save(f"./temp/imageFilter/{ctx.author.id}.png")

            image = Image.open(f'./temp/imageFilter/{ctx.author.id}.png')
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()

            if action == "gray":
                for x in range(width):
                    for y in range(height):
                        r = pix[x, y][0]
                        g = pix[x, y][1]
                        b = pix[x, y][2]
                        sr = (r + g + b) // 3
                        draw.point((x, y), (sr, sr, sr))
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")
            
            if action == "inverse":
                for x in range(width):
                    for y in range(height):
                        r = pix[x, y][0]
                        g = pix[x, y][1]
                        b = pix[x, y][2]
                        draw.point((x, y), (255 - r, 255 - g, 255 - b))
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")
            
            if action == "shades of gray":
                for x in range(width):
                    for y in range(height):
                        r = pix[x, y][0]
                        g = pix[x, y][1]
                        b = pix[x, y][2]
                        if (r+g+b)>100:
                            sr = (r + g + b) // 3
                            draw.point((x, y), (255-sr, 255-sr, 255-sr))
                        else:
                            sr = (r + g + b) // 3
                            draw.point((x, y), (sr, sr, sr))
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "blur":
                image = image.filter(ImageFilter.BLUR)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "contour":
                image = image.filter(ImageFilter.CONTOUR)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")
            
            if action == "detail":
                image = image.filter(ImageFilter.DETAIL)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "edge_enhance":
                image = image.filter(ImageFilter.EDGE_ENHANCE)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "edge_enhance_more":
                image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "emboss":
                image = image.filter(ImageFilter.EMBOSS)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "find_edges":
                image = image.filter(ImageFilter.FIND_EDGES)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "smooth":
                image = image.filter(ImageFilter.SMOOTH)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "smooth_more":
                image = image.filter(ImageFilter.SMOOTH_MORE)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")

            if action == "sharpen":
                image = image.filter(ImageFilter.SHARPEN)
                image.save(f"./temp/imageFilter/{ctx.author.id}_output.png", "PNG")
                await ctx.send(file=discord.File(f"./temp/imageFilter/{ctx.author.id}_output.png"))
                os.remove(f"./temp/imageFilter/{ctx.author.id}.png")
                os.remove(f"./temp/imageFilter/{ctx.author.id}_output.png")
        else:
            if langCodeReal == "ru":
                await ctx.send("Картинка не поддерживается! Поддерживается: PNG")
            if langCodeReal == "en":
                await ctx.send("Image not supported! Supported: PNG")

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(ImageTools(bot))