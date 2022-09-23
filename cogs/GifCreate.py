import disnake as discord
from disnake.ext import commands
from disnake import Localized
from PIL import Image
import os

frames = []

class GifCreate(commands.Cog):
    @commands.slash_command(description=Localized("Create a gif from images (All formats are supported)", key="GENERATE_GIF_DESCRIPTION"))
    async def gif_create(
        ctx,
        duration: int,
        image1: discord.Attachment,
        image2: discord.Attachment,
        image3: discord.Attachment = None,
        image4: discord.Attachment = None,
        image5: discord.Attachment = None,
        image6: discord.Attachment = None,
        image7: discord.Attachment = None,
        image8: discord.Attachment = None,
        image9: discord.Attachment = None,
        image10: discord.Attachment = None,
        image11: discord.Attachment = None,
        image12: discord.Attachment = None,
        image13: discord.Attachment = None,
        image14: discord.Attachment = None,
        image15: discord.Attachment = None,
        image16: discord.Attachment = None,
        image17: discord.Attachment = None,
        image18: discord.Attachment = None,
        image19: discord.Attachment = None,
        image20: discord.Attachment = None
    ):
        await ctx.response.defer()

        for imgNumber in range(1, 20):
            if imgNumber == 1:
                await image1.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                frames.append(frame)
            if imgNumber == 2:
                await image2.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                frames.append(frame)
            if imgNumber == 3:
                if image3 is not None:
                    await image3.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)
            if imgNumber == 4:
                if image4 is not None:
                    await image4.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)
            if imgNumber == 5:
                if image5 is not None:
                    await image5.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)
            if imgNumber == 6:
                if image6 is not None:
                    await image6.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)
            if imgNumber == 7:
                if image7 is not None:
                    await image7.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 8:
                if image8 is not None:
                    await image8.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 9:
                if image9 is not None:
                    await image9.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 10:
                if image10 is not None:
                    await image10.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 11:
                if image11 is not None:
                    await image11.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 12:
                if image12 is not None:
                    await image12.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 13:
                if image13 is not None:
                    await image13.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 14:
                if image14 is not None:
                    await image14.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 15:
                if image15 is not None:
                    await image15.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 16:
                if image16 is not None:
                    await image16.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 17:
                if image17 is not None:
                    await image17.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 18:
                if image18 is not None:
                    await image18.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 19:
                if image19 is not None:
                    await image19.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

            if imgNumber == 20:
                if image20 is not None:
                    await image20.save(f"./temp/gifCreate/{ctx.author.id}_{imgNumber}.png")
                    frame = Image.open(f'./temp/gifCreate/{ctx.author.id}_{imgNumber}.png')
                    frames.append(frame)

        # Берем первый кадр и в него добавляем оставшееся кадры.
        frames[0].save(
            f'./temp/gifCreate/{ctx.author.id}_output.gif',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=duration,
            loop=0
        )

        await ctx.send(file=discord.File(f"./temp/gifCreate/{ctx.author.id}_output.gif"))

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(GifCreate(bot))