import disnake as discord
from disnake.ext import commands
from disnake import Localized
import os


class FileUpload(commands.Cog):
    @commands.slash_command(description=Localized("Upload file to server", key="FILE_UPLOAD_DESCRIPTION"))
    async def file_upload(ctx, file: discord.Attachment):
        await ctx.response.defer()

        try:
            os.mkdir(f'./user/files/{ctx.author.id}')
        except:
            pass

        await file.save(f"./user/files/{ctx.author.id}/{file.filename}")

        await ctx.send(f"Файл был загружен на сервер под названием: {file.filename}\nThe file was uploaded to the server with name: {file.filename}")

    @commands.slash_command(description=Localized("Get file from server", key="FILE_GET_DESCRIPTION"))
    async def file_get(ctx, file: str):
        try:
            await ctx.send(file=discord.File(f"./user/files/{ctx.author.id}/{file}"))
        except:
            await ctx.send(f"Неизвестный или слишком большой файл: {file}\nUnknown or too large file: {file}")

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(FileUpload(bot))