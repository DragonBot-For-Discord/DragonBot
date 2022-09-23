from disnake.ext import commands
from disnake import Localized
import uuid
import random
import string
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite RandomCommands] database.db загружен!")

class RandomCommands(commands.Cog):
    @commands.slash_command(description=Localized("Generates a random identifier", key="CLEAR_CHAT_DESCRIPTION_SLASH_COMMAND"))
    async def rand_uuid(ctx):
        uuidGenerated = uuid.uuid4()
        await ctx.send(uuidGenerated, ephemeral=True)

    # random number
    @commands.slash_command(description=Localized("Generates a random number", key="RAND_NUMBER_DESCRIPTION"))
    async def rand_number(ctx, minnum: int, maxnum: int):
        randnum = random.randint(minnum, maxnum)
        await ctx.send(randnum, ephemeral=True)

    # random string
    @commands.slash_command(description=Localized("Generates a random string", key="RAND_STRING_DESCRIPTION"))
    async def rand_string(ctx, length: int):
        if length > 500:
            cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
            langCode = cursor.fetchone()
            langCodeStr = str(langCode)
            langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
            if langCodeReal == "ru":
                await ctx.send("Не больше 500 символов", ephemeral=True)
            if langCodeReal == "en":
                await ctx.send("Not more than 500 characters", ephemeral=True)
        else:
            randstring = ''.join(random.choice(string.ascii_letters) for i in range(length))
            print(f'[rand_string] {randstring}')
            await ctx.send(randstring, ephemeral=True)

    @commands.slash_command(description=Localized("Generates a random token (It is not actually valid)", key="RAND_TOKEN_DESCRIPTION"))
    async def rand_token(ctx):
        tokenPart1 = ''.join(random.choice(string.ascii_letters) for i in range(24))
        tokenPart2 = ''.join(random.choice(string.ascii_letters) for i in range(6))
        tokenPart3 = ''.join(random.choice(string.ascii_letters) for i in range(27))
        await ctx.send(f'{tokenPart1}.{tokenPart2}.{tokenPart3}', ephemeral=True)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(RandomCommands(bot))